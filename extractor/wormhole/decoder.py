from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class WormholeDecoder(BaseDecoder):
    CLASS_NAME = "WormholeDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        topic0 = log["topics"][0]
        # LogMessagePublished
        if topic0 == "0x6eb224fb001ed210e379b335e35efe88672a8ce935d981a6896b27ffdf52a3b2":
            return contract.events.LogMessagePublished().process_log(log)["args"]
        # TransferRedeemed
        if topic0 == "0xcaf280c8cfeba144da67230d9b009c8f868a75bac9a528fa0474be1ba317c169":
            return contract.events.TransferRedeemed().process_log(log)["args"]

        raise CustomException(self.CLASS_NAME, "decode_event", f"Unknown event topic: {topic0}")
