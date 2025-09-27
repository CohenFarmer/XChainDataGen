import time

from sqlalchemy import text

from config.constants import Bridge
from generator.base_generator import BaseGenerator
from generator.common.price_generator import PriceGenerator
from repository.common.repository import (
    NativeTokenRepository,
    TokenMetadataRepository,
    TokenPriceRepository,
)
from repository.database import DBSession
from repository.eco.repository import (
    EcoBlockchainTransactionRepository,
    EcoIntentCreatedRepository,
    EcoFulfillmentRepository,
    EcoCrossChainTransactionRepository,
)
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message_generator,
    log_error,
    log_to_cli,
)


class EcoGenerator(BaseGenerator):
    CLASS_NAME = "EcoGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.ECO
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.blockchain_tx_repo = EcoBlockchainTransactionRepository(DBSession)
        self.intent_created_repo = EcoIntentCreatedRepository(DBSession)
        self.fulfillment_repo = EcoFulfillmentRepository(DBSession)
        self.cctx_repo = EcoCrossChainTransactionRepository(DBSession)

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "generate_cross_chain_data"
        try:
            self.match_transfers()

            start_ts = int(self.blockchain_tx_repo.get_min_timestamp()) - 86400
            end_ts = int(self.blockchain_tx_repo.get_max_timestamp()) + 86400

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

            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cctx_repo,
                "eco_cross_chain_transactions",
                "input_amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "input_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cctx_repo,
                "eco_cross_chain_transactions",
                "output_amount",
                "dst_blockchain",
                "dst_contract_address",
                "src_timestamp",
                "output_amount_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cctx_repo,
                "eco_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cctx_repo,
                "eco_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "dst_fee",
                "dst_fee_usd",
            )
        except Exception as e:
            exception = CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error generating ECO cross chain transactions: {e}",
            )
            log_error(self.bridge, exception)

    def match_transfers(self):
        func_name = "match_transfers"
        start_time = time.time()
        log_to_cli(build_log_message_generator(self.bridge, "Matching transactions..."))

        self.cctx_repo.empty_table()

        #join on intent_hash between source-side IntentCreated and dest-side Fulfillment
        query = text(
            """
            INSERT INTO eco_cross_chain_transactions (
                src_blockchain,
                src_transaction_hash,
                src_from_address,
                src_to_address,
                src_fee,
                src_fee_usd,
                src_timestamp,
                dst_blockchain,
                dst_transaction_hash,
                dst_from_address,
                dst_to_address,
                dst_fee,
                dst_fee_usd,
                dst_timestamp,
                src_contract_address,
                dst_contract_address,
                input_amount,
                input_amount_usd,
                output_amount,
                output_amount_usd,
                intent_hash
            )
            SELECT
                src_tx.blockchain as src_blockchain,
                src_tx.transaction_hash as src_transaction_hash,
                src_tx.from_address as src_from_address,
                src_tx.to_address as src_to_address,
                src_tx.fee as src_fee,
                NULL as src_fee_usd,
                src_tx.timestamp as src_timestamp,
                dst_tx.blockchain as dst_blockchain,
                dst_tx.transaction_hash as dst_transaction_hash,
                dst_tx.from_address as dst_from_address,
                f.claimant as dst_to_address,
                dst_tx.fee as dst_fee,
                NULL as dst_fee_usd,
                dst_tx.timestamp as dst_timestamp,
                ic.inbox as src_contract_address,
                dst_tx.to_address as dst_contract_address,
                ic.native_value as input_amount,
                NULL as input_amount_usd,
                ic.native_value as output_amount,
                NULL as output_amount_usd,
                ic.intent_hash as intent_hash
            FROM eco_intent_created ic
            JOIN eco_blockchain_transactions src_tx ON src_tx.transaction_hash = ic.transaction_hash
            JOIN eco_fulfillment f ON f.intent_hash = ic.intent_hash
            JOIN eco_blockchain_transactions dst_tx ON dst_tx.transaction_hash = f.transaction_hash;
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
                        f"Transactions matched in {end_time - start_time} seconds. "
                        f"Total records inserted: {size}"
                    ),
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing transactions. Error: {e}",
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
