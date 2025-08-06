import argparse

from cli import Cli


def test_extract_data():
    print("COW Starting data extraction test...")
    args = argparse.Namespace(
        blockchains=["ethereum", "arbitrum", "polygon", "optimism", "base"],
        bridge="cow",
        start_ts=1733011200,  # 1st Dec 2024 00:00
        end_ts=1733011800  # 1st Dec 2024 01:00
    )

    Cli.extract_data(args)

    # now we can check if the data was extracted correctly
    # For example, we can check if the AcrossV3FundsDeposited table has been populated
    from repository.cow.repository import (
        CowTradeRepository,
    )
    from repository.database import DBSession

    cow_trade_repo = CowTradeRepository(DBSession)

    events = cow_trade_repo.get_all()
    print(f"Number of events in cow_trade_repo: {len(events)}")
    """assert len(events) == 911, (
        "Expected 911 events in AcrossV3FundsDepositedRepository table after extraction."
    )"""

    args = argparse.Namespace(
        bridge="cow",
    )
    Cli.generate_data(args)

    # Here we can check if the data was generated correctly
    from repository.cow.repository import CowCrossChainTransactionRepository
    from repository.database import DBSession

    cow_cross_chain_transactions_repo = CowCrossChainTransactionRepository(DBSession)
    transactions = cow_cross_chain_transactions_repo.get_all()

    print(f"Number of transactions in CowCrossChainTransaction: {len(transactions)}")

test_extract_data()