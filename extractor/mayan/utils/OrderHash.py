import struct

import base58
from eth_utils import keccak


def reconstruct_order_hash(
    trader: str,
    src_chain_id: int,
    token_in: str,
    dest_chain_id: int,
    token_out: str,
    min_amount_out64: int,
    gas_drop64: int,
    refund_fee_dest64: int,
    refund_fee_src64: int,
    deadline: int,
    dest_addr: str,
    referrer_addr: str,
    referrer_bps: int,
    mayan_bps: int,
    auction_mode: int,
    random: str,
) -> bytes:
    buffer = bytearray(239)
    offset = 0

    def write(bytes_data):
        nonlocal offset
        buffer[offset : offset + len(bytes_data)] = bytes_data
        offset += len(bytes_data)

    # Placeholder: convert address + chainID to 32-byte array
    trader32 = try_native_to_uint8_array(trader)
    write(trader32)

    write(struct.pack(">H", src_chain_id))

    token_in32 = try_native_to_uint8_array(token_in)
    write(token_in32)

    destination_address32 = try_native_to_uint8_array(dest_addr)
    write(destination_address32)

    write(struct.pack(">H", dest_chain_id))

    token_out32 = try_native_to_uint8_array(token_out)
    write(token_out32)

    write(struct.pack(">Q", min_amount_out64))
    write(struct.pack(">Q", gas_drop64))
    write(struct.pack(">Q", refund_fee_dest64))
    write(struct.pack(">Q", refund_fee_src64))
    write(struct.pack(">Q", deadline))

    referrer_address32 = try_native_to_uint8_array(referrer_addr)
    write(referrer_address32)

    write(struct.pack("B", referrer_bps))
    write(struct.pack("B", mayan_bps))
    write(struct.pack("B", auction_mode))

    random_key32 = hex_to_uint8_array(random)
    write(random_key32)

    if offset != 239:
        raise ValueError("Invalid offset")

    order_hash = keccak(buffer).hex()
    return order_hash


def try_native_to_uint8_array(address: str) -> bytes:
    if address.startswith("0x"):
        # EVM hex address
        addr_bytes = bytes.fromhex(address[2:])
        return addr_bytes.rjust(32, b"\x00")
    else:
        # Solana base58 address
        addr_bytes = base58.b58decode(address)
        if len(addr_bytes) != 32:
            raise ValueError(f"Expected 32-byte Solana address, got {len(addr_bytes)} bytes")
        return addr_bytes


def hex_to_uint8_array(hex_str: str) -> bytes:
    return bytes.fromhex(hex_str.replace("0x", ""))


def reconstruct_order_hash_from_params(
    trader: str, token_in: str, src_chain_id: int, params: dict[str, int | str | list[int]]
) -> str:
    buffer = bytearray(239)
    offset = 0

    def write(bytes_data):
        nonlocal offset
        buffer[offset : offset + len(bytes_data)] = bytes_data
        offset += len(bytes_data)

    # trader address (EVM or Solana, use helper)
    trader32 = try_native_to_uint8_array(trader)
    write(trader32)

    # src_chain_id
    write(struct.pack(">H", src_chain_id))

    # token_in (EVM or Solana, use helper)
    tokenIn32 = try_native_to_uint8_array(token_in)
    write(tokenIn32)

    # destination address (32-byte array of ints)
    write(bytes(params["addrDest"]))

    # dest_chain_id
    write(struct.pack(">H", params["chainDest"]))

    # token_out (32-byte array of ints)
    write(bytes(params["tokenOut"]))

    # min_amount_out
    value_int = int(params["amountOutMin"], 16)
    write(struct.pack(">Q", value_int))

    # gas_drop
    value_int = int(params["gasDrop"], 16)
    write(struct.pack(">Q", value_int))

    # refund_fee_dest
    value_int = int(params["feeCancel"], 16)
    write(struct.pack(">Q", value_int))

    # refund_fee_src
    value_int = int(params["feeRefund"], 16)
    write(struct.pack(">Q", value_int))

    # deadline
    value_int = int(params["deadline"], 16)
    write(struct.pack(">Q", value_int))

    # referrer address (32-byte array of ints)
    write(bytes(params["addrRef"]))

    # referrer_bps
    write(struct.pack("B", params["feeRateRef"]))

    # mayan_bps
    write(struct.pack("B", params["feeRateMayan"]))

    # auction_mode
    write(struct.pack("B", params["auctionMode"]))

    # random_key32 (32-byte array of ints)
    write(bytes(params["keyRnd"]))

    if offset != 239:
        raise ValueError("Invalid offset")

    order_hash = keccak(buffer).hex()
    return order_hash
