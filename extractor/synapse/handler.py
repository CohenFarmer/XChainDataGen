from typing import Any, Dict, List

from config.constants import Bridge
from extractor.base_handler import BaseHandler
from extractor.synapse.constants import BRIDGE_CONFIG
from repository.database import DBSession
from repository.synapse.repository import (
    SynapseBlockchainTransactionRepository,
    SynapseTokenDepositAndSwapRepository,
    SynapseTokenMintAndSwapRepository,
)
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import CustomException, log_error
from eth_utils import keccak, to_hex


#Topic0 constants for Synapse events (already listed in constants.py)
TOKEN_DEPOSIT_AND_SWAP = (
    "0x79c15604b92ef54d3f61f0c40caab8857927ca3d5092367163b4562c1699eb5f"
)
TOKEN_MINT_AND_SWAP = (
    "0x4f56ec39e98539920503fd54ee56ae0cbebe9eb15aa778f18de67701eeae7c65"
)


class SynapseHandler(BaseHandler):
    CLASS_NAME = "SynapseHandler"

    def __init__(self, rpc_client: EvmRPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.SYNAPSE

    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]):
        return super().get_bridge_contracts_and_topics(
            config=BRIDGE_CONFIG, bridge=bridge, blockchain=blockchain
        )

    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = SynapseBlockchainTransactionRepository(DBSession)
        self.deposit_and_swap_repo = SynapseTokenDepositAndSwapRepository(DBSession)
        self.mint_and_swap_repo = SynapseTokenMintAndSwapRepository(DBSession)

    def does_transaction_exist_by_hash(self, transaction_hash: str) -> Any:
        try:
            return self.blockchain_transaction_repo.get_transaction_by_hash(transaction_hash)
        except Exception as e:
            raise CustomException(self.CLASS_NAME, "does_transaction_exist_by_hash", str(e)) from e

    def handle_events(
        self,
        blockchain: str,
        start_block: int,
        end_block: int,
        contract: str,
        topics: List[str],
        events: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        included: List[Dict[str, Any]] = []
        for event in events:
            try:
                t = event.get("topic")
                if t == TOKEN_DEPOSIT_AND_SWAP:
                    obj = self.handle_deposit_and_swap(blockchain, event)
                elif t == TOKEN_MINT_AND_SWAP:
                    obj = self.handle_mint_and_swap(blockchain, event)
                else:
                    obj = None
                if obj:
                    included.append(event)
            except CustomException as e:
                log_error(self.bridge, str(e))
        return included

    def handle_deposit_and_swap(self, blockchain: str, event: Dict[str, Any]):
        to_addr = event.get("to")
        amount = event.get("amount")
        if self.deposit_and_swap_repo.event_exists(event["transaction_hash"], to_addr, amount):
            return None

        try:
            tx_hash = event["transaction_hash"].lower()
            kappa = to_hex(keccak(text=tx_hash))
            self.deposit_and_swap_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "contract_address": event.get("contract_address"),
                    "to_address": to_addr,
                    "chain_id": str(event.get("chainId")) if event.get("chainId") is not None else None,
                    "token": event.get("token"),
                    "amount": str(amount) if amount is not None else None,
                    "token_index_from": event.get("tokenIndexFrom"),
                    "token_index_to": event.get("tokenIndexTo"),
                    "min_dy": str(event.get("minDy")) if event.get("minDy") is not None else None,
                    "deadline": str(event.get("deadline")) if event.get("deadline") is not None else None,
                    "kappa": kappa[2:],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                "handle_deposit_and_swap",
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e


    def handle_mint_and_swap(self, blockchain: str, event: Dict[str, Any]):
        kappa = event.get("kappa")
        to_addr = event.get("to")
        if self.mint_and_swap_repo.event_exists(event["transaction_hash"], kappa):
            return None

        try:
            self.mint_and_swap_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": event["transaction_hash"],
                    "contract_address": event.get("contract_address"),
                    "to_address": to_addr,
                    "token": event.get("token"),
                    "amount": str(event.get("amount")) if event.get("amount") is not None else None,
                    "fee": str(event.get("fee")) if event.get("fee") is not None else None,
                    "token_index_from": event.get("tokenIndexFrom"),
                    "token_index_to": event.get("tokenIndexTo"),
                    "min_dy": str(event.get("minDy")) if event.get("minDy") is not None else None,
                    "deadline": str(event.get("deadline")) if event.get("deadline") is not None else None,
                    "swap_success": event.get("swapSuccess"),
                    "kappa": kappa,
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                "handle_mint_and_swap",
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e
