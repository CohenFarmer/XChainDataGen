import time

from sqlalchemy import text

from config.constants import Bridge
from generator.base_generator import BaseGenerator
from generator.common.price_generator import PriceGenerator
from repository.database import DBSession
from repository.fly.repository import (
    FlyBlockchainTransactionRepository,
    FlyCrossChainTransactionRepository,
    FlyDepositRepository,
    FlySwapInRepository,
    FlySwapOutRepository,
)
from repository.common.repository import (
    NativeTokenRepository,
    TokenMetadataRepository,
    TokenPriceRepository,
)
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message_generator,
    log_error,
    log_to_cli,
)


class FlyGenerator(BaseGenerator):
    CLASS_NAME = "FlyGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.FLY
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.transactions_repo = FlyBlockchainTransactionRepository(DBSession)
        self.swap_in_repo = FlySwapInRepository(DBSession)
        self.swap_out_repo = FlySwapOutRepository(DBSession)
        self.deposit_repo = FlyDepositRepository(DBSession)
        self.cctx_repo = FlyCrossChainTransactionRepository(DBSession)

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "generate_cross_chain_data"
        try:
            self.match_token_transfers()

            start_ts = int(self.transactions_repo.get_min_timestamp()) - 86400
            end_ts = int(self.transactions_repo.get_max_timestamp()) + 86400

            #Populate native tokens (needed for fee USD calc)
            self.price_generator.populate_native_tokens(
                self.bridge,
                self.native_token_repo,
                self.token_metadata_repo,
                self.token_price_repo,
                start_ts,
                end_ts,
            )

            cctxs = self.cctx_repo.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)

            #USD amounts for tokens and fees
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cctx_repo,
                "fly_cross_chain_transactions",
                "input_amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "input_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cctx_repo,
                "fly_cross_chain_transactions",
                "output_amount",
                "dst_blockchain",
                "dst_contract_address",
                "dst_timestamp",
                "output_amount_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cctx_repo,
                "fly_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cctx_repo,
                "fly_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "dst_fee",
                "dst_fee_usd",
            )

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

        self.cctx_repo.empty_table()

        # Ensure new human-readable date columns exist on older databases
        try:
            self.cctx_repo.execute(
                text(
                    "ALTER TABLE fly_cross_chain_transactions ADD COLUMN IF NOT EXISTS src_date VARCHAR(10);"
                )
            )
            self.cctx_repo.execute(
                text(
                    "ALTER TABLE fly_cross_chain_transactions ADD COLUMN IF NOT EXISTS dst_date VARCHAR(10);"
                )
            )
        except Exception:
            # If the DB doesn't support IF NOT EXISTS or lacks permissions, continue without failing.
            pass

        # Join strategy:
        #SwapIn (source) joined with FlyBlockchainTransaction for src tx meta
        #SwapOut (dest) joined by deposit_data_hash with SwapIn
        #Deposit is optional informational; linkage also by deposit_data_hash
        query = text(
            """
            INSERT INTO fly_cross_chain_transactions (
                deposit_data_hash,
                src_blockchain,
                src_transaction_hash,
                src_from_address,
                src_to_address,
                src_fee,
                src_fee_usd,
                src_timestamp,
                src_date,
                dst_blockchain,
                dst_transaction_hash,
                dst_from_address,
                dst_to_address,
                dst_fee,
                dst_fee_usd,
                dst_timestamp,
                dst_date,
                src_contract_address,
                dst_contract_address,
                input_amount,
                input_amount_usd,
                output_amount,
                output_amount_usd
            )
            SELECT
                si.deposit_data_hash,
                si.blockchain as src_blockchain,
                si.transaction_hash as src_transaction_hash,
                stx.from_address as src_from_address,
                stx.to_address as src_to_address,
                stx.fee as src_fee,
                NULL as src_fee_usd,
                stx.timestamp as src_timestamp,
                TO_CHAR(TO_TIMESTAMP(stx.timestamp), 'DD/MM/YY') as src_date,
                so.blockchain as dst_blockchain,
                so.transaction_hash as dst_transaction_hash,
                dtx.from_address as dst_from_address,
                dtx.to_address as dst_to_address,
                dtx.fee as dst_fee,
                NULL as dst_fee_usd,
                dtx.timestamp as dst_timestamp,
                TO_CHAR(TO_TIMESTAMP(dtx.timestamp), 'DD/MM/YY') as dst_date,
                si.from_asset_address as src_contract_address,
                so.to_asset_address as dst_contract_address,
                si.amount_in as input_amount,
                NULL as input_amount_usd,
                so.amount_out as output_amount,
                NULL as output_amount_usd
            FROM fly_swap_in si
            JOIN fly_blockchain_transactions stx ON stx.transaction_hash = si.transaction_hash
            JOIN fly_swap_out so ON lower(so.deposit_data_hash) = lower(si.deposit_data_hash)
            JOIN fly_blockchain_transactions dtx ON dtx.transaction_hash = so.transaction_hash;
            """
        )

        try:
            self.cctx_repo.execute(query)
            size = self.cctx_repo.get_number_of_records()

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
