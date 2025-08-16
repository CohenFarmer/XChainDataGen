from sqlalchemy import func

from repository.base import BaseRepository

from .models import (
    FlyBlockchainTransaction,
    FlyDeposit,
    FlyCrossChainTransaction,
    FlySwapIn,
    FlySwapOut,
)


class FlyBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(FlyBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(FlyBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(FlyBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(FlyBlockchainTransaction.timestamp)).scalar()


class FlySwapInRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(FlySwapIn, session_factory)

    def event_exists(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(FlySwapIn)
                .filter(FlySwapIn.transaction_hash == transaction_hash)
                .first()
            )


class FlySwapOutRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(FlySwapOut, session_factory)

    def event_exists(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(FlySwapOut)
                .filter(FlySwapOut.transaction_hash == transaction_hash)
                .first()
            )


class FlyDepositRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(FlyDeposit, session_factory)

    def event_exists(self, deposit_hash: str):
        with self.get_session() as session:
            return (
                session.query(FlyDeposit)
                .filter(FlyDeposit.deposit_data_hash == deposit_hash)
                .first()
            )


class FlyCrossChainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(FlyCrossChainTransaction, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(FlyCrossChainTransaction.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(FlyCrossChainTransaction).delete()

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    FlyCrossChainTransaction.src_blockchain,
                    FlyCrossChainTransaction.src_contract_address,
                    FlyCrossChainTransaction.dst_blockchain,
                    FlyCrossChainTransaction.dst_contract_address,
                )
                .group_by(
                    FlyCrossChainTransaction.src_blockchain,
                    FlyCrossChainTransaction.src_contract_address,
                    FlyCrossChainTransaction.dst_blockchain,
                    FlyCrossChainTransaction.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(FlyCrossChainTransaction.input_amount_usd)).scalar()
