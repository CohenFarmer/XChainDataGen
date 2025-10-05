import argparse

from cli import Cli


def test_extract_and_generate_synapse():
    print("Starting Synapse data extraction test...")
    args = argparse.Namespace(
        blockchains=["ethereum", "arbitrum", "optimism", "base", "polygon", "avalanche"],
        bridge="synapse",
        start_ts=1756652400,
        end_ts=	1759244400,  
    )


    Cli.extract_data(args)

    from repository.synapse.repository import (
        SynapseTokenDepositAndSwapRepository,
        SynapseTokenMintAndSwapRepository,
        SynapseBlockchainTransactionRepository,
    )
    from repository.database import DBSession

    deposit_repo = SynapseTokenDepositAndSwapRepository(DBSession)
    mint_repo = SynapseTokenMintAndSwapRepository(DBSession)
    tx_repo = SynapseBlockchainTransactionRepository(DBSession)

    deposits = deposit_repo.get_all()
    mints = mint_repo.get_all()
    txs = tx_repo.get_all()

    print(f"SynapseTokenDepositAndSwap events: {len(deposits)}")
    print(f"SynapseTokenMintAndSwap events: {len(mints)}")
    print(f"SynapseBlockchainTransaction rows: {len(txs)}")

    #Generate
    gen_args = argparse.Namespace(bridge="synapse")
    Cli.generate_data(gen_args)

    from repository.synapse.models import SynapseCrossChainTransaction
    from repository.database import DBSession as _DB
    with _DB() as session:
        rows = session.query(SynapseCrossChainTransaction).all()
        print(f"SynapseCrossChainTransaction rows: {len(rows)}")
        if rows:
            r = rows[0]
            _ = (
                r.src_blockchain,
                r.dst_blockchain,
                r.input_amount,
                r.output_amount,
                r.swap_success,
                r.src_token,
                r.dst_token,
                r.kappa,
            )


test_extract_and_generate_synapse()
