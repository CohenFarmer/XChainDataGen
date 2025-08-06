from sqlalchemy import Index, func

from repository.base import BaseRepository

from .models import (
    CowBlockchainTransaction,
    CowCrossChainTransaction,
    CowTrade,
)

class CowTradeRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(CowTrade, session_factory)

    def event_exists(
        self,
        transaction_hash: str,
        trade_id: str,
        owner: str,
        sell_token: str,
        buy_token: str,
        sell_amount: str,
        buy_amount: str,
        fee_amount: str,
        receiver: str = None,
        app_data: str = None,
        valid_to: str = None,
        order_kind: str = None,
        price_info: str = None,
        from_address: str = None,
        timestamp: str = None,
    ):
        with self.get_session() as session:
            return (
                session.query(CowTrade).filter(
                    CowTrade.transaction_hash == transaction_hash,
                    CowTrade.trade_id == trade_id,
                    CowTrade.owner == owner,
                    CowTrade.sell_token == sell_token,
                    CowTrade.buy_token == buy_token,
                    CowTrade.sell_amount == sell_amount,
                    CowTrade.buy_amount == buy_amount,
                    CowTrade.fee_amount == fee_amount,
                    CowTrade.receiver == receiver,
                    CowTrade.app_data == app_data,
                    CowTrade.valid_to == valid_to,
                    CowTrade.order_kind == order_kind,
                    CowTrade.price_info == price_info,
                    CowTrade.from_address == from_address,
                    CowTrade.timestamp == timestamp,
                )
                .first()
            )
        
class CowBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(CowBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(CowBlockchainTransaction, transaction_hash)
    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(CowBlockchainTransaction.timestamp)).scalar()
    
    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(CowBlockchainTransaction.timestamp)).scalar()
        

#processed cross-chain data
class CowCrossChainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(CowCrossChainTransaction, session_factory)
    
    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(CowCrossChainTransaction.id)).scalar()
    
    def empty_table(self):
        with self.get_session() as session:
            return session.query(CowCrossChainTransaction).delete()
        
    def update_amount_usd(self, transaction_hash: str, amount_usd: float):
        with self.get_session() as session:
            session.query(CowCrossChainTransaction).filter(
                CowCrossChainTransaction.src_transaction_hash == transaction_hash
            ).update({"amount_usd": amount_usd})
    
    def get_by_src_tx_hash(self, src_tx_hash: str):
        with self.get_session() as session:
            return (
                session.query(CowCrossChainTransaction)
                .filter(CowCrossChainTransaction.src_transaction_hash == src_tx_hash)
                .first()
            )
    
    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    CowCrossChainTransaction.src_blockchain,
                    CowCrossChainTransaction.src_contract_address,
                    CowCrossChainTransaction.dst_blockchain,
                    CowCrossChainTransaction.dst_contract_address,
                ).group_by(
                    CowCrossChainTransaction.src_blockchain,
                    CowCrossChainTransaction.src_contract_address,  
                    CowCrossChainTransaction.dst_blockchain,
                    CowCrossChainTransaction.dst_contract_address,
                )
                .all()
            )
        
    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(CowCrossChainTransaction.input_amount_usd)).scalar()
        
Index("ix_cow_cross_blockchain_transactions_src_tx_hash", CowCrossChainTransaction.src_transaction_hash)
