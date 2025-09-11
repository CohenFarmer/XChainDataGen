from sqlalchemy import func

from repository.base import BaseRepository

from .models import (
    EcoBlockchainTransaction,
    EcoIntentCreated,
    EcoFulfillment,
    EcoCrossChainTransaction,
)


class EcoIntentCreatedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(EcoIntentCreated, session_factory)

    def event_exists(self, intent_hash: str):
        with self.get_session() as session:
            return (
                session.query(EcoIntentCreated)
                .filter(EcoIntentCreated.intent_hash == intent_hash)
                .first()
            )


class EcoFulfillmentRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(EcoFulfillment, session_factory)

    def event_exists(self, intent_hash: str):
        with self.get_session() as session:
            return (
                session.query(EcoFulfillment)
                .filter(EcoFulfillment.intent_hash == intent_hash)
                .first()
            )


class EcoBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(EcoBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(EcoBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(EcoBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(EcoBlockchainTransaction.timestamp)).scalar()


class EcoCrossChainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(EcoCrossChainTransaction, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(EcoCrossChainTransaction.id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(EcoCrossChainTransaction).delete()

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    EcoCrossChainTransaction.src_blockchain,
                    EcoCrossChainTransaction.src_contract_address,
                    EcoCrossChainTransaction.dst_blockchain,
                    EcoCrossChainTransaction.dst_contract_address,
                )
                .group_by(
                    EcoCrossChainTransaction.src_blockchain,
                    EcoCrossChainTransaction.src_contract_address,
                    EcoCrossChainTransaction.dst_blockchain,
                    EcoCrossChainTransaction.dst_contract_address,
                )
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(EcoCrossChainTransaction.input_amount_usd)).scalar()
