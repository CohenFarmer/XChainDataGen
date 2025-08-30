from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException

# Event topic constants (topic0) defined in constants.py already
FUNDS_DEPOSITED = "0x6f223106c8e3df857d691613d18d1478cc7c629a1fdf16c7b461d36729fcc7ad"
FUNDS_DEPOSITED_WITH_MESSAGE = "0x3dbc28a2fa93575c89d951d683c45ddb951a2ecf6bc9b9704a61589fa0fcb70f"
IUSDC_DEPOSITED = "0x297a8bc8b87367a63661d6429dbab51be5cefd71ce6a3050fa900a8f276d66d9"
DEPOSIT_INFO_UPDATE = "0x86896302632bf6dc8a3ac0ae7ddf17d5a5d5c1ca1aad37b4b920a587c51135b1"
FUNDS_PAID = "0x0f3ca0b27903ec13ef88a7ea8be837cc19b0d7f71a735f2083215739a8004464"
FUNDS_PAID_WITH_MESSAGE = "0x21937deaa62558dad619c8d730a7d1d7ef41731fc194c32973511e1455cb37ad"

class RouterDecoder(BaseDecoder):
    CLASS_NAME = "RouterDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"
        t0 = log["topics"][0]
        try:
            if t0 == FUNDS_DEPOSITED:
                return contract.events.FundsDeposited().process_log(log)["args"]
            if t0 == FUNDS_DEPOSITED_WITH_MESSAGE:
                return contract.events.FundsDepositedWithMessage().process_log(log)["args"]
            if t0 == IUSDC_DEPOSITED:
                return contract.events.IUSDCDeposited().process_log(log)["args"]
            if t0 == DEPOSIT_INFO_UPDATE:
                return contract.events.DepositInfoUpdate().process_log(log)["args"]
            if t0 == FUNDS_PAID:
                return contract.events.FundsPaid().process_log(log)["args"]
            if t0 == FUNDS_PAID_WITH_MESSAGE:
                return contract.events.FundsPaidWithMessage().process_log(log)["args"]
        except Exception as e:
            raise CustomException(self.CLASS_NAME, func_name, f"Error decoding event: {e}") from e

        raise CustomException(self.CLASS_NAME, func_name, f"Unknown event topic: {t0}")
