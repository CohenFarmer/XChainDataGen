import os
import time
import traceback

from jinja2 import clear_caches
from sqlalchemy import text

from collections import defaultdict

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
from generator.cow.cow_api import get_order

import random

class CowGenerator(BaseGenerator):
    class_name = "CowGenerator"

    def __init__(self) -> None:
        super().__init__()
        self.bridge = Bridge.COW
        self.price_generator = PriceGenerator()

    def enrich_trades_with_cross_chain_key(self):
        func_name = "enrich_trades_with_cross_chain_key"
        try:
            batch = 0
            limit = 5000
            while True:
                to_process = list(self.cow_trade_repo.iter_missing_cross_chain_key(limit=limit))
                if not to_process:
                    break
                batch += 1
                for r in to_process:
                    order = get_order(r.blockchain, r.trade_id)
                    app_data = order.get("appData") if order else None
                    app_data_cid = order.get("appDataCid") if order else None

                    
                    cross_chain_key = app_data_cid or app_data

                    self.cow_trade_repo.set_cross_chain_fields(r.blockchain, r.trade_id, app_data, app_data_cid, cross_chain_key)
              
                if len(to_process) < limit:
                    break
        except Exception as e:
            tb = traceback.format_exc()
            raise CustomException(self.class_name, func_name, f"Failed enriching trades: {type(e).__name__}: {e}\n{tb}") from e

    def backfill_missing_appdata(self):
        func_name = "backfill_missing_appdata"
        try:
            limit = 5000
            while True:
                to_process = list(self.cow_trade_repo.iter_missing_appdata(limit=limit))
                if not to_process:
                    break
                for t in to_process:
                    order = get_order(t.blockchain, t.trade_id)
                    if not order:
                        continue
                    app_data = order.get("appData")
                    app_data_cid = order.get("appDataCid")
                    self.cow_trade_repo.update_appdata_fields_if_missing(t.blockchain, t.trade_id, app_data, app_data_cid)
                if len(to_process) < limit:
                    break
        except Exception as e:
            tb = traceback.format_exc()
            raise CustomException(self.class_name, func_name, f"Failed backfilling appdata: {type(e).__name__}: {e}\n{tb}") from e

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
            self.bind_db_to_repos()

            max_passes = 2
            prev_missing = None
            for _ in range(max_passes):
                self.enrich_trades_with_cross_chain_key()
            
                remaining = sum(1 for _ in self.cow_trade_repo.iter_missing_appdata(limit=100000))
                if prev_missing is not None and remaining >= prev_missing:
                    break
                if remaining == 0:
                    break
                prev_missing = remaining
                time.sleep(0.5)
            self.match_token_transfers()
        
            self.backfill_missing_appdata()

            min_ts = self.cow_blockchain_transaction_repo.get_min_timestamp()
            max_ts = self.cow_blockchain_transaction_repo.get_max_timestamp()
            if not min_ts or not max_ts:
                log_to_cli(build_log_message_generator(self.bridge, "No blockchain tx timestamps found; skipping pricing."), CliColor.INFO)
                return

            start_ts = int(min_ts) - 86400
            end_ts = int(max_ts) + 86400

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
                "sell_amount",
                "src_blockchain",
                "sell_token",        
                "src_valid_to",
                "sell_amount_usd",
            )
            PriceGenerator.calculate_cctx_usd_values(
                self.bridge,
                self.cow_cross_chain_token_transfers_repo,
                "cow_cross_chain_transactions",
                "buy_amount",
                "dst_blockchain",
                "buy_token",         
                "dst_valid_to",
                "buy_amount_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cow_cross_chain_token_transfers_repo,
                "cow_cross_chain_transactions",
                "src_valid_to",
                "src_blockchain",
                "src_fee",
                "src_fee_usd",
            )
            PriceGenerator.calculate_cctx_native_usd_values(
                self.bridge,
                self.cow_cross_chain_token_transfers_repo,
                "cow_cross_chain_transactions",
                "dst_valid_to",
                "dst_blockchain",
                "dst_fee",
                "dst_fee_usd",
            )
        except Exception as e:
            tb = traceback.format_exc()
            exception = CustomException(
                self.class_name,
                func_name,
                f"Error processing cross chain transactions. {type(e).__name__}: {e}\n{tb}",
            )
            log_error(self.bridge, exception)

    def match_token_transfers(self):
        func_name = "match_token_transfers"
        try:
            self.enrich_trades_with_cross_chain_key()

            query = text("""
                WITH src_tx AS (
                    SELECT blockchain, lower(transaction_hash) AS txh, MIN(fee) AS fee
                    FROM cow_blockchain_transactions
                    GROUP BY 1,2
                ),
                dst_tx AS (
                    SELECT blockchain, lower(transaction_hash) AS txh, MIN(fee) AS fee
                    FROM cow_blockchain_transactions
                    GROUP BY 1,2
                )
                INSERT INTO cow_cross_chain_transactions (
                    src_blockchain, src_transaction_hash, src_owner, src_fee, src_fee_usd,
                    dst_blockchain, dst_transaction_hash, dst_owner, dst_fee, dst_fee_usd,
                    trade_id, sell_token, buy_token, sell_amount, sell_amount_usd,
                    buy_amount, buy_amount_usd, src_valid_to, dst_valid_to
                )
                SELECT DISTINCT ON (src_trade.trade_id, src_trade.blockchain, dst_trade.blockchain)
                    src_trade.blockchain,
                    src_trade.transaction_hash,
                    src_trade.owner,
                    s.fee,
                    NULL,
                    dst_trade.blockchain,
                    dst_trade.transaction_hash,
                    dst_trade.owner,
                    d.fee,
                    NULL,
                    src_trade.trade_id,
                    src_trade.sell_token,
                    src_trade.buy_token,
                    src_trade.sell_amount,
                    NULL,
                    dst_trade.buy_amount,
                    NULL,
                    src_trade.valid_to,
                    dst_trade.valid_to
                FROM cow_trade src_trade
                JOIN cow_trade dst_trade
                  ON src_trade.cross_chain_key IS NOT NULL
                 AND src_trade.cross_chain_key = dst_trade.cross_chain_key
                 AND src_trade.blockchain < dst_trade.blockchain
                LEFT JOIN src_tx s
                  ON s.txh = lower(src_trade.transaction_hash)
                 AND s.blockchain = src_trade.blockchain
                LEFT JOIN dst_tx d
                  ON d.txh = lower(dst_trade.transaction_hash)
                 AND d.blockchain = dst_trade.blockchain
                ORDER BY
                  src_trade.trade_id,
                  src_trade.blockchain,
                  dst_trade.blockchain,
                  src_trade.log_index
                ON CONFLICT ON CONSTRAINT uq_cow_cctx_triplet DO NOTHING
            """)
            with DBSession() as session:
                result = session.execute(query)
                session.commit()
                inserted = result.rowcount or 0
            log_to_cli(build_log_message_generator(self.bridge, f"Token transfers matched. Total records inserted: {inserted}"))
        except Exception as e:
            tb = traceback.format_exc()
            raise CustomException(self.class_name, func_name, f"Error processing token transfers. {type(e).__name__}: {e}\n{tb}") from e

    def populate_token_info_tables(self, cctxs, start_ts, end_ts):
        start_time = time.time()
        log_to_cli(build_log_message_generator(self.bridge, "Fetching token prices..."))

        for cctx in cctxs:
            try:
                src_blockchain = getattr(cctx, "src_blockchain", None) or cctx[0]
                sell_token = getattr(cctx, "sell_token", None) or cctx[1]
                dst_blockchain = getattr(cctx, "dst_blockchain", None) or cctx[2]
                buy_token = getattr(cctx, "buy_token", None) or cctx[3]
            except Exception:
                continue

            self.price_generator.populate_token_info(
                self.bridge,
                self.token_metadata_repo,
                self.token_price_repo,
                src_blockchain,
                dst_blockchain,
                sell_token,
                buy_token,
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

    '''def fix_token_symbol_clashes(self):
        func_name = "fix_token_symbol_clashes"

        query = text(
            """
            UPDATE cow_cross_chain_transactions cctx
            SET output_amount_usd = token_price.price_usd * cctx.output_amount / power(10, token_metadata.decimals)
            FROM token_metadata
            JOIN token_price
                ON token_metadata.symbol = token_price.symbol
                AND token_metadata.name = token_price.name
            WHERE lower(cctx.dst_owner) = lower(token_metadata.address)
            AND cctx.dst_blockchain = token_metadata.blockchain
            AND CAST(TO_TIMESTAMP(cctx.src_timestamp) AS DATE) = token_price.date
            """
        )

        try:
            self.cow_cross_chain_token_transfers_repo.execute(query)
        except Exception as e:
            raise CustomException(
                PriceGenerator.class_name,
                func_name,
                (
                    f"Error processing USD values for symbol clashes in cow_cross_chain_transactions."
                    f"Error: {e}"
                ),
            ) from e*/'''