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

    def event_exists(self, blockchain: str, trade_id: str):
        with self.get_session() as session:
            return (
                session.query(CowTrade.id)
                .filter(CowTrade.blockchain == blockchain, CowTrade.trade_id == trade_id)
                .first()
            )

    def iter_missing_cross_chain_key(self, limit: int = 500):
        with self.get_session() as session:
            for row in (
                session.query(CowTrade)
                .filter(CowTrade.cross_chain_key.is_(None))
                .limit(limit)
                .all()
            ):
                yield row

    def set_cross_chain_fields(self, blockchain: str, trade_id: str, app_data: str | None, app_data_cid: str | None, key: str | None):
        with self.get_session() as session:
            session.query(CowTrade).filter(
                CowTrade.blockchain == blockchain,
                CowTrade.trade_id == trade_id,
            ).update(
                {
                    "app_data": app_data,
                    "app_data_cid": app_data_cid,
                    "cross_chain_key": key,
                }
            )
            session.commit()

        
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
                    CowCrossChainTransaction.sell_token,
                    CowCrossChainTransaction.dst_blockchain,
                    CowCrossChainTransaction.buy_token,
                ).group_by(
                    CowCrossChainTransaction.src_blockchain,
                    CowCrossChainTransaction.sell_token,
                    CowCrossChainTransaction.dst_blockchain,
                    CowCrossChainTransaction.buy_token,
                )
                .all()
            )
        
    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(CowCrossChainTransaction.input_amount_usd)).scalar()
        
Index("ix_cow_cross_blockchain_transactions_src_tx_hash", CowCrossChainTransaction.src_transaction_hash)
