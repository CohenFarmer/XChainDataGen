from sqlalchemy import BigInteger, Column, Float, Integer, LargeBinary, Numeric, String, Index

from repository.common.models import BlockchainTransaction
from repository.database import Base


class WormholePublished(Base):
    __tablename__ = "wormhole_published"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(16), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    block_number = Column(BigInteger, nullable=False)
    sender = Column(String(42), nullable=False)  # Token Bridge proxy on src
    sequence = Column(Numeric(40, 0), nullable=False)
    nonce = Column(Numeric(40, 0), nullable=True)
    payload = Column(String, nullable=False)  # hex string
    consistency_level = Column(Integer, nullable=True)
    emitter_address_32 = Column(String(66), nullable=False)  # bytes32 left-padded sender
    emitter_chain_id = Column(Integer, nullable=False)  # Wormhole chain id
    amount = Column(Numeric(30, 0), nullable=True)  # extracted from payload for VAA types 1 and 3


class WormholeRedeemed(Base):
    __tablename__ = "wormhole_redeemed"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(16), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    block_number = Column(BigInteger, nullable=False)
    emitter_chain_id = Column(Integer, nullable=False)
    emitter_address_32 = Column(String(66), nullable=False)
    sequence = Column(Numeric(40, 0), nullable=False)


class WormholeBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "wormhole_blockchain_transactions"


Index("ix_wh_pub_tx", WormholePublished.transaction_hash)
Index("ix_wh_pub_seq", WormholePublished.sequence)
Index("ix_wh_pub_key", WormholePublished.emitter_chain_id, WormholePublished.emitter_address_32, WormholePublished.sequence)
Index("ix_wh_red_tx", WormholeRedeemed.transaction_hash)
Index("ix_wh_red_key", WormholeRedeemed.emitter_chain_id, WormholeRedeemed.emitter_address_32, WormholeRedeemed.sequence)


class WormholeCrossChainTransaction(Base):
    __tablename__ = "wormhole_cross_chain_transactions"

    id = Column(BigInteger, nullable=False, autoincrement=True, primary_key=True)

    emitter_chain_id = Column(Integer, nullable=False)
    emitter_address_32 = Column(String(66), nullable=False)
    sequence = Column(Numeric(40, 0), nullable=False)

    src_blockchain = Column(String(16), nullable=False)
    src_transaction_hash = Column(String(66), nullable=False)
    src_from_address = Column(String(42), nullable=False)
    src_to_address = Column(String(42), nullable=False)
    src_fee = Column(Numeric(30, 0), nullable=False)
    src_fee_usd = Column(Float, nullable=True)
    src_timestamp = Column(BigInteger, nullable=False)
    src_date = Column(String(10), nullable=True)

    dst_blockchain = Column(String(16), nullable=False)
    dst_transaction_hash = Column(String(66), nullable=False)
    dst_from_address = Column(String(42), nullable=False)
    dst_to_address = Column(String(42), nullable=False)
    dst_fee = Column(Numeric(30, 0), nullable=False)
    dst_fee_usd = Column(Float, nullable=True)
    dst_timestamp = Column(BigInteger, nullable=False)
    dst_date = Column(String(10), nullable=True)

    src_contract_address = Column(String(42), nullable=False)
    dst_contract_address = Column(String(42), nullable=False)

    input_amount = Column(Numeric(30, 0), nullable=True)
    input_amount_usd = Column(Float, nullable=True)
    output_amount = Column(Numeric(30, 0), nullable=True)
    output_amount_usd = Column(Float, nullable=True)


Index("ix_wh_cctx_src_tx", WormholeCrossChainTransaction.src_transaction_hash)
Index("ix_wh_cctx_dst_tx", WormholeCrossChainTransaction.dst_transaction_hash)
Index(
    "ix_wh_cctx_join",
    WormholeCrossChainTransaction.emitter_chain_id,
    WormholeCrossChainTransaction.emitter_address_32,
    WormholeCrossChainTransaction.sequence,
)
