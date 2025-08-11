from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class CowDecoder(BaseDecoder):
    CLASS_NAME = "CowDecoder"

    def __init__(self):
        super().__init__()

    def _to_0x_hex(self, v):
        if v is None:
            return None
        if hasattr(v, "hex"):
            h = v.hex()
            return f"0x{h}" if not h.startswith("0x") else h
        s = str(v)
        return s if s.startswith("0x") else f"0x{s}"

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"
        topic = log["topics"][0]
        if topic == "0xa07a543ab8a018198e99ca0184c93fe9050a79400a0a723441f84de1d972cc17":
            processed = contract.events.Trade().process_log(log)
            args = dict(processed["args"])

            args["transactionHash"] = self._to_0x_hex(log.get("transactionHash"))
            args["logIndex"] = log.get("logIndex")
            args["contractAddress"] = log.get("address")
            args["blockNumber"] = log.get("blockNumber")

            return args

        raise CustomException(
            self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
        )