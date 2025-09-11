from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException

# Explicit topic0 hashes for ECO events we care about
# Intent contract events
INTENT_CREATED = "0xd802f2610d0c85b3f19be4413f3cf49de1d4e787edecd538274437a5b9aa648d"
INTENT_FUNDED = "0x2da42efda5225344c30e729dc0eafc2e56292ac9b9b5c2b16e0e74c86ea5921d"
WITHDRAWAL = "0x6653a45d3871e4110fa55dac0269f9f93a6d9078d402f7153594e50573d7f0cd"

# Inbox contract events
FULFILLMENT = "0x4a817ec64beb8020b3e400f30f3b458110d5765d7a9d1ace4e68754ed2d082de"


class EcoDecoder(BaseDecoder):
    CLASS_NAME = "EcoDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"
        t0 = log["topics"][0]
        try:
            # Intent contract
            if t0 == INTENT_CREATED:
                return contract.events.IntentCreated().process_log(log)["args"]
            if t0 == INTENT_FUNDED:
                #not used for joins but decoded for completeness
                return contract.events.IntentFunded().process_log(log)["args"]
            if t0 == WITHDRAWAL:
                #not used directly, but included since it's filtered in topics
                return contract.events.Withdrawal().process_log(log)["args"]

            #inbox contract
            if t0 == FULFILLMENT:
                return contract.events.Fulfillment().process_log(log)["args"]
        except Exception as e:
            raise CustomException(self.CLASS_NAME, func_name, f"Error decoding event: {e}") from e

        raise CustomException(self.CLASS_NAME, func_name, f"Unknown event topic: {t0}")
