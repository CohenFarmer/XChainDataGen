import argparse

from cli import Cli


def test_extract_and_generate_eco():
    print("Starting ECO data extraction test...")
    args = argparse.Namespace(
        blockchains=["ethereum", "base", "optimism", "polygon", "arbitrum"],
        bridge="eco",
        start_ts=1751292000,  # 1st of July 2025 00:00
        end_ts=  1751368400
        #end_ts= 1753970400  # 1st of August 2025 00:00
    )

    Cli.extract_data(args)

    from repository.eco.repository import (
        EcoIntentCreatedRepository,
        EcoFulfillmentRepository,
        EcoBlockchainTransactionRepository,
        EcoCrossChainTransactionRepository,
    )
    from repository.database import DBSession

    intent_repo = EcoIntentCreatedRepository(DBSession)
    fulfillment_repo = EcoFulfillmentRepository(DBSession)
    blockchain_tx_repo = EcoBlockchainTransactionRepository(DBSession)

    ic_events = intent_repo.get_all()
    f_events = fulfillment_repo.get_all()
    tx_events = blockchain_tx_repo.get_all()

    print(f"EcoIntentCreated events: {len(ic_events)}")
    print(f"EcoFulfillment events: {len(f_events)}")
    print(f"EcoBlockchainTransaction events: {len(tx_events)}")

    gen_args = argparse.Namespace(bridge="eco")
    Cli.generate_data(gen_args)

    cctx_repo = EcoCrossChainTransactionRepository(DBSession)
    cctxs = cctx_repo.get_all()
    print(f"EcoCrossChainTransaction rows: {len(cctxs)}")


test_extract_and_generate_eco()
