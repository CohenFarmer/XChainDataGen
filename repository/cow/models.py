from sqlalchemy import BigInteger, Column, Float, Integer, Numeric, String

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
    #reciever = Column(String(42), nullable=True)
    #app_data = Column(String(66), nullable=True)
    valid_to = Column(BigInteger, nullable=False)
    #order_kind = Column(String(20), nullable=True)
    #price_info = Column(String(100), nullable=True)
    #from_address = Column(String(42), nullable=True)
    #timestamp = Column(BigInteger, nullable=False)

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
        #receiver=None,
        #app_data=None,
        valid_to=None,
        #order_kind=None,
        #price_info=None,
        #from_address=None,
        #timestamp=None,
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
        #self.reciever = receiver
        #self.app_data = app_data
        self.valid_to = valid_to
        #self.order_kind = order_kind
        #self.price_info = price_info
        #self.from_address = from_address
        #self.timestamp = timestamp

    def __repr__(self):
        return (
            f"<AcrossRelayerRefund(blockchain={self.blockchain}, "
            f"trade_id={self.trade_id}, owner={self.owner}, "
            f"sell_token={self.sell_token}, buy_token={self.buy_token}, "
            f"sell_amount={self.sell_amount}, buy_amount={self.buy_amount}, "
            f"fee_amount={self.fee_amount}",
        )
    
class CowBlockchainTransaction(BlockchainTransaction):
    __tablename__ = "cow_blockchain_transactions"

    def __repr__(self):
        return (
            f"<AcrossBlockchainTransaction(blockchain={self.blockchain},"
            f"transaction_hash={self.transaction_hash}, block_number={self.block_number}, ",
        )
    
class CowCrossChainTransaction(Base):
    __tablename__ = "cow_cross_chain_transactions"

    id = Column(BigInteger, nullable=False, autoincrement=True, primary_key=True)
    src_blockchain = Column(String(10), nullable=False)
    src_transaction_hash = Column(String(256), nullable=False)
    src_owner = Column(String(42), nullable=False)
    #src_to_address = Column(String(42), nullable=False)
    src_fee = Column(Numeric(30, 0), nullable=True)
    src_fee_usd = Column(Float, nullable=True)
    #src_timestamp = Column(BigInteger, nullable=False)

    dst_blockchain = Column(String(10), nullable=False)
    dst_transaction_hash = Column(String(256), nullable=False)
    dst_owner = Column(String(42), nullable=False)
    #dst_to_address = Column(String(42), nullable=False)
    dst_fee = Column(Numeric(30, 0), nullable=True)
    dst_fee_usd = Column(Float, nullable=True)
    #dst_timestamp = Column(BigInteger, nullable=False)

    trade_id = Column(String(256), nullable=False)
    sell_token = Column(String(42), nullable=False)
    buy_token = Column(String(42), nullable=False)
    sell_amount = Column(Numeric(30, 0), nullable=False)
    sell_amount_usd = Column(Float, nullable=True)
    buy_amount = Column(Numeric(30, 0), nullable=False)
    buy_amount_usd = Column(Float, nullable=True)
    #input_amount = Column(Numeric(30, 0), nullable=False)
    #input_amount_usd = Column(Float, nullable=True)
    #output_amount = Column(Numeric(30, 0), nullable=False)
    #output_amount_usd = Column(Float, nullable=True)
    #receiver = Column(String(42), nullable=True)
    #app_data = Column(String(66), nullable=True)
    src_valid_to = Column(BigInteger, nullable=False)
    dst_valid_to = Column(BigInteger, nullable=False)
    #order_kind = Column(String(20), nullable=True)
    #price_info = Column(String(100), nullable=True)
    #from_address = Column(String(42), nullable=True)
    #timestamp = Column(BigInteger, nullable=False)

    #src_contract_address = Column(String(42), nullable=True)
    #dst_contract_address = Column(String(42), nullable=True)

    def __init__(
        self,
        src_blockchain,
        src_transaction_hash,
        src_owner,
        #src_to_address,
        src_fee,
        src_fee_usd,
        #src_timestamp,
        dst_blockchain,
        dst_transaction_hash,
        dst_owner,
        #dst_to_address,
        dst_fee,
        dst_fee_usd,
        #dst_timestamp,
        trade_id,
        sell_token,
        buy_token,
        sell_amount,
        sell_amount_usd,
        buy_amount,
        buy_amount_usd,
        #receiver,
        #app_data,
        src_valid_to,
        dst_valid_to,
        #order_kind,
        #price_info,
        #from_address,
        #timestamp,
        #src_contract_address=None,
        #dst_contract_address=None,
    ):
        self.src_blockchain = src_blockchain
        self.src_transaction_hash = src_transaction_hash
        self.src_owner = src_owner
        #self.src_to_address = src_to_address
        self.src_fee = src_fee
        self.src_fee_usd = src_fee_usd
        #self.src_timestamp = src_timestamp
        self.dst_blockchain = dst_blockchain
        self.dst_transaction_hash = dst_transaction_hash
        self.dst_owner = dst_owner
        #self.dst_to_address = dst_to_address
        self.dst_fee = dst_fee
        self.dst_fee_usd = dst_fee_usd
        #self.dst_timestamp = dst_timestamp
        self.trade_id = trade_id
        self.sell_token = sell_token
        self.buy_token = buy_token
        self.sell_amount = sell_amount
        self.sell_amount_usd = sell_amount_usd
        self.buy_amount = buy_amount
        self.buy_amount_usd = buy_amount_usd

        #self.receiver = receiver
        #self.app_data = app_data
        self.src_valid_to = src_valid_to
        
        self.dst_valid_to = dst_valid_to
        #self.order_kind = order_kind
        #self.price_info = price_info
        #self.from_address = from_address
        #self.timestamp = timestamp
        #self.src_contract_address = src_contract_address
        #self.dst_contract_address = dst_contract_address
        #self.input_amount = input_amount
        #self.input_amount_usd = input_amount_usd
        #self.output_amount = output_amount
        #self.output_amount_usd = output_amount_usd

    def __repr__(self):
        return (
            f"<CowCrossChainTransaction(src_blockchain={self.src_blockchain}, "
            f"dst_blockchain={self.dst_blockchain}, trade_id={self.trade_id}, "
            f"src_owner={self.owner}, sell_token={self.sell_token}, buy_token={self.buy_token}, "
            f"sell_amount={self.sell_amount}, buy_amount={self.buy_amount}, "
        )