from typing import Any, Dict, List

from config.constants import Bridge, BLOCKCHAIN_IDS
from extractor.base_handler import BaseHandler
from extractor.router.constants import BRIDGE_CONFIG
from repository.database import DBSession
from repository.router.repository import (
    RouterBlockchainTransactionRepository,
    RouterDepositInfoUpdateRepository,
    RouterFundsDepositedRepository,
    RouterFundsPaidRepository,
    RouterIUSDCDepositedRepository,
)
from rpcs.evm_rpc_client import EvmRPCClient
from utils.utils import CustomException, log_error
from utils.router_hash import compute_message_hash, to_ascii_bytes32_chain_id

FUNDS_DEPOSITED = "0x6f223106c8e3df857d691613d18d1478cc7c629a1fdf16c7b461d36729fcc7ad"
FUNDS_DEPOSITED_WITH_MESSAGE = "0x3dbc28a2fa93575c89d951d683c45ddb951a2ecf6bc9b9704a61589fa0fcb70f"
IUSDC_DEPOSITED = "0x297a8bc8b87367a63661d6429dbab51be5cefd71ce6a3050fa900a8f276d66d9"
DEPOSIT_INFO_UPDATE = "0x86896302632bf6dc8a3ac0ae7ddf17d5a5d5c1ca1aad37b4b920a587c51135b1"
FUNDS_PAID = "0x0f3ca0b27903ec13ef88a7ea8be837cc19b0d7f71a735f2083215739a8004464"
FUNDS_PAID_WITH_MESSAGE = "0x21937deaa62558dad619c8d730a7d1d7ef41731fc194c32973511e1455cb37ad"

STABLE_TOKENS: dict[str, str] = {
    "ethereum": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "arbitrum": "0xAf88d065e77c8cC2239327C5EDb3A432268e5831",
    "optimism": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
    "polygon": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
    "base": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "bnb": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
    "avalanche": "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
}

