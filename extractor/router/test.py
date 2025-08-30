from eth_abi import encode
from eth_utils import keccak
from web3 import Web3


def ascii_chain_id_bytes32(chain_id: int | str) -> bytes:
    if isinstance(chain_id, str):
        if chain_id.startswith("0x"):
            chain_id = int(chain_id, 16)
        else:
            chain_id = int(chain_id)
    s = str(chain_id).encode()
    if len(s) > 32:
        raise ValueError("ASCII chain id exceeds 32 bytes")
    return s + b"\x00" * (32 - len(s))


def numeric_chain_id_bytes32(chain_id: int | str) -> bytes:
    if isinstance(chain_id, str):
        chain_id = int(chain_id, 0)
    return int(chain_id).to_bytes(32, byteorder="big")


def solidity_keccak_packed(amount, src_chain_id_int, deposit_id, dest_token, recipient, forwarder):
    return Web3.solidity_keccak(
        ["uint256", "uint256", "uint256", "address", "address", "address"],
        [amount, int(src_chain_id_int), deposit_id, dest_token, recipient, forwarder]
    )


SAMPLE_AMOUNT = 204847482445445254
SAMPLE_SRC_CHAIN_ID = 42161
SAMPLE_DEPOSIT_ID = 468794
SAMPLE_DEST_TOKEN = Web3.to_checksum_address("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE")
SAMPLE_RECIPIENT = Web3.to_checksum_address("0x8857acc3a823277632Bf1EC51B1b58B87dF50F53")
FORWARDER_ADDRESS = Web3.to_checksum_address("0xc21e4ebd1d92036cb467b53fe3258f219d909eb9")



def compute_message_hash():
    ascii_b32 = ascii_chain_id_bytes32(SAMPLE_SRC_CHAIN_ID)
    numeric_b32 = numeric_chain_id_bytes32(SAMPLE_SRC_CHAIN_ID)

    encoded_ascii = encode(
        ["uint256", "bytes32", "uint256", "address", "address", "address"],
        [SAMPLE_AMOUNT, ascii_b32, SAMPLE_DEPOSIT_ID, SAMPLE_DEST_TOKEN, SAMPLE_RECIPIENT, FORWARDER_ADDRESS]
    )
    hash_ascii = keccak(encoded_ascii)

    encoded_numeric = encode(
        ["uint256", "bytes32", "uint256", "address", "address", "address"],
        [SAMPLE_AMOUNT, numeric_b32, SAMPLE_DEPOSIT_ID, SAMPLE_DEST_TOKEN, SAMPLE_RECIPIENT, FORWARDER_ADDRESS]
    )
    hash_numeric = keccak(encoded_numeric)

    packed_hash = solidity_keccak_packed(
        SAMPLE_AMOUNT, SAMPLE_SRC_CHAIN_ID, SAMPLE_DEPOSIT_ID, SAMPLE_DEST_TOKEN, SAMPLE_RECIPIENT, FORWARDER_ADDRESS
    )

    print("Amount:", SAMPLE_AMOUNT)
    print("Src chain id (int):", SAMPLE_SRC_CHAIN_ID)
    print("ASCII bytes32 srcChainId:", Web3.to_hex(ascii_b32))
    print("Numeric bytes32 srcChainId:", Web3.to_hex(numeric_b32))
    print("Dest token:", SAMPLE_DEST_TOKEN)
    print("Recipient:", SAMPLE_RECIPIENT)
    print("Forwarder (address(this)):", FORWARDER_ADDRESS)
    print()
    print("keccak256(abi.encode(...)) with ASCII srcChainId  =>", Web3.to_hex(hash_ascii))
    print("keccak256(abi.encode(...)) with numeric srcChainId =>", Web3.to_hex(hash_numeric))
    print("keccak256(abi.encodePacked(...)) variant          =>", Web3.to_hex(packed_hash))
    print()
    print("NOTE: Choose the one matching the on-chain FundsPaid messageHash; expected is likely the ASCII abi.encode version.")


if __name__ == "__main__":
    compute_message_hash()
