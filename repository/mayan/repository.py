from sqlalchemy import func

from repository.base import BaseRepository

from .models import (
    MayanAuctionBid,
    MayanAuctionClose,
    MayanBlockchainTransaction,
    MayanCrossChainTransaction,
    MayanForwarded,
    MayanFulfillOrder,
    MayanInitOrder,
    MayanOrderCreated,
    MayanOrderFulfilled,
    MayanOrderUnlocked,
    MayanRegisterOrder,
    MayanSetAuctionWinner,
    MayanSettle,
    MayanSwapAndForwarded,
    MayanUnlock,
)


class MayanSwapAndForwardedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanSwapAndForwarded, session_factory)

    def event_exists(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(MayanSwapAndForwarded)
                .filter(MayanSwapAndForwarded.transaction_hash == transaction_hash)
                .first()
            )


class MayanForwardedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanForwarded, session_factory)

    def event_exists(self, transaction_hash: str):
        with self.get_session() as session:
            return (
                session.query(MayanForwarded)
                .filter(MayanForwarded.transaction_hash == transaction_hash)
                .first()
            )

    def get_all_forwarded_eth(self):
        with self.get_session() as session:
            return (
                session.query(MayanForwarded)
                .filter(MayanForwarded.token == "0x0000000000000000000000000000000000000000")
                .all()
            )


class MayanOrderCreatedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanOrderCreated, session_factory)

    def event_exists(self, key: str):
        with self.get_session() as session:
            return session.query(MayanOrderCreated).filter(MayanOrderCreated.key == key).first()


class MayanOrderFulfilledRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanOrderFulfilled, session_factory)

    def event_exists(self, key: str):
        with self.get_session() as session:
            return session.query(MayanOrderFulfilled).filter(MayanOrderFulfilled.key == key).first()

    def update_middle_info_order_fulfilled(
        self, key: str, middle_dst_token: str, middle_dst_amount: float
    ):
        with self.get_session() as session:
            session.query(MayanOrderFulfilled).filter(MayanOrderFulfilled.key == key).update(
                {"middle_dst_token": middle_dst_token, "middle_dst_amount": middle_dst_amount}
            )


class MayanOrderUnlockedRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanOrderUnlocked, session_factory)

    def event_exists(self, key: str):
        with self.get_session() as session:
            return session.query(MayanOrderUnlocked).filter(MayanOrderUnlocked.key == key).first()


class MayanInitOrderRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanInitOrder, session_factory)

    def event_exists(self, order_hash: str):
        with self.get_session() as session:
            return session.query(self.model).filter(self.model.order_hash == order_hash).first()


class MayanUnlockRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanUnlock, session_factory)

    def event_exists(self, state_from_acc: str):
        with self.get_session() as session:
            return (
                session.query(self.model)
                .filter(MayanUnlock.state_from_acc == state_from_acc)
                .first()
            )


class MayanFulfillOrderRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanFulfillOrder, session_factory)

    def event_exists(self, signature: str):
        with self.get_session() as session:
            return (
                session.query(self.model).filter(MayanFulfillOrder.signature == signature).first()
            )


class MayanSettleRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanSettle, session_factory)

    def event_exists(self, signature: str):
        with self.get_session() as session:
            return session.query(self.model).filter(MayanSettle.signature == signature).first()


class MayanSetAuctionWinnerRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanSetAuctionWinner, session_factory)

    def event_exists(self, auction: str):
        with self.get_session() as session:
            return (
                session.query(self.model).filter(MayanSetAuctionWinner.auction == auction).first()
            )


class MayanRegisterOrderRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanRegisterOrder, session_factory)

    def event_exists(self, order_hash: str):
        with self.get_session() as session:
            return (
                session.query(self.model)
                .filter(MayanRegisterOrder.order_hash == order_hash)
                .first()
            )


class MayanAuctionBidRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanAuctionBid, session_factory)

    def event_exists(self, signature: str):
        with self.get_session() as session:
            return session.query(self.model).filter(MayanAuctionBid.signature == signature).first()


class MayanAuctionCloseRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanAuctionClose, session_factory)

    def event_exists(self, auction: str):
        with self.get_session() as session:
            return session.query(self.model).filter(MayanAuctionClose.auction == auction).first()


class MayanBlockchainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanBlockchainTransaction, session_factory)

    def get_transaction_by_hash(self, transaction_hash: str):
        with self.get_session() as session:
            return session.get(MayanBlockchainTransaction, transaction_hash)

    def get_min_timestamp(self):
        with self.get_session() as session:
            return session.query(func.min(MayanBlockchainTransaction.timestamp)).scalar()

    def get_max_timestamp(self):
        with self.get_session() as session:
            return session.query(func.max(MayanBlockchainTransaction.timestamp)).scalar()


########## Processed Data ##########


class MayanCrossChainTransactionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(MayanCrossChainTransaction, session_factory)

    def get_number_of_records(self):
        with self.get_session() as session:
            return session.query(func.count(MayanCrossChainTransaction.intent_id)).scalar()

    def empty_table(self):
        with self.get_session() as session:
            return session.query(MayanCrossChainTransaction).delete()

    def update_amount_usd(self, transaction_hash: str, amount_usd: float):
        with self.get_session() as session:
            session.query(MayanCrossChainTransaction).filter(
                MayanCrossChainTransaction.src_transaction_hash == transaction_hash
            ).update({"output_amount_usd": amount_usd})

    def get_by_src_tx_hash(self, src_tx_hash: str):
        with self.get_session() as session:
            return (
                session.query(MayanCrossChainTransaction)
                .filter(MayanCrossChainTransaction.src_transaction_hash == src_tx_hash)
                .first()
            )

    def get_unique_src_dst_contract_pairs(self):
        with self.get_session() as session:
            return (
                session.query(
                    MayanCrossChainTransaction.src_blockchain,
                    MayanCrossChainTransaction.src_contract_address,
                    MayanCrossChainTransaction.dst_blockchain,
                    MayanCrossChainTransaction.dst_contract_address,
                    func.count().label("pair_count"),
                )
                .group_by(
                    MayanCrossChainTransaction.src_blockchain,
                    MayanCrossChainTransaction.src_contract_address,
                    MayanCrossChainTransaction.dst_blockchain,
                    MayanCrossChainTransaction.dst_contract_address,
                )
                .order_by(func.count().desc())
                .all()
            )

    def get_total_amount_usd_transacted(self):
        with self.get_session() as session:
            return session.query(func.sum(MayanCrossChainTransaction.input_amount_usd)).scalar()
