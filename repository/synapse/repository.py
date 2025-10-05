from sqlalchemy import func

from repository.base import BaseRepository

from .models import (
    SynapseBlockchainTransaction,
    SynapseTokenDepositAndSwap,
    SynapseTokenMintAndSwap,
)

class SynapseTokenDepositAndSwapRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(SynapseTokenDepositAndSwap, session_factory)

    def event_exists(self, transaction_hash: str, to_address: str, amount: int | None):
        with self.get_session() as session:
            query = session.query(SynapseTokenDepositAndSwap).filter(
                SynapseTokenDepositAndSwap.transaction_hash == transaction_hash,
            )
            if to_address is not None:
                query = query.filter(SynapseTokenDepositAndSwap.to_address == to_address)
            if amount is not None:
                query = query.filter(SynapseTokenDepositAndSwap.amount == amount)
            return query.first()


class SynapseTokenMintAndSwapRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(SynapseTokenMintAndSwap, session_factory)

    def event_exists(self, transaction_hash: str, kappa: str | None):
        with self.get_session() as session:
            query = session.query(SynapseTokenMintAndSwap).filter(
                SynapseTokenMintAndSwap.transaction_hash == transaction_hash,
            )
            if kappa is not None:
                query = query.filter(SynapseTokenMintAndSwap.kappa == kappa)
            return query.first()

class SynapseBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(SynapseBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(SynapseBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(SynapseBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(SynapseBlockchainTransaction.timestamp)).scalar()
