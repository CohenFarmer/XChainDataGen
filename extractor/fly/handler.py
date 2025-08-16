from typing import Any, Dict, List

from eth_utils import keccak

from config.constants import Bridge
from extractor.base_handler import BaseHandler
from extractor.fly.constants import BRIDGE_CONFIG
from repository.database import DBSession
from utils.utils import CustomException, convert_bin_to_hex, log_error

from repository.fly.repository import (
	FlyBlockchainTransactionRepository,
	FlyDepositRepository,
	FlySwapInRepository,
	FlySwapOutRepository,
)


class FlyHandler(BaseHandler):
	CLASS_NAME = "FlyHandler"

	def __init__(self, rpc_client, blockchains: list) -> None:
		super().__init__(rpc_client, blockchains)
		self.bridge = Bridge.FLY

	def get_bridge_contracts_and_topics(self, bridge: str, blockchain: List[str]) -> None:
		return super().get_bridge_contracts_and_topics(
			config=BRIDGE_CONFIG,
			bridge=bridge,
			blockchain=blockchain,
		)

	def bind_db_to_repos(self):
		if FlyBlockchainTransactionRepository is None:
			return
		self.blockchain_transaction_repo = FlyBlockchainTransactionRepository(DBSession)
		self.fly_swap_in_repo = FlySwapInRepository(DBSession)
		self.fly_swap_out_repo = FlySwapOutRepository(DBSession)
		self.fly_deposit_repo = FlyDepositRepository(DBSession)

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
				if event["topic"] == "0x37600fc06910ae05ad532c02a9de91251b21674999c33c6e6da90271029bfa23":
					ev = self.handle_swap_in(blockchain, event)
				elif event["topic"] == "0x13d672f2c19bbdf5ce8c9c4894d9586248592fd27d555c2c03ac5e49d219f45d":
					ev = self.handle_swap_out(blockchain, event)
				elif event["topic"] == "0x98e783c3864bbf744a057ef605a2a61701c3b62b5ed68b3745b99094497daf1f":
					ev = self.handle_deposit(blockchain, event)
				else:
					ev = None

				if ev:
					included_events.append(ev)
			except CustomException as e:
				request_desc = (
					f"Error processing request: {blockchain}, {start_block}, {end_block}, {contract}, {topics}.\n{e}"
				)
				log_error(self.bridge, request_desc)

		return included_events

	def _compute_deposit_hash_from_encoded(self, encoded: bytes | str) -> str:
		if isinstance(encoded, str):
			try:
				data = bytes.fromhex(encoded[2:] if encoded.startswith("0x") else encoded)
			except Exception:
				data = encoded.encode("utf-8")
		else:
			data = encoded
		return keccak(data).hex()

	def handle_swap_in(self, blockchain: str, event: Dict[str, Any]):
		func_name = "handle_swap_in"

		try:
			if self.fly_swap_in_repo.event_exists(event["transaction_hash"]):
				return None

			encoded = event.get("encodedDepositData")
			deposit_hash = self._compute_deposit_hash_from_encoded(encoded) if encoded is not None else None

			self.fly_swap_in_repo.create(
				{
					"blockchain": blockchain,
					"transaction_hash": event["transaction_hash"],
					"from_address": event["fromAddress"],
					"to_address": event["toAddress"],
					"from_asset_address": event["fromAssetAddress"],
					"to_asset_address": event["toAssetAddress"],
					"amount_in": str(event["amountIn"]),
					"amount_out": str(event["amountOut"]),
					"encoded_deposit_data": convert_bin_to_hex(encoded) if isinstance(encoded, (bytes, bytearray)) else encoded,
					"deposit_data_hash": deposit_hash,
				}
			)
			return event
		except Exception as e:
			raise CustomException(
				self.CLASS_NAME,
				func_name,
				f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
			) from e

	def handle_swap_out(self, blockchain: str, event: Dict[str, Any]):
		func_name = "handle_swap_out"
		try:
			if self.fly_swap_out_repo.event_exists(event["transaction_hash"]):
				return None

			self.fly_swap_out_repo.create(
				{
					"blockchain": blockchain,
					"transaction_hash": event["transaction_hash"],
					"from_address": event["fromAddress"],
					"to_address": event["toAddress"],
					"from_asset_address": event["fromAssetAddress"],
					"to_asset_address": event["toAssetAddress"],
					"amount_in": str(event["amountIn"]),
					"amount_out": str(event["amountOut"]),
					"deposit_data_hash": event.get("depositDataHash"),
				}
			)
			return event
		except Exception as e:
			raise CustomException(
				self.CLASS_NAME,
				func_name,
				f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
			) from e

	def handle_deposit(self, blockchain: str, event: Dict[str, Any]):
		func_name = "handle_deposit"
		try:
			if self.fly_deposit_repo.event_exists(event.get("depositDataHash")):
				return None

			self.fly_deposit_repo.create(
				{
					"blockchain": blockchain,
					"transaction_hash": event["transaction_hash"],
					"deposit_data_hash": event.get("depositDataHash"),
					"amount": str(event.get("amount")) if event.get("amount") is not None else None,
				}
			)
			return event
		except Exception as e:
			raise CustomException(
				self.CLASS_NAME,
				func_name,
				f"{blockchain} -- Tx Hash: {event['transaction_hash']}. Error writing to DB: {e}",
			) from e

