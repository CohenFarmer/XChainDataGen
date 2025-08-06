from eth_utils import keccak, to_hex
topic = to_hex(keccak(text="PreSignature(bytes32,bool)"))
print(topic)