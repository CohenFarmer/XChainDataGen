"""
reference:
    bytes32 messageHash = keccak256(
        abi.encode(
            relayData.amount,
            relayData.srcChainId,
            relayData.depositId,
            relayData.destToken,
            relayData.recipient,
            address(this)
        )
    );
"""
from __future__ import annotations

from typing import Union
from eth_abi import encode as abi_encode  # web3 dependency
from web3 import Web3


def _normalize_address(addr: str) -> str:
    if not isinstance(addr, str):
        raise TypeError("Address must be string")
    if not addr.startswith("0x"):
        raise ValueError("Address must start with 0x")
    if len(addr) != 42:
        raise ValueError(f"Address length mismatch: {addr}")
    return Web3.to_checksum_address(addr)


def to_bytes32_chain_id(value: Union[int, str, bytes]) -> bytes:
    """Convert a chain/domain id representation into the bytes32 used on-chain.

    If value is int -> big-endian uint256 padded to 32 bytes.
    If hex string (0x...) of length <= 66 -> interpreted as hex bytes and left-padded to 32.
    If already bytes32 -> returned as-is (after length check / padding).
    """
    if isinstance(value, int):
        if value < 0:
            raise ValueError("Negative chain id not allowed")
        return value.to_bytes(32, byteorder="big")
    if isinstance(value, bytes):
        if len(value) > 32:
            raise ValueError("bytes longer than 32")
        return value.rjust(32, b"\x00")
    if isinstance(value, str):
        if value.startswith("0x"):
            raw = bytes.fromhex(value[2:])
            if len(raw) > 32:
                raise ValueError("hex too long for bytes32")
            return raw.rjust(32, b"\x00")
        as_int = int(value)
        return as_int.to_bytes(32, byteorder="big")
    raise TypeError("Unsupported chain id type")


def to_ascii_bytes32_chain_id(chain_id: Union[int, str]) -> bytes:
    """Encode chain id as ASCII decimal left-aligned then null padded to 32 bytes.

    If provided hex string (0x..), convert to int first. Ensures <=32 bytes.
    """
    if isinstance(chain_id, str):
        if chain_id.startswith("0x"):
            chain_id = int(chain_id, 16)
        else:
            # accept decimal
            chain_id = int(chain_id)
    elif not isinstance(chain_id, int):
        raise TypeError("chain_id must be int or str")
    if chain_id < 0:
        raise ValueError("Negative chain id not allowed")
    s = str(chain_id).encode("ascii")
    if len(s) > 32:
        raise ValueError("ASCII chain id longer than 32 bytes")
    return s + b"\x00" * (32 - len(s))


def compute_message_hash(
    amount: int,
    src_chain_id_bytes32: bytes,
    deposit_id: int,
    dest_token: str,
    recipient: str,
    destination_contract: str,
) -> str:
    if len(src_chain_id_bytes32) != 32:
        raise ValueError("src_chain_id_bytes32 must be exactly 32 bytes")
    dest_token_cs = _normalize_address(dest_token)
    recipient_cs = _normalize_address(recipient)
    destination_cs = _normalize_address(destination_contract)

    encoded = abi_encode(
        ["uint256", "bytes32", "uint256", "address", "address", "address"],
        [amount, src_chain_id_bytes32, deposit_id, dest_token_cs, recipient_cs, destination_cs],
    )
    return Web3.to_hex(Web3.keccak(encoded))


def compute_message_hash_packed(
    amount: int,
    src_chain_id: int | str | int,
    deposit_id: int,
    dest_token: str,
    recipient: str,
    destination_contract: str,
) -> str:
    """Alternative hash if the contract used keccak256(abi.encodePacked(...)).

    Layout (packed / solidityKeccak types):
        uint256 amount
        uint256 srcChainId (numeric)
        uint256 depositId
        address destToken
        address recipient
        address this (destination contract)

    Only use this if you confirm the Solidity code uses abi.encodePacked with those
    exact types/order. Otherwise prefer compute_message_hash (abi.encode + bytes32 srcChainId).
    """
    dest_token_cs = _normalize_address(dest_token)
    recipient_cs = _normalize_address(recipient)
    destination_cs = _normalize_address(destination_contract)
    if isinstance(src_chain_id, str):
        # allow decimal or hex
        if src_chain_id.startswith("0x"):
            src_chain_id_int = int(src_chain_id, 16)
        else:
            src_chain_id_int = int(src_chain_id)
    else:
        src_chain_id_int = int(src_chain_id)
    return Web3.to_hex(
        Web3.solidity_keccak(
            ["uint256", "uint256", "uint256", "address", "address", "address"],
            [amount, src_chain_id_int, deposit_id, dest_token_cs, recipient_cs, destination_cs],
        )
    )


__all__ = [
    "compute_message_hash",
    "to_bytes32_chain_id",
    "compute_message_hash_packed",
    "to_ascii_bytes32_chain_id",
]
