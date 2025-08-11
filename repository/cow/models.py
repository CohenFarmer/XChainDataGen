from sqlalchemy import BigInteger, Column, Float, Integer, Numeric, String, UniqueConstraint, Index

from repository.common.models import BlockchainTransaction
from repository.database import Base

class CowTrade(Base):
    __tablename__ = "cow_trade"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(66), nullable=False)
    transaction_hash = Column(String(256), nullable=False)
    trade_id = Column(String(256), nullable=False)
    owner = Column(String(42), nullable=False)
    sell_token = Column(String(42), nullable=False)
    buy_token = Column(String(42), nullable=False)
    sell_amount = Column(Numeric(30, 0), nullable=False)
    buy_amount = Column(Numeric(30, 0), nullable=False)
    fee_amount = Column(Numeric(30, 0), nullable=False)
    log_index = Column(BigInteger, nullable=False)
    contract_address = Column(String(42), nullable=False)
    block_number = Column(BigInteger, nullable=False)
    valid_to = Column(BigInteger, nullable=False)
    app_data = Column(String, nullable=True)
    app_data_cid = Column(String, nullable=True)
    cross_chain_key = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("blockchain", "trade_id", name="uq_cow_trade_chain_trade_id"),
        Index("ix_cow_trade_cross_chain_key", "cross_chain_key"),
        Index("ix_cow_trade_blockchain_trade_id", "blockchain", "trade_id"),
        Index("ix_cow_trade_tx_hash", "transaction_hash"),
    )

    def __init__(
        self,
        blockchain,
        transaction_hash,
        trade_id,
        owner,
        sell_token,
        buy_token,
        sell_amount,
        buy_amount,
        fee_amount,
        log_index,
        contract_address,
        block_number,
        valid_to,
        app_data=None,
        app_data_cid=None,
        cross_chain_key=None
    ):
        self.blockchain = blockchain
        self.transaction_hash = transaction_hash
        self.trade_id = trade_id
        self.owner = owner
        self.sell_token = sell_token
        self.buy_token = buy_token
        self.sell_amount = sell_amount
        self.buy_amount = buy_amount
        self.fee_amount = fee_amount
        self.contract_address = contract_address
        self.log_index = log_index
        self.block_number = block_number
        self.valid_to = valid_to
        self.app_data = app_data
        self.app_data_cid = app_data_cid
        self.cross_chain_key = cross_chain_key

    def __repr__(self):
        return (
            f"<CowTrade(blockchain={self.blockchain}, "
            f"trade_id={self.trade_id}, owner={self.owner}, "
            f"sell_token={self.sell_token}, buy_token={self.buy_token}, "
            f"sell_amount={self.sell_amount}, buy_amount={self.buy_amount}, "
            f"fee_amount={self.fee_amount})>"
        )
    
class CowBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "cow_blockchain_transactions"

    def __repr__(self):
        return (
            f"<CowBlockchainTransaction(blockchain={self.blockchain}, "
            f"transaction_hash={self.transaction_hash}, block_number={self.block_number})>"
        )
    
class CowCrossChainTransaction(Base):
    __tablename__ = "cow_cross_chain_transactions"

    id = Column(BigInteger, nullable=False, autoincrement=True, primary_key=True)
    src_blockchain = Column(String(66), nullable=False)
    src_transaction_hash = Column(String(256), nullable=False)
    src_owner = Column(String(42), nullable=False)
    src_fee = Column(Numeric(30, 0), nullable=True)
    src_fee_usd = Column(Float, nullable=True)

    dst_blockchain = Column(String(66), nullable=False)
    dst_transaction_hash = Column(String(256), nullable=False)
    dst_owner = Column(String(42), nullable=False)
    dst_fee = Column(Numeric(30, 0), nullable=True)
    dst_fee_usd = Column(Float, nullable=True)

    trade_id = Column(String(256), nullable=False)
    sell_token = Column(String(42), nullable=False)
    buy_token = Column(String(42), nullable=False)
    sell_amount = Column(Numeric(30, 0), nullable=False)
    sell_amount_usd = Column(Float, nullable=True)
    buy_amount = Column(Numeric(30, 0), nullable=False)
    buy_amount_usd = Column(Float, nullable=True)
    src_valid_to = Column(BigInteger, nullable=False)
    dst_valid_to = Column(BigInteger, nullable=False)

    __table_args__ = (
        UniqueConstraint("trade_id", "src_blockchain", "dst_blockchain", name="uq_cow_cctx_triplet"),
        Index("ix_cow_cctx_src_tx_hash", "src_transaction_hash"),
        Index("ix_cow_cctx_dst_tx_hash", "dst_transaction_hash"),
    )

    def __init__(
        self,
        src_blockchain,
        src_transaction_hash,
        src_owner,
        src_fee,
        src_fee_usd,
        dst_blockchain,
        dst_transaction_hash,
        dst_owner,
        dst_fee,
        dst_fee_usd,
        trade_id,
        sell_token,
        buy_token,
        sell_amount,
        sell_amount_usd,
        buy_amount,
        buy_amount_usd,
        src_valid_to,
        dst_valid_to,
    ):
        self.src_blockchain = src_blockchain
        self.src_transaction_hash = src_transaction_hash
        self.src_owner = src_owner
        self.src_fee = src_fee
        self.src_fee_usd = src_fee_usd
        self.dst_blockchain = dst_blockchain
        self.dst_transaction_hash = dst_transaction_hash
        self.dst_owner = dst_owner
        self.dst_fee = dst_fee
        self.dst_fee_usd = dst_fee_usd
        self.trade_id = trade_id
        self.sell_token = sell_token
        self.buy_token = buy_token
        self.sell_amount = sell_amount
        self.sell_amount_usd = sell_amount_usd
        self.buy_amount = buy_amount
        self.buy_amount_usd = buy_amount_usd
        self.src_valid_to = src_valid_to
        self.dst_valid_to = dst_valid_to

    def __repr__(self):
        return (
            f"<CowCrossChainTransaction(src_blockchain={self.src_blockchain}, "
            f"dst_blockchain={self.dst_blockchain}, trade_id={self.trade_id}, "
            f"src_owner={self.src_owner}, sell_token={self.sell_token}, buy_token={self.buy_token}, "
            f"sell_amount={self.sell_amount}, buy_amount={self.buy_amount})>"
        )