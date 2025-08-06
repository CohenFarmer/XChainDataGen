from typing import Any, Dict, List

from config.constants import Bridge
from extractor.across.constants import BRIDGE_CONFIG
from extractor.base_handler import BaseHandler
from repository.cow.repository import (
    CowBlockchainTransactionRepository,
    CowTradeRepository,
    #CowSettlementRepository,
    #CowInteractionRepository,
    #CowOrderInvalidatedRepository,
)
from repository.database import DBSession
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import CustomException, convert_bin_to_hex, log_error
import requests

class CowHandler(BaseHandler):
    CLASS_NAME = "CowHandler"

    def __init__(self, rpc_client: EvmRPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.COW

    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]) -> None:
        return super().get_bridge_contracts_and_topics(
            config=BRIDGE_CONFIG,
            bridge=bridge,
            blockchain=blockchain,
        )

    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = CowBlockchainTransactionRepository(DBSession)
        self.cow_trade_repo = CowTradeRepository(DBSession)
        #self.cow_settlement_repo = CowSettlement(DBSession)
        #self.cow_interaction_repo = CowInteractionRepository(DBSession)
        #self.cow_order_invalidated_repo = CowOrderInvalidatedRepository(DBSession)

    def handle_transactions(self, transactions: List[Dict[str, Any]]) -> None:
        func_name = "handle_transactions"
        try:
            self.blockchain_transaction_repo.create_all(transactions)
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error writing transactions to database: {e}",
            ) from e

    def does_transaction_exist_by_hash(self, transaction_hash: str) -> Any:
        func_name = "does_transaction_exist_by_hash"
        """
        Retrieves a transaction by its hash from the database.

        Args:
            transaction_hash: The hash of the transaction to retrieve.

        Returns:
            The transaction with the given hash.
        """
        try:
            return self.blockchain_transaction_repo.get_transaction_by_hash(transaction_hash)
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error reading transaction from database: {e}",
            ) from e

    def handle_events(
        self,
        blockchain: str,
        start_block: int,
        end_block: int,
        contract: str,
        topics: List[str],
        events: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        included_events = []

        for event in events:
            try:
                if event["topic"] == "0xa07a543ab8a018198e99ca0184c93fe9050a79400a0a723441f84de1d972cc17":
                    event = self.handle_trade(blockchain, event)
                #elif event["topic"] == "0x40338ce1a7c49204f0099533b1e9a7ee0a3d261f84974ab7af36105b8c4e9db4":
                #    event = self.handle_settlement(blockchain, event)
                """elif event["topic"] == "0xed99827efb37016f2275f98c4bcf71c7551c75d59e9b450f79fa32e60be672c2":
                    event = self.handle_interaction(blockchain, event)
                elif event["topic"] == "0x875b6cb035bbd4ac6500fabc6d1e4ca5bdc58a3e2b424ccb5c24cdbebeb009a9":
                    event = self.handle_order_invalidated(blockchain, event)"""

                if event:
                    included_events.append(event)

            except CustomException as e:
                request_desc = (
                    f"Error processing request: {blockchain}, {start_block}, "
                    f"{end_block}, {contract}, {topics}.\n{e}"
                )
                log_error(self.bridge, request_desc)

        return included_events
    
    def handle_trade(self, blockchain, event):
        func_name = "handle_trade"
        
        try:
            if self.cow_trade_repo.event_exists(event["orderUid"]):
                return None
            
            decoded = self.decode_order_uid(event["orderUid"])
            order_hash = decoded["order_hash"]

            enriched_order_data = self.fetch_order_data_from_api(order_hash)

            response = requests.get(f"https://api.cow.fi/mainnet/api/v1/trades/{event['orderUid']}")
            trade_info = response.json()
            tx_hash = trade_info.get("txHash")  
            
            self.cow_trade_repo.create(
                {
                    "blockchain": blockchain,
                    "transaction_hash": tx_hash,
                    "trade_id": event["orderUid"],
                    "owner": event["owner"],
                    "sell_token": event["sellToken"],
                    "buy_token": event["buyToken"],
                    "sell_amount": str(event["sellAmount"]),
                    "buy_amount": str(event["buyAmount"]),
                    "fee_amount": str(event["feeAmount"]),
                    "receiver": enriched_order_data.get("receiver"),
                    "app_data": enriched_order_data.get("appData"),
                    "valid_to": decoded["valid_to"],
                    "order_kind": enriched_order_data.get("kind"),
                    "price_info": enriched_order_data.get("price"),
                    "from_address": enriched_order_data.get("from"),
                    "timestamp": enriched_order_data.get("creationDate"),
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {tx_hash}. Error writing to DB: {e}",
            ) from e
        
    """def handle_settlement(self, blockchain, event):
        func_name = "handle_settlement"

        destination_chain = self.convert_id_to_blockchain_name(event["destinationChainId"])

        if destination_chain is None:
            return None
        
        try:
            if self.cow_settlement_repo.event_exists(event["settlementId"]):
                return None
            
            self.cow_settlement_repo.create(
                {
                    "blockchain": blockchain,
                    "solver": event["solver"],
                }
            )
            return event
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
            ) from e"""
        

    def decode_order_uid(uid_hex: str) -> Dict[str, Any]:
        uid = bytes.fromhex(uid_hex[2:] if uid_hex.startswith("0x") else uid_hex)
        return {
            "order_hash": "0x" + uid[:32].hex(),
            "owner": "0x" + uid[32:52].hex(),
            "valid_to": int.from_bytes(uid[52:56], byteorder="big"),
            }
    
    def fetch_order_data_from_api(self, order_hash: str) -> Dict[str, Any]:
        try:
            url = f"https://api.cow.fi/mainnet/api/v1/orders/{order_hash}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log_error(self.bridge, f"Failed to fetch order data from CoW API: {e}")
            return {}