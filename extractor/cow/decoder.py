from web3.contract import Contract

from extractor.base_decoder import BaseDecoder
from utils.utils import CustomException


class CowDecoder(BaseDecoder):
    CLASS_NAME = "CowDecoder"

    def __init__(self):
        super().__init__()

    def decode_event(self, contract: Contract, log: dict):
        func_name = "decode_event"
        if log["topics"][0] == "0x40338ce1a7c49204f0099533b1e9a7ee0a3d261f84974ab7af36105b8c4e9db4":
            return contract.events.Settlement().process_log(log)["args"]
        elif log["topics"][0] == "0xa07a543ab8a018198e99ca0184c93fe9050a79400a0a723441f84de1d972cc17":
            return contract.events.Trade().process_log(log)["args"]
        elif log["topics"][0] == "0xed99827efb37016f2275f98c4bcf71c7551c75d59e9b450f79fa32e60be672c2":
            return contract.events.Interaction().process_log(log)["args"]
        elif log["topics"][0] == "0x7bdff905ec67fa813155a174e73ba3caed0914fd902e9d8fb8626c52d31d9e07":
            return contract.events.PreSignature().process_log(log)["args"]
        elif log["topics"][0] == "0x875b6cb035bbd4ac6500fabc6d1e4ca5bdc58a3e2b424ccb5c24cdbebeb009a9":
            return contract.events.OrderInvalidated().process_log(log)["args"]
        
        raise CustomException(
            self.CLASS_NAME, func_name, f"Unknown event topic: {log['topics'][0]}"
        )