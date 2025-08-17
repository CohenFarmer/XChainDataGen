from typing import Any, Dict, List
import logging

from config.constants import Bridge
from extractor.base_handler import BaseHandler
from extractor.wormhole.constants import BRIDGE_CONFIG
from repository.database import DBSession
from repository.wormhole.repository import (
	WormholeBlockchainTransactionRepository,
	WormholePublishedRepository,
	WormholeRedeemedRepository,
)
from utils.utils import CustomException, convert_bin_to_hex


class WormholeHandler(BaseHandler):
	CLASS_NAME = "WormholeHandler"

	def __init__(self, rpc_client, blockchains: list) -> None:
		super().__init__(rpc_client, blockchains)
		self.bridge = Bridge.WORMHOLE
		self.logger = logging.getLogger("wormhole")

		# Wormhole V2 chain IDs 
		self.WORMHOLE_CHAIN_IDS = {
			"ethereum": 2,
			"bsc": 4,
			"bnb": 4,
			"binance": 4,
			"polygon": 5,
			"avalanche": 6,
			"arbitrum": 23,
			"optimism": 24,
			"base": 30,
			"scroll": 34,
		}

	def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]) -> None:
		return super().get_bridge_contracts_and_topics(
			config=BRIDGE_CONFIG,
			bridge=bridge,
			blockchain=blockchain,
		)

	def bind_db_to_repos(self):
		self.blockchain_transaction_repo = WormholeBlockchainTransactionRepository(DBSession)
		self.published_repo = WormholePublishedRepository(DBSession)
		self.redeemed_repo = WormholeRedeemedRepository(DBSession)

	def handle_transactions(self, transactions: List[Dict[str, Any]]) -> None:
		return super().handle_transactions(transactions)

	def does_transaction_exist_by_hash(self, transaction_hash: str) -> Any:
		return self.blockchain_transaction_repo.get_transaction_by_hash(transaction_hash)

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
				topic0 = event.get("topic")

				# LogMessagePublished(address sender, uint64 sequence, uint32 nonce, bytes payload, uint8 consistencyLevel)
				if topic0 == "0x6eb224fb001ed210e379b335e35efe88672a8ce935d981a6896b27ffdf52a3b2":
					included_events.append(self._handle_published(blockchain, event))

				# TransferRedeemed(uint16 emitterChainId, bytes32 emitterAddress, uint64 sequence)
				elif topic0 == "0xcaf280c8cfeba144da67230d9b009c8f868a75bac9a528fa0474be1ba317c169":
					included_events.append(self._handle_redeemed(blockchain, event))

			except CustomException:
				pass

		return [e for e in included_events if e]

	def _handle_published(self, blockchain: str, event: Dict[str, Any]):
		seq = str(event.get("sequence"))
		if self.published_repo.event_exists(event["transaction_hash"], seq):
			return None

		payload = event.get("payload")
		payload_hex = (
			convert_bin_to_hex(payload) if isinstance(payload, (bytes, bytearray)) else payload
		)

		emitter_chain_id = self._get_wormhole_chain_id(blockchain)
		emitter_address_32 = event.get("emitterAddress")
		if emitter_address_32:
			emitter_address_32 = self._normalize_bytes32_hex(emitter_address_32)
		else:
			emitter_address_32 = self._to_bytes32_address(event.get("sender"))

		self.published_repo.create(
			{
				"blockchain": blockchain,
				"transaction_hash": event["transaction_hash"],
				"block_number": int(event["block_number"], 0)
				if isinstance(event.get("block_number"), str) else int(event.get("block_number")),
				"sender": event.get("sender"),
				"sequence": str(event.get("sequence")),
				"nonce": str(event.get("nonce")) if event.get("nonce") is not None else None,
				"payload": payload_hex,
				"consistency_level": int(event.get("consistencyLevel"))
				if event.get("consistencyLevel") is not None else None,
				"emitter_address_32": emitter_address_32,
				"emitter_chain_id": emitter_chain_id,
			}
		)
		return event

	def _handle_redeemed(self, blockchain: str, event: Dict[str, Any]):
		seq = str(event.get("sequence"))
		if self.redeemed_repo.event_exists(event["transaction_hash"], seq):
			return None

		# Normalize emitterAddress to ensure it has 0x prefix and bytes32 length
		emitter_addr_32 = self._normalize_bytes32_hex(event.get("emitterAddress"))

		self.redeemed_repo.create(
			{
				"blockchain": blockchain,
				"transaction_hash": event["transaction_hash"],
				"block_number": int(event["block_number"], 0)
				if isinstance(event.get("block_number"), str) else int(event.get("block_number")),
				"emitter_chain_id": int(event.get("emitterChainId")),
				"emitter_address_32": emitter_addr_32,
				"sequence": str(event.get("sequence")),
			}
		)
		return event

	def _get_wormhole_chain_id(self, blockchain: str) -> int:
		"""Map local blockchain name to Wormhole chain id, defaulting to 0 with an info log."""
		key = (blockchain or "").lower()
		cid = self.WORMHOLE_CHAIN_IDS.get(key)
		if cid is None:
			self.logger.info(
				"Missing Wormhole chain-id mapping for blockchain '%s'. Writing 0.", key
			)
			return 0
		return cid

	@staticmethod
	def _to_bytes32_address(addr: str | None) -> str | None:
		if not addr:
			return None
		a = addr.lower()
		if a.startswith("0x"):
			a = a[2:]
		if len(a) != 40:
			return None
		return "0x" + ("0" * 24) + a

	@staticmethod
	def _normalize_bytes32_hex(value: str | None) -> str | None:
		"""Ensure a bytes32 hex string has 0x prefix and is lowercased.

		- If 64-nybble hex without prefix, add 0x.
		- If 40-nybble address, left-pad to 32 bytes.
		"""
		if not value:
			return None
		v = value.lower()
		if v.startswith("0x"):
			v = v[2:]
		if len(v) == 64:
			return "0x" + v
		if len(v) == 40:
			return "0x" + ("0" * 24) + v
		if len(v) < 64:
			return "0x" + v.rjust(64, "0")
		return "0x" + v[:64]
