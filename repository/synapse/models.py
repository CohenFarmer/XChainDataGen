from sqlalchemy import BigInteger, Boolean, Column, Integer, Numeric, String

from repository.common.models import BlockchainTransaction
from repository.database import Base


class SynapseTokenDepositAndSwap(Base):
    __tablename__ = "synapse_token_deposit_and_swap"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(16), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    contract_address = Column(String(42), nullable=True)
    to_address = Column(String(42), nullable=True)
    chain_id = Column(String(32), nullable=True)
    token = Column(String(42), nullable=True)
    amount = Column(Numeric(30, 0), nullable=True)
    token_index_from = Column(Numeric(10, 0), nullable=True)
    token_index_to = Column(Numeric(10, 0), nullable=True)
    min_dy = Column(Numeric(30, 0), nullable=True)
    deadline = Column(Numeric(30, 0), nullable=True)
    kappa = Column(String(66), nullable=True)


class SynapseTokenMintAndSwap(Base):
    __tablename__ = "synapse_token_mint_and_swap"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(16), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    contract_address = Column(String(42), nullable=True)
    to_address = Column(String(42), nullable=True)
    token = Column(String(42), nullable=True)
    amount = Column(Numeric(30, 0), nullable=True)
    fee = Column(Numeric(30, 0), nullable=True)
    token_index_from = Column(Numeric(10, 0), nullable=True)
    token_index_to = Column(Numeric(10, 0), nullable=True)
    min_dy = Column(Numeric(30, 0), nullable=True)
    deadline = Column(Numeric(30, 0), nullable=True)
    swap_success = Column(Boolean, nullable=True)
    kappa = Column(String(66), nullable=True)

class SynapseBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "synapse_blockchain_transactions"

class SynapseCrossChainTransaction(Base):
    __tablename__ = "synapse_cross_chain_transactions"

    id = Column(BigInteger, nullable=False, autoincrement=True, primary_key=True)
    src_blockchain = Column(String(16), nullable=False)
    src_transaction_hash = Column(String(66), nullable=False)
    src_from_address = Column(String(42), nullable=False)
    src_to_address = Column(String(42), nullable=False)
    src_fee = Column(Numeric(30, 0), nullable=False)
    src_fee_usd = Column(Numeric(30, 0), nullable=True)
    src_timestamp = Column(BigInteger, nullable=False)
    dst_blockchain = Column(String(16), nullable=False)
    dst_transaction_hash = Column(String(66), nullable=False)
    dst_from_address = Column(String(42), nullable=False)
    dst_to_address = Column(String(42), nullable=False)
    dst_fee = Column(Numeric(30, 0), nullable=False)
    dst_fee_usd = Column(Numeric(30, 0), nullable=True)
    dst_timestamp = Column(BigInteger, nullable=False)
    recipient = Column(String(512), nullable=True)
    src_contract_address = Column(String(66), nullable=True)
    src_token = Column(String(50), nullable=True)  # token symbol, populated from token_metadata
    dst_contract_address = Column(String(66), nullable=True)
    dst_token = Column(String(50), nullable=True)  # token symbol, populated from token_metadata
    input_amount = Column(Numeric(30, 0), nullable=True)
    input_amount_usd = Column(Numeric(30, 0), nullable=True)
    output_amount = Column(Numeric(30, 0), nullable=True)
    output_amount_usd = Column(Numeric(30, 0), nullable=True)
    swap_success = Column(Boolean, nullable=True)
    kappa = Column(String(66), nullable=True)