TOKEN_DECIMALS: dict[str, int] = {
    "ethereum": 18,
    "arbitrum": 18,
    "optimism": 18,
    "polygon": 18,
    "base": 18,
    "bnb": 6,
    "avalanche": 18,
}
class RouterHandler(BaseHandler):
    CLASS_NAME = "RouterHandler"
    def __init__(self, rpc_client: EvmRPCClient, blockchains: list) -> None:
        super().__init__(rpc_client, blockchains)
        self.bridge = Bridge.ROUTER
    def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]):
        return super().get_bridge_contracts_and_topics(config=BRIDGE_CONFIG, bridge=bridge, blockchain=blockchain)
    def bind_db_to_repos(self):
        self.blockchain_transaction_repo = RouterBlockchainTransactionRepository(DBSession)
        self.router_funds_deposited_repo = RouterFundsDepositedRepository(DBSession)
        self.router_iusdc_deposited_repo = RouterIUSDCDepositedRepository(DBSession)
        self.router_deposit_info_update_repo = RouterDepositInfoUpdateRepository(DBSession)
        self.router_funds_paid_repo = RouterFundsPaidRepository(DBSession)
    def does_transaction_exist_by_hash(self, transaction_hash: str) -> Any:
        try:
            return self.blockchain_transaction_repo.get_transaction_by_hash(transaction_hash)
        except Exception as e:
            raise CustomException(self.CLASS_NAME, "does_transaction_exist_by_hash", str(e)) from e
    def handle_events(self, blockchain: str, start_block: int, end_block: int, contract: str, topics: List[str], events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        included = []
        for event in events:
            try:
                t = event["topic"]
                if t in (FUNDS_DEPOSITED, FUNDS_DEPOSITED_WITH_MESSAGE):
                    obj = self.handle_funds_deposited(blockchain, event, t == FUNDS_DEPOSITED_WITH_MESSAGE)
                elif t == IUSDC_DEPOSITED:
                    obj = self.handle_iusdc_deposited(blockchain, event)
                elif t == DEPOSIT_INFO_UPDATE:
                    obj = self.handle_deposit_info_update(blockchain, event)
                elif t in (FUNDS_PAID, FUNDS_PAID_WITH_MESSAGE):
                    obj = self.handle_funds_paid(blockchain, event, t == FUNDS_PAID_WITH_MESSAGE)
                else:
                    obj = None
                if obj:
                    included.append(event)
            except CustomException as e:
                log_error(self.bridge, str(e))
        return included
    @staticmethod
    def _extract_address(raw: Any) -> str | None:
        if not isinstance(raw, str) or raw == "":
            return None
        s = raw.lower()
        if s.startswith("0x"):
            s = s[2:]
        if not all(c in "0123456789abcdef" for c in s):
            return None
        if len(s) == 64:
            s = s[-40:]
        elif len(s) != 40:
            return None
        return "0x" + s
    @staticmethod
    def _decode_ascii_chain_id(val: str) -> int | None:
        if not isinstance(val, str):
            return None
        h = val[2:] if val.startswith("0x") else val
        if len(h) != 64:
            return None
        try:
            b = bytes.fromhex(h)
        except ValueError:
            return None
        digits = []
        for x in b:
            if x == 0:
                break
            if 48 <= x <= 57:
                digits.append(chr(x))
            else:
                break
        if not digits:
            return None
        try:
            return int("".join(digits))
        except ValueError:
            return None
    def _map_chain_name(self, chain_id_int: int | None) -> str | None:
        if chain_id_int is None:
            return None
        for cid, meta in BLOCKCHAIN_IDS.items():
            if cid.isdigit() and int(cid) == chain_id_int:
                return meta.get("name")
        return None
    def _source_chain_id_int(self, blockchain: str) -> int | None:
        for cid, meta in BLOCKCHAIN_IDS.items():
            if meta.get("name") == blockchain and cid.isdigit():
                return int(cid)
        return None
    def _forwarder(self, chain_name: str) -> str | None:
        cfg = BRIDGE_CONFIG["blockchains"].get(chain_name, [])
        if cfg and cfg[0].get("contracts"):
            lst = cfg[0]["contracts"]
            if lst:
                return lst[0]
        return None
    def handle_funds_deposited(self, blockchain: str, event: Dict[str, Any], has_message: bool):
        if self.router_funds_deposited_repo.event_exists(event["depositId"], has_message):
            return None
        dest_chain_id_int = self._decode_ascii_chain_id(event.get("destChainIdBytes"))
        dest_chain_name = self._map_chain_name(dest_chain_id_int)
        if not dest_chain_name:
            return None
        # Prefer the actual event-provided destination token (if present); fallback to stable token mapping.
        raw_dest_token = event.get("destToken") or event.get("dest_token") or event.get("dest_token_raw")
        dest_token = None
        if isinstance(raw_dest_token, str):
            dest_token = self._extract_address(raw_dest_token)
        if not dest_token:
            dest_token = STABLE_TOKENS.get(dest_chain_name)
        if not dest_token:
            return None
        recipient_addr = self._extract_address(event.get("recipient"))
        message_hash = None
        if recipient_addr:
            fwd = self._forwarder(dest_chain_name)
            if fwd:
                src_chain_id_int = self._source_chain_id_int(blockchain)
                if src_chain_id_int is not None:
                    src_chain_id_bytes32 = to_ascii_bytes32_chain_id(src_chain_id_int)
                    raw_relay_amt = int(event.get("destAmount") or event["amount"])
                    # Scale to 18 decimals only when token has fewer than 18 decimals.
                    dest_decimals = TOKEN_DECIMALS.get(dest_chain_name, 18)
                    if dest_decimals < 18:
                        amount_for_hash = raw_relay_amt * (10 ** (18 - dest_decimals))
                    else:
                        amount_for_hash = raw_relay_amt
                    message_hash = compute_message_hash(amount_for_hash, src_chain_id_bytes32, int(event["depositId"]), dest_token, recipient_addr, fwd)
        self.router_funds_deposited_repo.create({
            "blockchain": blockchain,
            "transaction_hash": event["transaction_hash"],
            "partner_id": event["partnerId"],
            "amount": event["amount"],
            "dest_chain_id_bytes": event["destChainIdBytes"],
            "dest_amount": event.get("destAmount"),
            "deposit_id": event["depositId"],
            "src_token": event["srcToken"],
            "depositor": event["depositor"],
            "recipient_raw": event.get("recipient"),
            "dest_token_raw": dest_token,
            "message": event.get("message"),
            "has_message": has_message,
            "message_hash": message_hash,
        })
        return event
    def handle_iusdc_deposited(self, blockchain: str, event: Dict[str, Any]):
        if self.router_iusdc_deposited_repo.event_exists(event["usdcNonce"]):
            return None
        self.router_iusdc_deposited_repo.create({
            "blockchain": blockchain,
            "transaction_hash": event["transaction_hash"],
            "partner_id": event["partnerId"],
            "amount": event["amount"],
            "dest_chain_id_bytes": event["destChainIdBytes"],
            "usdc_nonce": event["usdcNonce"],
            "src_token": event["srcToken"],
            "recipient": event["recipient"],
            "depositor": event["depositor"],
        })
        return event
    def handle_deposit_info_update(self, blockchain: str, event: Dict[str, Any]):
        if self.router_deposit_info_update_repo.event_exists(event["depositId"], event["eventNonce"]):
            return None
        self.router_deposit_info_update_repo.create({
            "blockchain": blockchain,
            "transaction_hash": event["transaction_hash"],
            "src_token": event["srcToken"],
            "fee_amount": event["feeAmount"],
            "deposit_id": event["depositId"],
            "event_nonce": event["eventNonce"],
            "initiate_withdrawal": event["initiatewithdrawal"],
            "depositor": event["depositor"],
        })
        return event
    def handle_funds_paid(self, blockchain: str, event: Dict[str, Any], has_message: bool):
        if self.router_funds_paid_repo.event_exists(event["messageHash"], has_message):
            return None
        h = event["messageHash"]
        if isinstance(h, str):
            if not h.startswith("0x") and len(h) == 64:
                h = "0x" + h
            elif h.startswith("0x") and len(h) != 66:
                h = h if len(h) == 66 else h[:66]
        self.router_funds_paid_repo.create({
            "blockchain": blockchain,
            "transaction_hash": event["transaction_hash"],
            "message_hash": h,
            "forwarder": event["forwarder"],
            "nonce": event["nonce"],
            "has_message": has_message,
            "exec_flag": event.get("execFlag"),
            "exec_data": event.get("execData"),
        })
        return event