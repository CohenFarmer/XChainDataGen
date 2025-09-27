import argparse

from cli import Cli


def test_extract_data():
    print("Wormhole Starting data extraction test...")
    args = argparse.Namespace(
        blockchains=["ethereum", "arbitrum", "polygon", "optimism", "base", "avalanche", "bnb", "scroll"],
        bridge="wormhole",
        start_ts=1733011200,  # 1st of July 2025 00:00
        end_ts=1733097600
        #end_ts=1735653600  # 1st of August 2025 00:00
    )

    Cli.extract_data(args)
    
    from repository.wormhole.repository import (
        WormholePublishedRepository,
        WormholeRedeemedRepository,
    WormholeCrossChainTransactionRepository,
    )


    from repository.database import DBSession

    published_repo = WormholePublishedRepository(DBSession)
    redeemed_repo = WormholeRedeemedRepository(DBSession)

    events_pub = published_repo.get_all()
    events_red = redeemed_repo.get_all()
    print(f"Published: {len(events_pub)}; Redeemed: {len(events_red)}")

    args = argparse.Namespace(
        bridge="wormhole",
    )
    Cli.generate_data(args)
    cctx_repo = WormholeCrossChainTransactionRepository(DBSession)

    cctxs = cctx_repo.get_all()
    print(f"Wormhole CCTX rows: {len(cctxs)}")

test_extract_data()