from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class FlyDecoder(BaseDecoder):
	CLASS_NAME = "FlyDecoder"

	def __init__(self):
		super().__init__()

	def decode_event(self, contract: Contract, log: dict):
		func_name = "decode_event"

		if log["topics"][0] == "0x37600fc06910ae05ad532c02a9de91251b21674999c33c6e6da90271029bfa23":
			return contract.events.SwapIn().process_log(log)["args"]
		elif log["topics"][0] == "0x13d672f2c19bbdf5ce8c9c4894d9586248592fd27d555c2c03ac5e49d219f45d":
			return contract.events.SwapOut().process_log(log)["args"]
		elif log["topics"][0] == "0x98e783c3864bbf744a057ef605a2a61701c3b62b5ed68b3745b99094497daf1f":
			return contract.events.Deposit().process_log(log)["args"]

		raise CustomException(
			self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
		)

