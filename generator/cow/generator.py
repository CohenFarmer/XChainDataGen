import time

from sqlalchemy import text

from config.constants import Bridge
from generator.base_generator import BaseGenerator
from generator.common.price_generator import PriceGenerator
from repository.cow.repository import CowTradeRepository, CowBlockchainTransactionRepository, CowCrossChainTransactionRepository
from repository.common.repository import NativeTokenRepository, TokenPriceRepository, TokenMetadataRepository
from repository.database import DBSession
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message_generator,
    log_error,
    log_to_cli,
)

class CowGenerator(BaseGenerator):
    class_name = "CowGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.COW
        self.price_generator = PriceGenerator()
    
    def bind_db_to_repos(self):
        self.cow_trade_repo = CowTradeRepository(DBSession)
        self.cow_blockchain_transaction_repo = CowBlockchainTransactionRepository(DBSession)
        self.cow_cross_chain_token_transfers_repo = CowCrossChainTransactionRepository(
            DBSession
        )
        self.native_token_repo = NativeTokenRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.token_metadata_repo = TokenMetadataRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "create_cross_chain_transactions"

        try:
            self.match_token_transfers()

            start_ts = int(self.transactions_repo.get_min_timestamp()) - 86400
            end_ts = int(self.transactions_repo.get_max_timestamp()) + 86400

            self.price_generator.populate_native_tokens(
                self.bridge,
                self.native_token_repo,
                self.token_metadata_repo,
                self.token_price_repo,
                start_ts,
                end_ts,
            )
            cctxs = self.cow_cross_chain_token_transfers_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)

            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cow_cross_chain_token_transfers_repo,
                "cow_cross_chain_transactions",
                "input_amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "input_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cow_cross_chain_token_transfers_repo,
                "cow_cross_chain_transactions",
                "output_amount",
                "dst_blockchain",
                "dst_contract_address",
                "src_timestamp",
                "output_amount_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cow_cross_chain_token_transfers_repo,
                "cow_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cow_cross_chain_token_transfers_repo,
                "cow_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "dst_fee",
                "dst_fee_usd",
            )

            self.fix_token_symbol_clashes()
        except Exception as e:
            exception = CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing cross chain transactions. Error: {e}",
            )
            log_error(self.bridge, exception)

    def match_token_transfers(self):
        func_name = "match_token_transfers"

        start_time = time.time()
        log_to_cli(build_log_message_generator(self.bridge, "Matching token transfers..."))

        self.cow_cross_chain_token_transfers_repo.empty_table()

        query = text(
            """
            INSERT INTO cow_cross_chain_transactions (
                src_blockchain,
                src_transaction_hash,
                src_from_address,
                src_to_address,
                src_fee,
                src_timestamp,
                dst_blockchain,
                dst_transaction_hash,
                dst_from_address,
                dst_to_address,
                dst_fee,
                dst_timestamp,
                trade_id,
                owner,
                sell_token,
                buy_token,
                sell_amount,
                buy_amount,
                fee_amount,
                app_data,
                valid_to,
                order_kind,
                price_info,
                timestamp,
                src_contract_address,
                dst_contract_address,
                input_amount,
                output_amount
            )
            SELECT
                trade.blockchain AS src_blockchain,
                trade.transaction_hash AS src_transaction_hash,
                src_tx.from_address AS src_from_address,
                src_tx.to_address AS src_to_address,
                src_tx.fee AS src_fee,
                src_tx.timestamp AS src_timestamp,
                trade.blockchain AS dst_blockchain,
                trade.transaction_hash AS dst_transaction_hash,
                src_tx.from_address AS dst_from_address,
                src_tx.to_address AS dst_to_address,
                src_tx.fee AS dst_fee,
                src_tx.timestamp AS dst_timestamp,
                trade.trade_id,
                trade.owner,
                trade.sell_token,
                trade.buy_token,
                trade.sell_amount,
                trade.buy_amount,
                trade.app_data,
                trade.valid_to,
                trade.order_kind,
                trade.price_info,
                trade.timestamp,
                trade.sell_token AS src_contract_address,
                trade.buy_token AS dst_contract_address,
                trade.sell_amount AS input_amount,
                trade.buy_amount AS output_amount
            FROM cow_trade trade
            JOIN cow_blockchain_transactions src_tx ON src_tx.transaction_hash = trade.transaction_hash
            WHERE src_tx.blockchain = trade.blockchain
            """
        )

        try:
            self.cow_cross_chain_token_transfers_repo.execute(query)

            size = self.cow_cross_chain_token_transfers_repo.get_number_of_records()

            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    (
                        f"Token transfers matched in {end_time - start_time} seconds. "
                        f"Total records inserted: {size}"
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

    def fix_token_symbol_clashes(self):
        func_name = "fix_token_symbol_clashes"

        query = text(
            """
            UPDATE cow_cross_chain_transactions cctx
            SET output_amount_usd = token_price.price_usd * cctx.output_amount / power(10, token_metadata.decimals)
            FROM token_metadata
            JOIN token_price
                ON token_metadata.symbol = token_price.symbol
                AND token_metadata.name = token_price.name
            WHERE lower(cctx.dst_contract_address) = lower(token_metadata.address)
            AND cctx.dst_blockchain = token_metadata.blockchain
            AND CAST(TO_TIMESTAMP(cctx.src_timestamp) AS DATE) = token_price.date
            """
        )

        try:
            self.cow_cross_chain_token_transfers_repo.execute(query)
        except Exception as e:
            raise CustomException(
                PriceGenerator.CLASS_NAME,
                func_name,
                (
                    f"Error processing USD values for symbol clashes in cow_cross_chain_transactions."
                    f"Error: {e}"
                ),
            ) from e