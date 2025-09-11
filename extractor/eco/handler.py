from typing import Any, Dict, List

from config.constants import Bridge, BLOCKCHAIN_IDS
from extractor.base_handler import BaseHandler
from extractor.eco.constants import BRIDGE_CONFIG
from repository.database import DBSession
from repository.eco.repository import (
    EcoBlockchainTransactionRepository,
    EcoIntentCreatedRepository,
    EcoFulfillmentRepository,
)
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import CustomException, log_error


class EcoHandler(BaseHandler):
    CLASS_NAME = "EcoHandler"

    def __init__(self, rpc_client: EvmRPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.ECO

    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]):
        return super().get_bridge_contracts_and_topics(config=BRIDGE_CONFIG, bridge=bridge, blockchain=blockchain)

    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = EcoBlockchainTransactionRepository(DBSession)
        self.intent_created_repo = EcoIntentCreatedRepository(DBSession)
        self.fulfillment_repo = EcoFulfillmentRepository(DBSession)

    def does_transaction_exist_by_hash(self, transaction_hash: str) -> Any:
        try:
            return self.blockchain_transaction_repo.get_transaction_by_hash(transaction_hash)
        except Exception as e:
            raise CustomException(self.CLASS_NAME, "does_transaction_exist_by_hash", str(e)) from e

    # Event topic constants (topic0)
    INTENT_CREATED = "0xd802f2610d0c85b3f19be4413f3cf49de1d4e787edecd538274437a5b9aa648d"
    FULFILLMENT = "0x4a817ec64beb8020b3e400f30f3b458110d5765d7a9d1ace4e68754ed2d082de"

    def handle_events(self, blockchain: str, start_block: int, end_block: int, contract: str, topics: List[str], events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        included = []
        for event in events:
            try:
                t = event.get("topic")
                if t == self.INTENT_CREATED:
                    obj = self.handle_intent_created(blockchain, event)
                elif t == self.FULFILLMENT:
                    obj = self.handle_fulfillment(blockchain, event)
                else:
                    obj = None
                if obj:
                    included.append(event)
            except CustomException as e:
                log_error(self.bridge, str(e))
        return included

    def _map_chain_name(self, chain_id_int: int | None) -> str | None:
        if chain_id_int is None:
            return None
        for cid, meta in BLOCKCHAIN_IDS.items():
            if cid.isdigit() and int(cid) == chain_id_int:
                return meta.get("name")
        return None

    def handle_intent_created(self, blockchain: str, event: Dict[str, Any]):
        # Normalize keys: event["hash"] is bytes32; store 0x-prefixed lower
        intent_hash = event.get("hash")
        if isinstance(intent_hash, str) and not intent_hash.startswith("0x") and len(intent_hash) == 64:
            intent_hash = "0x" + intent_hash
        if self.intent_created_repo.event_exists(intent_hash):
            return None
        self.intent_created_repo.create({
            "blockchain": blockchain,
            "transaction_hash": event["transaction_hash"],
            "intent_hash": intent_hash,
            "salt": event.get("salt"),
            "source_chain_id": event.get("source"),
            "destination_chain_id": event.get("destination"),
            "inbox": event.get("inbox"),
            "creator": event.get("creator"),
            "prover": event.get("prover"),
            "deadline": event.get("deadline"),
            "native_value": event.get("nativeValue"),
        })
        return event

    def handle_fulfillment(self, blockchain: str, event: Dict[str, Any]):
        # Normalize _hash
        h = event.get("_hash")
        if isinstance(h, str) and not h.startswith("0x") and len(h) == 64:
            h = "0x" + h
        if self.fulfillment_repo.event_exists(h):
            return None
        self.fulfillment_repo.create({
            "blockchain": blockchain,
            "transaction_hash": event["transaction_hash"],
            "intent_hash": h,
            "source_chain_id": event.get("_sourceChainID"),
            "prover": event.get("_prover"),
            "claimant": event.get("_claimant"),
        })
        return event
