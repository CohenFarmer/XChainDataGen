import argparse

from cli import Cli

def test_extract_and_generate_router():
    print("Starting Router data extraction test...")
    args = argparse.Namespace(
        blockchains=["ethereum", "arbitrum", "optimism", "base", "polygon", "bnb", "avalanche"],
        bridge="router",
        start_ts=1733011200,  # 1st Dec 2024 00:00
        end_ts=1733616000 # 2nd Dec 2024 00:00
    )

    Cli.extract_data(args)

    from repository.router.repository import (
        RouterFundsDepositedRepository,
        RouterFundsPaidRepository,
        RouterBlockchainTransactionRepository,
        RouterCrossChainTransactionRepository,
    )
    from repository.database import DBSession

    funds_deposited_repo = RouterFundsDepositedRepository(DBSession)
    funds_paid_repo = RouterFundsPaidRepository(DBSession)
    blockchain_tx_repo = RouterBlockchainTransactionRepository(DBSession)

    deposited_events = funds_deposited_repo.get_all()
    paid_events = funds_paid_repo.get_all()
    tx_events = blockchain_tx_repo.get_all()

    print(f"RouterFundsDeposited events: {len(deposited_events)}")
    print(f"RouterFundsPaid events: {len(paid_events)}")
    print(f"RouterBlockchainTransaction events: {len(tx_events)}")

    gen_args = argparse.Namespace(bridge="router")
    Cli.generate_data(gen_args)

    cctx_repo = RouterCrossChainTransactionRepository(DBSession)
    cctxs = cctx_repo.get_all()
    print(f"RouterCrossChainTransaction rows: {len(cctxs)}")


test_extract_and_generate_router()
