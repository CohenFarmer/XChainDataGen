from sqlalchemy import BigInteger, Column, Integer, Numeric, String, Boolean

from repository.common.models import BlockchainTransaction
from repository.database import Base

class RouterFundsDeposited(Base):
    __tablename__ = "router_funds_deposited"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(16), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    partner_id = Column(Numeric(30, 0), nullable=False)
    amount = Column(Numeric(30, 0), nullable=False)
    dest_chain_id_bytes = Column(String(66), nullable=False)
    dest_amount = Column(Numeric(30, 0), nullable=False)
    deposit_id = Column(Numeric(30, 0), nullable=False)
    src_token = Column(String(42), nullable=False)
    depositor = Column(String(42), nullable=False)
    recipient_raw = Column(String(512), nullable=False)
    dest_token_raw = Column(String(512), nullable=False)
    message = Column(String(20000), nullable=True)
    has_message = Column(Boolean, nullable=False)
    message_hash = Column(String(66), nullable=True)  # computed for join with FundsPaid

class RouterIUSDCDeposited(Base):
    __tablename__ = "router_iusdc_deposited"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(16), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    partner_id = Column(Numeric(30, 0), nullable=False)
    amount = Column(Numeric(30, 0), nullable=False)
    dest_chain_id_bytes = Column(String(66), nullable=False)
    usdc_nonce = Column(Numeric(30, 0), nullable=False)
    src_token = Column(String(42), nullable=False)
    recipient = Column(String(66), nullable=False)  # bytes32
    depositor = Column(String(42), nullable=False)

class RouterDepositInfoUpdate(Base):
    __tablename__ = "router_deposit_info_update"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(16), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    src_token = Column(String(42), nullable=False)
    fee_amount = Column(Numeric(30, 0), nullable=False)
    deposit_id = Column(Numeric(30, 0), nullable=False)
    event_nonce = Column(Numeric(30, 0), nullable=False)
    initiate_withdrawal = Column(Boolean, nullable=False)
    depositor = Column(String(42), nullable=False)

class RouterFundsPaid(Base):
    __tablename__ = "router_funds_paid"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    blockchain = Column(String(16), nullable=False)
    transaction_hash = Column(String(66), nullable=False)
    message_hash = Column(String(66), nullable=False)
    forwarder = Column(String(42), nullable=False)
    nonce = Column(Numeric(30, 0), nullable=False)
    has_message = Column(Boolean, nullable=False)
    exec_flag = Column(Boolean, nullable=True)
    exec_data = Column(String(20000), nullable=True)

class RouterBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "router_blockchain_transactions"

class RouterCrossChainTransaction(Base):
    __tablename__ = "router_cross_chain_transactions"

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
    deposit_id = Column(Numeric(30, 0), nullable=True)
    depositor = Column(String(42), nullable=False)
    recipient = Column(String(512), nullable=True)
    src_contract_address = Column(String(66), nullable=True)
    dst_contract_address = Column(String(66), nullable=True)
    input_amount = Column(Numeric(30, 0), nullable=True)
    input_amount_usd = Column(Numeric(30, 0), nullable=True)
    output_amount = Column(Numeric(30, 0), nullable=True)
    output_amount_usd = Column(Numeric(30, 0), nullable=True)
    message_hash = Column(String(66), nullable=True)

