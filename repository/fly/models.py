from sqlalchemy import BigInteger, Column, Float, Integer, Numeric, String, Index

from repository.common.models import BlockchainTransaction
from repository.database import Base


class FlySwapIn(Base):
    __tablename__ = "fly_swap_in"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    from_address = Column(String(42), nullable=False)
    to_address = Column(String(42), nullable=False)
    from_asset_address = Column(String(42), nullable=False)
    to_asset_address = Column(String(42), nullable=False)
    amount_in = Column(Numeric(30, 0), nullable=False)
    amount_out = Column(Numeric(30, 0), nullable=False)
    encoded_deposit_data = Column(String, nullable=True)
    deposit_data_hash = Column(String(66), nullable=True)

    def __repr__(self):
        return (
            f"<FlySwapIn(blockchain={self.blockchain}, tx={self.transaction_hash}, "
            f"from={self.from_address}, to={self.to_address}, amount_in={self.amount_in}, "
            f"amount_out={self.amount_out}, deposit_hash={self.deposit_data_hash})>"
        )


class FlySwapOut(Base):
    __tablename__ = "fly_swap_out"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    from_address = Column(String(42), nullable=False)
    to_address = Column(String(42), nullable=False)
    from_asset_address = Column(String(42), nullable=False)
    to_asset_address = Column(String(42), nullable=False)
    amount_in = Column(Numeric(30, 0), nullable=False)
    amount_out = Column(Numeric(30, 0), nullable=False)
    deposit_data_hash = Column(String(66), nullable=True)

    def __repr__(self):
        return (
            f"<FlySwapOut(blockchain={self.blockchain}, tx={self.transaction_hash}, "
            f"from={self.from_address}, to={self.to_address}, amount_in={self.amount_in}, "
            f"amount_out={self.amount_out}, deposit_hash={self.deposit_data_hash})>"
        )


class FlyDeposit(Base):
    __tablename__ = "fly_deposit"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(10), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    deposit_data_hash = Column(String(66), nullable=False)
    amount = Column(Numeric(30, 0), nullable=True)

    def __repr__(self):
        return (
            f"<FlyDeposit(blockchain={self.blockchain}, tx={self.transaction_hash}, "
            f"deposit_hash={self.deposit_data_hash}, amount={self.amount})>"
        )


class FlyBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "fly_blockchain_transactions"

    def __repr__(self):
        return (
            f"<FlyBlockchainTransaction(blockchain={self.blockchain}, tx={self.transaction_hash}, "
            f"block={self.block_number}, timestamp={self.timestamp})>"
        )


class FlyCrossChainTransaction(Base):
    __tablename__ = "fly_cross_chain_transactions"

    id = Column(BigInteger, nullable=False, autoincrement=True, primary_key=True)

    deposit_data_hash = Column(String(66), nullable=False)

    src_blockchain = Column(String(10), nullable=False)
    src_transaction_hash = Column(String(66), nullable=False)
    src_from_address = Column(String(42), nullable=False)
    src_to_address = Column(String(42), nullable=False)
    src_fee = Column(Numeric(30, 0), nullable=False)
    src_fee_usd = Column(Float, nullable=True)
    src_timestamp = Column(BigInteger, nullable=False)
    src_date = Column(String(10), nullable=True)

    dst_blockchain = Column(String(10), nullable=False)
    dst_transaction_hash = Column(String(66), nullable=False)
    dst_from_address = Column(String(42), nullable=False)
    dst_to_address = Column(String(42), nullable=False)
    dst_fee = Column(Numeric(30, 0), nullable=False)
    dst_fee_usd = Column(Float, nullable=True)
    dst_timestamp = Column(BigInteger, nullable=False)
    dst_date = Column(String(10), nullable=True) 

    src_contract_address = Column(String(42), nullable=False)
    dst_contract_address = Column(String(42), nullable=False)

    input_amount = Column(Numeric(30, 0), nullable=False)
    input_amount_usd = Column(Float, nullable=True)
    output_amount = Column(Numeric(30, 0), nullable=False)
    output_amount_usd = Column(Float, nullable=True)

    def __repr__(self):
        return (
            f"<FlyCrossChainTransaction(src_blockchain={self.src_blockchain}, "
            f"dst_blockchain={self.dst_blockchain}, deposit_hash={self.deposit_data_hash}, "
            f"input_amount={self.input_amount}, output_amount={self.output_amount})>"
        )


Index("ix_fly_swap_in_tx", FlySwapIn.transaction_hash)
Index("ix_fly_swap_in_hash", FlySwapIn.deposit_data_hash)
Index("ix_fly_swap_out_tx", FlySwapOut.transaction_hash)
Index("ix_fly_swap_out_hash", FlySwapOut.deposit_data_hash)
Index("ix_fly_deposit_tx", FlyDeposit.transaction_hash)
Index("ix_fly_deposit_hash", FlyDeposit.deposit_data_hash)
Index("ix_fly_cctx_src_tx", FlyCrossChainTransaction.src_transaction_hash)
Index("ix_fly_cctx_dst_tx", FlyCrossChainTransaction.dst_transaction_hash)
Index("ix_fly_cctx_hash", FlyCrossChainTransaction.deposit_data_hash)
