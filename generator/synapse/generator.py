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
from repository.synapse.repository import (
    SynapseBlockchainTransactionRepository,
    SynapseTokenDepositAndSwapRepository,
    SynapseTokenMintAndSwapRepository,
)
from utils.utils import (
    CliColor,
    CustomException,
    build_log_message_generator,
    log_error,
    log_to_cli,
)


class SynapseGenerator(BaseGenerator):
    CLASS_NAME = "SynapseGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.SYNAPSE
        self.price_generator = PriceGenerator()

    def bind_db_to_repos(self):
        self.blockchain_tx_repo = SynapseBlockchainTransactionRepository(DBSession)
        self.deposit_and_swap_repo = SynapseTokenDepositAndSwapRepository(DBSession)
        self.mint_and_swap_repo = SynapseTokenMintAndSwapRepository(DBSession)

        self.token_metadata_repo = TokenMetadataRepository(DBSession)
        self.token_price_repo = TokenPriceRepository(DBSession)
        self.native_token_repo = NativeTokenRepository(DBSession)

    def generate_cross_chain_data(self):
        func_name = "generate_cross_chain_data"
        try:
            self.match_deposit_mint_swaps()

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

            cctxs = self.get_unique_src_dst_contract_pairs()
            self.populate_token_info_tables(cctxs, start_ts, end_ts)
            self.backfill_token_symbols()

            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self,
                "synapse_cross_chain_transactions",
                "input_amount",
                "src_blockchain",
                "src_contract_address",
                "src_timestamp",
                "input_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self,
                "synapse_cross_chain_transactions",
                "output_amount",
                "dst_blockchain",
                "dst_contract_address",
                "dst_timestamp",
                "output_amount_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self,
                "synapse_cross_chain_transactions",
                "src_timestamp",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self,
                "synapse_cross_chain_transactions",
                "dst_timestamp",
                "dst_blockchain",
                "dst_fee",
                "dst_fee_usd",
            )
        except Exception as e:
            exception = CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error generating Synapse cross chain transactions: {e}",
            )
            log_error(self.bridge, exception)

    def match_deposit_mint_swaps(self):
        func_name = "match_deposit_mint_swaps"
        start_time = time.time()
        log_to_cli(build_log_message_generator(self.bridge, "Matching DepositAndSwap -> MintAndSwap..."))

        self.empty_cctx_table()

        query = text(
            """
            INSERT INTO synapse_cross_chain_transactions (
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
                recipient,
                src_contract_address,
                src_token,
                dst_contract_address,
                dst_token,
                input_amount,
                input_amount_usd,
                output_amount,
                output_amount_usd,
                swap_success,
                kappa
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
                dst_tx.to_address as dst_to_address,
                dst_tx.fee as dst_fee,
                NULL as dst_fee_usd,
                dst_tx.timestamp as dst_timestamp,
                src_ev.to_address as recipient,
                src_ev.token as src_contract_address,
                tm_src.symbol as src_token,
                dst_ev.token as dst_contract_address,
                tm_dst.symbol as dst_token,
                src_ev.amount as input_amount,
                NULL as input_amount_usd,
                dst_ev.amount as output_amount,
                NULL as output_amount_usd,
                dst_ev.swap_success as swap_success,
                dst_ev.kappa as kappa
            FROM synapse_token_deposit_and_swap src_ev
            JOIN synapse_blockchain_transactions src_tx ON src_tx.transaction_hash = src_ev.transaction_hash
            JOIN synapse_token_mint_and_swap dst_ev ON REPLACE(lower(dst_ev.kappa), '0x', '') = REPLACE(lower(src_ev.kappa), '0x', '')
            JOIN synapse_blockchain_transactions dst_tx ON dst_tx.transaction_hash = dst_ev.transaction_hash
            LEFT JOIN token_metadata tm_src ON tm_src.blockchain = src_tx.blockchain AND lower(tm_src.address) = lower(src_ev.token)
            LEFT JOIN token_metadata tm_dst ON tm_dst.blockchain = dst_tx.blockchain AND lower(tm_dst.address) = lower(dst_ev.token)
            WHERE ABS(CAST(dst_tx.timestamp AS BIGINT) - CAST(src_tx.timestamp AS BIGINT)) <= 86400;
            """
        )

        try:
            self.execute(query)
            size = self.get_number_of_records()
            end_time = time.time()
            log_to_cli(
                build_log_message_generator(
                    self.bridge,
                    (
                        f"Deposit/Mint swaps matched in {end_time - start_time} seconds. "
                        f"Total records inserted: {size}"
                    ),
                ),
                CliColor.SUCCESS,
            )
        except Exception as e:
            raise CustomException(
                self.CLASS_NAME,
                func_name,
                f"Error processing Deposit/Mint swaps. Error: {e}",
            ) from e

    def get_number_of_records(self):
        with DBSession() as session:
            res = session.execute(text("SELECT COUNT(1) FROM synapse_cross_chain_transactions"))
            return res.scalar() or 0

    def empty_cctx_table(self):
        with DBSession() as session:
            session.execute(text("DELETE FROM synapse_cross_chain_transactions"))
            session.commit()

    def get_unique_src_dst_contract_pairs(self):
        with DBSession() as session:
            sql = text(
                """
                SELECT DISTINCT
                    src_blockchain,
                    src_contract_address,
                    dst_blockchain,
                    dst_contract_address
                FROM synapse_cross_chain_transactions
                """
            )
            rows = session.execute(sql).all()
            class Row:
                def __init__(self, t):
                    (self.src_blockchain, self.src_contract_address, self.dst_blockchain, self.dst_contract_address) = t
            return [Row(r) for r in rows]

    def execute(self, query):
        with DBSession() as session:
            session.execute(query)
            session.commit()

    def get_total_amount_usd_transacted(self):
        with DBSession() as session:
            res = session.execute(
                text("SELECT SUM(input_amount_usd) FROM synapse_cross_chain_transactions")
            )
            return res.scalar() or 0

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

    def backfill_token_symbols(self):
        # Ensure src_token/dst_token get filled after token_metadata is available
        with DBSession() as session:
            session.execute(
                text(
                    """
                    UPDATE synapse_cross_chain_transactions c
                    SET src_token = tm.symbol
                    FROM token_metadata tm
                    WHERE c.src_token IS NULL
                      AND c.src_contract_address IS NOT NULL
                      AND lower(tm.address) = lower(c.src_contract_address)
                      AND tm.blockchain = c.src_blockchain;
                    """
                )
            )
            session.execute(
                text(
                    """
                    UPDATE synapse_cross_chain_transactions c
                    SET dst_token = tm.symbol
                    FROM token_metadata tm
                    WHERE c.dst_token IS NULL
                      AND c.dst_contract_address IS NOT NULL
                      AND lower(tm.address) = lower(c.dst_contract_address)
                      AND tm.blockchain = c.dst_blockchain;
                    """
                )
            )
            session.commit()
