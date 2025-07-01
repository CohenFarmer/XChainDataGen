import time

from sqlalchemy import case, update
from sqlalchemy.orm import aliased

from config.constants import Bridge
from generator.base_generator import BaseGenerator
from generator.common.price_generator import PriceGenerator
from repository.common.models import TokenMetadata
from repository.common.repository import (
    NativeTokenRepository,
    TokenMetadataRepository,
    TokenPriceRepository,
)
from repository.database import DBSession
from repository.mayan.models import (
    MayanBlockchainTransaction,
    MayanCrossChainTransaction,
    MayanForwarded,
    MayanFulfillOrder,
    MayanInitOrder,
    MayanOrderCreated,
    MayanOrderFulfilled,
    MayanOrderUnlocked,
    MayanRegisterOrder,
    MayanUnlock,
)
from repository.mayan.repository import (
    MayanBlockchainTransactionRepository,
    MayanCrossChainTransactionRepository,
)
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message_generator,
    log_error,
    log_to_cli,
)


class MayanGenerator(BaseGenerator):
    CLASS_NAME = "MayanGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.MAYAN
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.transactions_repo = MayanBlockchainTransactionRepository(DBSession)

        self.cross_chain_transactions_repo = MayanCrossChainTransactionRepository(DBSession)

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "create_cross_chain_transactions"

        try:
            self.match_sol_to_evm()
            self.match_evm_to_sol()

            start_ts = int(self.transactions_repo.get_min_timestamp()) - 86400
            end_ts = int(self.transactions_repo.get_max_timestamp()) + 86400

            # POPULATE TOKEN TABLES WITH NATIVE TOKEN INFO
            self.price_generator.populate_native_tokens(
                self.bridge,
                self.native_token_repo,
                self.token_metadata_repo,
                self.token_price_repo,
                start_ts,
                end_ts,
            )

            # The Solana blockchain is not supported by the Alchemy API, so we need to make some
            # additions to the database manually
            self.fetch_solana_data(start_ts, end_ts)

            cctxs = self.cross_chain_transactions_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)

            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "input_amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "input_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "output_amount",
                "dst_blockchain",
                "dst_contract_address",
                "dst_timestamp",
                "output_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "refund_amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "refund_amount_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "dst_fee",
                "dst_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cross_chain_transactions_repo,
                "mayan_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "refund_fee",
                "refund_fee_usd",
            )

            # We will need to also fix the decimals for the Solana native values
            # Natively, the token has 9 decimals, but the BNB chain uses 18 decimals
            # and the Alchemy API returns the values with 18 decimals
            # So we multiply the values by 10^9 to get the correct values
            with self.cross_chain_transactions_repo.get_session() as session:
                stmt = (
                    update(MayanCrossChainTransaction)
                    .where(MayanCrossChainTransaction.src_blockchain == "solana")
                    .values(
                        src_fee_usd=MayanCrossChainTransaction.src_fee_usd * 10**9,
                        refund_fee_usd=MayanCrossChainTransaction.refund_fee_usd * 10**9,
                    )
                    .execution_options(synchronize_session=False)
                    .execution_options(synchronize_session=False)
                )
                session.execute(stmt)

                stmt = (
                    update(MayanCrossChainTransaction)
                    .where(MayanCrossChainTransaction.dst_blockchain == "solana")
                    .values(dst_fee_usd=MayanCrossChainTransaction.dst_fee_usd * 10**9)
                    .execution_options(synchronize_session=False)
                )
                session.execute(stmt)

        except Exception as e:
            exception = CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing cross chain transactions. Error: {e}",
            )
            log_error(self.bridge, exception)

    def match_sol_to_evm(self):
        func_name = "match_sol_to_evm"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching cross-chain SOL -> EVM transfers...")
        )

        self.cross_chain_transactions_repo.empty_table()

        try:
            results = []

            SrcTx = aliased(MayanBlockchainTransaction)
            DstTx = aliased(MayanBlockchainTransaction)
            RefundTx = aliased(MayanBlockchainTransaction)

            with self.cross_chain_transactions_repo.get_session() as session:
                results = (
                    session.query(
                        MayanInitOrder,
                        MayanOrderFulfilled,
                        MayanUnlock,
                        SrcTx,
                        DstTx,
                        RefundTx,
                    )
                    .join(MayanOrderFulfilled, MayanInitOrder.order_hash == MayanOrderFulfilled.key)
                    .join(MayanUnlock, MayanInitOrder.state == MayanUnlock.state)
                    .outerjoin(SrcTx, SrcTx.transaction_hash == MayanInitOrder.signature)
                    .outerjoin(
                        DstTx, DstTx.transaction_hash == MayanOrderFulfilled.transaction_hash
                    )  # noqa: E501
                    .outerjoin(RefundTx, RefundTx.transaction_hash == MayanUnlock.signature)
                    .all()
                )

            cctxs = []

            for init, fulfilled, unlock, src_tx, dst_tx, refund_tx in results:
                cctxs.append(
                    MayanCrossChainTransaction(
                        src_blockchain="solana",
                        src_transaction_hash=src_tx.transaction_hash,
                        src_from_address=init.trader,
                        src_to_address="BLZRi6frs4X4DNLw56V4EXai1b6QVESN1BhHBTYM9VcY",
                        src_fee=src_tx.fee,
                        src_fee_usd=None,
                        src_timestamp=src_tx.timestamp,
                        dst_blockchain=dst_tx.blockchain,
                        dst_transaction_hash=dst_tx.transaction_hash,
                        dst_from_address=dst_tx.from_address,
                        dst_to_address=dst_tx.to_address,
                        dst_fee=dst_tx.fee,
                        dst_fee_usd=None,
                        dst_timestamp=dst_tx.timestamp,
                        refund_blockchain="solana",
                        refund_transaction_hash=unlock.signature,
                        refund_from_address=unlock.driver_acc,
                        refund_to_address="9w1D9okTM8xNE7Ntb7LpaAaoLc6LfU9nHFs2h2KTpX1H",
                        refund_fee=refund_tx.fee,
                        refund_fee_usd=None,
                        refund_timestamp=refund_tx.timestamp,
                        intent_id=init.order_hash,
                        depositor=init.trader,
                        recipient=init.addr_dest,
                        src_contract_address=init.mint_from,
                        dst_contract_address=init.token_out,
                        input_amount=init.amount_in,
                        input_amount_usd=None,
                        output_amount=fulfilled.net_amount,
                        output_amount_usd=None,
                        refund_amount=unlock.amount,
                        refund_amount_usd=None,
                        refund_token=unlock.mint_from,
                    )
                )

            self.cross_chain_transactions_repo.create_all(cctxs)

            size = self.cross_chain_transactions_repo.get_number_of_records()

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    (
                        f"Token transfers matched in {end_time - start_time} seconds. "
                        f"Total records inserted: {size}",
                    ),
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing token transfers. Error: {e}",
            ) from e

    def match_evm_to_sol(self):
        func_name = "match_evm_to_sol"

        start_time = time.time()
        log_to_cli(
            build_log_message_generator(self.bridge, "Matching cross-chain EVM -> SOL transfers...")
        )

        try:
            results = []

            SrcTx = aliased(MayanBlockchainTransaction)
            DstTx = aliased(MayanBlockchainTransaction)
            RefundTx = aliased(MayanBlockchainTransaction)

            with self.cross_chain_transactions_repo.get_session() as session:
                results = (
                    session.query(
                        MayanForwarded.blockchain.label("src_blockchain"),
                        MayanForwarded.transaction_hash.label("src_transaction_hash"),
                        MayanForwarded.trader.label("src_from_address"),
                        MayanForwarded.mayan_protocol.label("src_to_address"),
                        SrcTx.fee.label("src_fee"),
                        SrcTx.timestamp.label("src_timestamp"),
                        MayanFulfillOrder.signature.label("dst_transaction_hash"),
                        MayanFulfillOrder.driver.label("dst_from_address"),
                        MayanFulfillOrder.dest.label("dst_to_address"),
                        DstTx.fee.label("dst_fee"),
                        DstTx.timestamp.label("dst_timestamp"),
                        RefundTx.blockchain.label("refund_blockchain"),
                        RefundTx.transaction_hash.label("refund_transaction_hash"),
                        RefundTx.from_address.label("refund_from_address"),
                        RefundTx.to_address.label("refund_to_address"),
                        RefundTx.fee.label("refund_fee"),
                        RefundTx.timestamp.label("refund_timestamp"),
                        MayanOrderCreated.key.label("intent_id"),
                        MayanForwarded.trader.label("depositor"),
                        MayanRegisterOrder.addr_dest.label("recipient"),
                        MayanRegisterOrder.token_in.label("src_contract_address"),
                        MayanRegisterOrder.token_out.label("dst_contract_address"),
                        case(
                            (MayanForwarded.amount != None, MayanForwarded.amount),  # noqa: E711 DO NOT REPLACE != WITH 'IS NOT'
                            else_=SrcTx.value,
                        ).label("input_amount"),
                        MayanFulfillOrder.amount.label("output_amount"),
                    )
                    .join(
                        MayanOrderCreated,
                        MayanOrderCreated.transaction_hash == MayanForwarded.transaction_hash,
                    )
                    .join(
                        MayanRegisterOrder, MayanRegisterOrder.order_hash == MayanOrderCreated.key
                    )
                    .join(MayanFulfillOrder, MayanFulfillOrder.state == MayanRegisterOrder.state)
                    .join(MayanOrderUnlocked, MayanOrderUnlocked.key == MayanOrderCreated.key)
                    .join(SrcTx, SrcTx.transaction_hash == MayanForwarded.transaction_hash)
                    .join(DstTx, DstTx.transaction_hash == MayanFulfillOrder.signature)
                    .join(
                        RefundTx, RefundTx.transaction_hash == MayanOrderUnlocked.transaction_hash
                    )
                )

            cctxs = []

            for row in results:
                cctxs.append(
                    MayanCrossChainTransaction(
                        src_blockchain=row.src_blockchain,
                        src_transaction_hash=row.src_transaction_hash,
                        src_from_address=row.src_from_address,
                        src_to_address=row.src_to_address,
                        src_fee=row.src_fee,
                        src_fee_usd=None,
                        src_timestamp=row.src_timestamp,
                        dst_blockchain="solana",
                        dst_transaction_hash=row.dst_transaction_hash,
                        dst_from_address=row.dst_from_address,
                        dst_to_address=row.dst_to_address,
                        dst_fee=row.dst_fee,
                        dst_fee_usd=None,
                        dst_timestamp=row.dst_timestamp,
                        refund_blockchain=row.refund_blockchain,
                        refund_transaction_hash=row.refund_transaction_hash,
                        refund_from_address=row.refund_from_address,
                        refund_to_address=row.refund_to_address,
                        refund_fee=row.refund_fee,
                        refund_fee_usd=None,
                        refund_timestamp=row.refund_timestamp,
                        intent_id=row.intent_id,
                        depositor=row.depositor,
                        recipient=row.recipient,
                        src_contract_address=row.src_contract_address,
                        dst_contract_address=row.dst_contract_address,
                        input_amount=row.input_amount,
                        input_amount_usd=None,
                        output_amount=row.output_amount,
                        output_amount_usd=None,
                        refund_amount=row.input_amount,  # in the case of usage of intermediary
                        # protocols, the refund amount is a bit less than the input amount (because
                        # of fees), but there is not way to get the exact refund amount unless we
                        # parse internal transactions and match to the unlock events.
                        refund_amount_usd=None,
                        refund_token="0x0000000000000000000000000000000000000000",
                    )
                )

            self.cross_chain_transactions_repo.create_all(cctxs)

            size = self.cross_chain_transactions_repo.get_number_of_records()

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    (
                        f"Token transfers matched in {end_time - start_time} seconds. "
                        f"Total records inserted: {size}",
                    ),
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing token transfers. Error: {e}",
            ) from e

    def populate_token_info_tables(self, cctxs, start_ts, end_ts):
        start_time = time.time()
        log_to_cli(build_log_message_generator(self.bridge, "Fetching token prices..."))

        for cctx in cctxs:
            self.price_generator.populate_token_info(
                self.bridge,
                self.token_metadata_repo,
                self.token_price_repo,
                cctx.src_blockchain,
                cctx.dst_blockchain,
                cctx.src_contract_address,
                cctx.dst_contract_address,
                start_ts,
                end_ts,
            )

        end_time = time.time()
        log_to_cli(
            build_log_message_generator(
                self.bridge,
                f"Token prices fetched in {end_time - start_time} seconds.",
            ),
            CliColor.SUCCESS,
        )

    def fetch_solana_data(self, start_ts, end_ts):
        if not self.native_token_repo.get_native_token_by_blockchain("solana"):
            self.native_token_repo.create(
                {
                    "symbol": "SOL",
                    "blockchain": "solana",
                }
            )

        if not self.token_metadata_repo.get_token_metadata_by_symbol("SOL"):
            self.token_metadata_repo.create(
                {
                    "symbol": "SOL",
                    "name": "Solana",
                    "decimals": 9,
                    "blockchain": "solana",
                    "address": "11111111111111111111111111111111",
                }
            )

        # In Mayan, when the native token is used in the destination blockchain,
        # the address is set to 0x0000000000000000000000000000000000000000
        # however, if we fetch info from Alchemy, we will not get the
        # token metadata for the native token, so we need to fill it manually
        # with the data we have in the NativeToken table and the TokenMetadata table

        if not self.token_metadata_repo.get_token_metadata_by_symbol_and_blockchain(
            "WETH", "solana"
        ):
            self.token_metadata_repo.create(
                {
                    "symbol": "WETH",
                    "name": "Wrapped Ether",
                    "decimals": 8,
                    "blockchain": "solana",
                    "address": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
                }
            )

        if not self.token_metadata_repo.get_token_metadata_by_symbol_and_blockchain(
            "USDC", "solana"
        ):
            self.token_metadata_repo.create(
                {
                    "symbol": "USDC",
                    "name": "USDC",
                    "decimals": 6,
                    "blockchain": "solana",
                    "address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                }
            )

        if not PriceGenerator.is_token_price_complete(
            self.token_price_repo,
            start_ts,
            end_ts,
            "SOL",
            "solana",
        ):
            PriceGenerator.fetch_and_store_token_prices(
                self.bridge,
                self.token_price_repo,
                start_ts,
                end_ts,
                "Solana",
                "SOL",
            )

        # We found an erros in the Alchemy API where it returns the wrong
        # decimals for the DONKEY token in BNB, so we need to fix it manually
        with self.token_metadata_repo.get_session() as session:
            stmt = (
                update(TokenMetadata)
                .values(decimals=18)
                .where(
                    TokenMetadata.blockchain == "bnb",
                    TokenMetadata.symbol == "DONKEY",
                    TokenMetadata.address == "0xa49fa5e8106e2d6d6a69e78df9b6a20aab9c4444",
                )
                .execution_options(synchronize_session=False)
            )
            session.execute(stmt)
