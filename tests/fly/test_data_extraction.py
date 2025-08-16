import argparse

from cli import Cli


def test_extract_data():
    print("FLY Starting data extraction test...")
    args = argparse.Namespace(
        blockchains=["ethereum", "arbitrum", "polygon", "optimism", "base", "avalanche"],
        bridge="fly",
        start_ts=1733011200, # 1st Dec 2024 00:00
        end_ts=1733616000 # 8th Dec 2024 00:00
    )

    Cli.extract_data(args)

    from repository.fly.repository import (
        FlySwapInRepository,
        FlySwapOutRepository,
        FlyDepositRepository,
    )
    from repository.database import DBSession

    fly_swap_in_repo = FlySwapInRepository(DBSession)
    fly_swap_out_repo = FlySwapOutRepository(DBSession)
    fly_deposit_repo = FlyDepositRepository(DBSession)

    events = fly_swap_in_repo.get_all()
    print(f"Number of events in fly_swap_in_repo: {len(events)}")

    events = fly_swap_out_repo.get_all()
    print(f"Number of events in fly_swap_out_repo: {len(events)}")

    events = fly_deposit_repo.get_all()
    print(f"Number of events in fly_deposit_repo: {len(events)}")

    print("Generating Data...")
    args = argparse.Namespace(
        bridge="fly",
    )
    Cli.generate_data(args)

    from repository.fly.repository import FlyCrossChainTransactionRepository
    from repository.database import DBSession

    fly_cross_chain_transactions_repo = FlyCrossChainTransactionRepository(DBSession)
    transactions = fly_cross_chain_transactions_repo.get_all()

    print(f"Number of transactions in FlyCrossChainTransaction: {len(transactions)}")

test_extract_data()