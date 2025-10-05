from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException

TOKEN_DEPOSIT_AND_SWAP = "0x79c15604b92ef54d3f61f0c40caab8857927ca3d5092367163b4562c1699eb5f"
TOKEN_MINT_AND_SWAP = "0x4f56ec39e98539920503fd54ee56ae0cbebe9eb15aa778f18de67701eeae7c65"


class SynapseDecoder(BaseDecoder):
    CLASS_NAME = "SynapseDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"
        t0 = log["topics"][0]
        try:
            if t0 == TOKEN_DEPOSIT_AND_SWAP:
                return contract.events.TokenDepositAndSwap().process_log(log)["args"]
            if t0 == TOKEN_MINT_AND_SWAP:
                return contract.events.TokenMintAndSwap().process_log(log)["args"]
        except Exception as e:
            raise CustomException(self.CLASS_NAME, func_name, f"Error decoding event: {e}") from e

        raise CustomException(self.CLASS_NAME, func_name, f"Unknown event topic: {t0}")
