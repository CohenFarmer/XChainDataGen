from sqlalchemy import func

from repository.base import BaseRepository

from .models import (
    WormholeBlockchainTransaction,
    WormholePublished,
    WormholeRedeemed,
    WormholeCrossChainTransaction,
)


class WormholeBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(WormholeBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(WormholeBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(WormholeBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(WormholeBlockchainTransaction.timestamp)).scalar()


class WormholePublishedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(WormholePublished, session_factory)

    def event_exists(self, tx_hash: str, sequence: str):
        with self.get_session() as session:
            return (
                session.query(WormholePublished)
                .filter(WormholePublished.transaction_hash == tx_hash, WormholePublished.sequence == sequence)
                .first()
            )


class WormholeRedeemedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(WormholeRedeemed, session_factory)

    def event_exists(self, tx_hash: str, sequence: str):
        with self.get_session() as session:
            return (
                session.query(WormholeRedeemed)
                .filter(WormholeRedeemed.transaction_hash == tx_hash, WormholeRedeemed.sequence == sequence)
                .first()
            )


class WormholeCrossChainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(WormholeCrossChainTransaction, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(WormholeCrossChainTransaction.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(WormholeCrossChainTransaction).delete()

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    WormholeCrossChainTransaction.src_blockchain,
                    WormholeCrossChainTransaction.src_contract_address,
                    WormholeCrossChainTransaction.dst_blockchain,
                    WormholeCrossChainTransaction.dst_contract_address,
                )
                .group_by(
                    WormholeCrossChainTransaction.src_blockchain,
                    WormholeCrossChainTransaction.src_contract_address,
                    WormholeCrossChainTransaction.dst_blockchain,
                    WormholeCrossChainTransaction.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(WormholeCrossChainTransaction.input_amount_usd)).scalar()
