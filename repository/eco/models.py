from sqlalchemy import BigInteger, Column, Integer, Numeric, String

from repository.common.models import BlockchainTransaction
from repository.database import Base


class EcoIntentCreated(Base):
    __tablename__ = "eco_intent_created"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(16), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    intent_hash = Column(String(66), nullable=False)
    salt = Column(String(66), nullable=True)
    source_chain_id = Column(Numeric(30, 0), nullable=False)
    destination_chain_id = Column(Numeric(30, 0), nullable=False)
    inbox = Column(String(42), nullable=False)
    creator = Column(String(42), nullable=False)
    prover = Column(String(42), nullable=False)
    deadline = Column(Numeric(30, 0), nullable=False)
    native_value = Column(Numeric(30, 0), nullable=False)


class EcoFulfillment(Base):
    __tablename__ = "eco_fulfillment"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(16), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    intent_hash = Column(String(66), nullable=False)
    source_chain_id = Column(Numeric(30, 0), nullable=False)
    prover = Column(String(42), nullable=False)
    claimant = Column(String(42), nullable=False)


class EcoBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "eco_blockchain_transactions"


class EcoCrossChainTransaction(Base):
    __tablename__ = "eco_cross_chain_transactions"

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
    src_contract_address = Column(String(66), nullable=True)
    dst_contract_address = Column(String(66), nullable=True)
    input_amount = Column(Numeric(30, 0), nullable=True)
    input_amount_usd = Column(Numeric(30, 0), nullable=True)
    output_amount = Column(Numeric(30, 0), nullable=True)
    output_amount_usd = Column(Numeric(30, 0), nullable=True)
    intent_hash = Column(String(66), nullable=False)
