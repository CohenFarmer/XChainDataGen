from sqlalchemy import func

from repository.base import BaseRepository

from .models import (
    RouterBlockchainTransaction,
    RouterDepositInfoUpdate,
    RouterFundsDeposited,
    RouterFundsPaid,
    RouterIUSDCDeposited,
    RouterCrossChainTransaction,
)

class RouterFundsDepositedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(RouterFundsDeposited, session_factory)

    def event_exists(self, deposit_id: str, has_message: bool):
        with self.get_session() as session:
            return (
                session.query(RouterFundsDeposited)
                .filter(
                    RouterFundsDeposited.deposit_id == deposit_id,
                    RouterFundsDeposited.has_message == has_message,
                )
                .first()
            )

class RouterIUSDCDepositedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(RouterIUSDCDeposited, session_factory)

    def event_exists(self, usdc_nonce: str):
        with self.get_session() as session:
            return (
                session.query(RouterIUSDCDeposited)
                .filter(RouterIUSDCDeposited.usdc_nonce == usdc_nonce)
                .first()
            )

class RouterDepositInfoUpdateRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(RouterDepositInfoUpdate, session_factory)

    def event_exists(self, deposit_id: str, event_nonce: str):
        with self.get_session() as session:
            return (
                session.query(RouterDepositInfoUpdate)
                .filter(
                    RouterDepositInfoUpdate.deposit_id == deposit_id,
                    RouterDepositInfoUpdate.event_nonce == event_nonce,
                )
                .first()
            )

class RouterFundsPaidRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(RouterFundsPaid, session_factory)

    def event_exists(self, message_hash: str, has_message: bool):
        with self.get_session() as session:
            return (
                session.query(RouterFundsPaid)
                .filter(
                    RouterFundsPaid.message_hash == message_hash,
                    RouterFundsPaid.has_message == has_message,
                )
                .first()
            )

class RouterBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(RouterBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(RouterBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(RouterBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(RouterBlockchainTransaction.timestamp)).scalar()

class RouterCrossChainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(RouterCrossChainTransaction, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(RouterCrossChainTransaction.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(RouterCrossChainTransaction).delete()

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    RouterCrossChainTransaction.src_blockchain,
                    RouterCrossChainTransaction.src_contract_address,
                    RouterCrossChainTransaction.dst_blockchain,
                    RouterCrossChainTransaction.dst_contract_address,
                )
                .group_by(
                    RouterCrossChainTransaction.src_blockchain,
                    RouterCrossChainTransaction.src_contract_address,
                    RouterCrossChainTransaction.dst_blockchain,
                    RouterCrossChainTransaction.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(RouterCrossChainTransaction.input_amount_usd)).scalar()
