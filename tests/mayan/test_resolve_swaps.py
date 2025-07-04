from extractor.mayan.handler import MayanHandler


def test_3_swaps():
    # 2jVEXxUpgJx6me5nXyX9VGS968FgDPVy5GNcjaho9mBKEcxuKUx1AGAYvqBud9GoTMWmHVDZpuPGeQaXosQTVCey
    swaps = [
        {
            "args": {
                "amm": "SoLFiHG9TfgtdUXUjWAxi3LtvYuFyDLVhBWxdMZxyCe",
                "input_mint": "cbbtcf3aa214zXHbiAZQwf4122FBYbraNdFqgw4iMij",
                "input_amount": "61beb0",
                "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "output_amount": "018f562d9a",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc",
                "input_mint": "cbbtcf3aa214zXHbiAZQwf4122FBYbraNdFqgw4iMij",
                "input_amount": "0adc4d",
                "output_mint": "27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4",
                "output_amount": "09f8fa5f",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo",
                "input_mint": "27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4",
                "input_amount": "09f8fa5f",
                "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "output_amount": "2c5f0251",
            },
            "name": "SwapEvent",
        },
    ]

    result = MayanHandler.resolve_swaps("", swaps)
    assert result == {
        "args": {
            "input_mint": "cbbtcf3aa214zXHbiAZQwf4122FBYbraNdFqgw4iMij",
            "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "input_amount": "0x6c9afd",
            "output_amount": "0x1bbb52feb",
        }
    }


def test_3_agg_swaps():
    # BoqZDVMr7ZK47r2rnJcCGJRX3LmywvswkqEyCkD1UC1HcdbKSNNt2JKSLxNbz547cmCQpRRuRk6qaHbGDTBxtXP
    swaps = [
        {
            "args": {
                "amm": "ZERor4xhbUycZ6gb9ntrhqscUcZmAbQDjEAtCf4hbZY",
                "input_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "input_amount": "0x3B09F493A",
                "output_mint": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
                "output_amount": "0x25439125",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "SoLFiHG9TfgtdUXUjWAxi3LtvYuFyDLVhBWxdMZxyCe",
                "input_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "input_amount": "0x2F3B2A0FB",
                "output_mint": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
                "output_amount": "0x1DCF7DDB",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "PhoeNiXZ8ByJGLkxNfZRnkUfjvmuYqLR89jjFHGqdXY",
                "input_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "input_amount": "0xBCECA83F",
                "output_mint": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
                "output_amount": "0x773CE70",
            },
            "name": "SwapEvent",
        },
    ]

    result = MayanHandler.resolve_swaps("", swaps)
    assert result == {
        "args": {
            "input_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "output_mint": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
            "input_amount": "0x7613e9274",
            "output_amount": "0x4a86dd70",
        }
    }


def test_1_swap():
    # 4D8wroxz46EaBzHwrd3Pyg7W1rDifVTSLjx93KL5Vy7KtM5A2UHGKek3PKepu4hhD4db36xJjKRtVKK3DFcfSLyB
    swaps = [
        {
            "args": {
                "amm": "SoLFiHG9TfgtdUXUjWAxi3LtvYuFyDLVhBWxdMZxyCe",
                "input_mint": "So11111111111111111111111111111111111111112",
                "input_amount": "0x8077B20",
                "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "output_amount": "0x1407A0E",
            },
            "name": "SwapEvent",
        }
    ]

    result = MayanHandler.resolve_swaps("", swaps)
    assert result == {
        "args": {
            "input_mint": "So11111111111111111111111111111111111111112",
            "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "input_amount": "0x8077B20",
            "output_amount": "0x1407A0E",
        }
    }


def test_1_linked_swaps():
    # 4CMPJt8VGYd3nFrss1HRDwua1iRx2dWetiuRWzS69z3fbMcRP1TanxwrmauQaoMmvfh3aAcBEv8j3vBj8k7PvHU2
    swaps = [
        {
            "args": {
                "amm": "2wT8Yq49kHgDzXuPxZSaeLaH1qbmGXtEyPy64bL7aD3c",
                "input_mint": "So11111111111111111111111111111111111111112",
                "input_amount": "0x15712CC",
                "output_mint": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
                "output_amount": "0x356186",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "obriQD1zbpyLz95G5n7nJe6a4DPjpFwa5XYPoNm113y",
                "input_mint": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
                "input_amount": "0x356186",
                "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "output_amount": "0x3568C3",
            },
            "name": "SwapEvent",
        },
    ]

    result = MayanHandler.resolve_swaps("", swaps)
    assert result == {
        "args": {
            "input_mint": "So11111111111111111111111111111111111111112",
            "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "input_amount": "0x15712cc",
            "output_amount": "0x3568c3",
        }
    }


def test_1_linked_and_agg_swaps():
    # 55wrchD5fKuyLpuBKmr3h2uq9Rzt4JLyaYJ7eimVvS7Lxe8YCnzeKd4U3fwkF9JCR9AZwj8RU17jJFK327VuHNSk
    swaps = [
        {
            "args": {
                "amm": "opnb2LAfJYbRMAHHvqjCwQxanZn7ReEHp1k81EohpZb",
                "input_mint": "So11111111111111111111111111111111111111112",
                "input_amount": "0x18AE17A400",
                "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "output_amount": "0x3D9D61D35",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "SoLFiHG9TfgtdUXUjWAxi3LtvYuFyDLVhBWxdMZxyCe",
                "input_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "input_amount": "0x18A55A548",
                "output_mint": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
                "output_amount": "0xFC94E34",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "ZERor4xhbUycZ6gb9ntrhqscUcZmAbQDjEAtCf4hbZY",
                "input_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "input_amount": "0x24F8077ED",
                "output_mint": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
                "output_amount": "0x17ADE68C",
            },
            "name": "SwapEvent",
        },
    ]

    result = MayanHandler.resolve_swaps("", swaps)
    assert result == {
        "args": {
            "input_mint": "So11111111111111111111111111111111111111112",
            "output_mint": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
            "input_amount": "0x18ae17a400",
            "output_amount": "0x277734c0",
        }
    }


def test_4_swaps():
    # 4zUMPu7pQscvmaExW53h45Q5H61uB71kxvN9quwxuLo86Mdrvizhd5YqQMS3XTwKM111HWHhCCusiuCunJBggiWb
    swaps = [
        {
            "args": {
                "amm": "ZERor4xhbUycZ6gb9ntrhqscUcZmAbQDjEAtCf4hbZY",
                "input_mint": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
                "input_amount": "0x5ca079a",
                "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "output_amount": "0x902595de",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "ZERor4xhbUycZ6gb9ntrhqscUcZmAbQDjEAtCf4hbZY",
                "input_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "input_amount": "0x81bb6d47",
                "output_mint": "So11111111111111111111111111111111111111112",
                "output_amount": "0x3577ca10d",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "opnb2LAfJYbRMAHHvqjCwQxanZn7ReEHp1k81EohpZb",
                "input_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "input_amount": "0xe6a2897",
                "output_mint": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
                "output_amount": "0xe680ca0",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "2wT8Yq49kHgDzXuPxZSaeLaH1qbmGXtEyPy64bL7aD3c",
                "input_mint": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
                "input_amount": "0xe680ca0",
                "output_mint": "So11111111111111111111111111111111111111112",
                "output_amount": "0x5f0db6f3",
            },
            "name": "SwapEvent",
        },
    ]

    result = MayanHandler.resolve_swaps("", swaps)
    assert result == {
        "args": {
            "input_mint": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
            "output_mint": "So11111111111111111111111111111111111111112",
            "input_amount": "0x5ca079a",
            "output_amount": "0x3b68a5800",
        }
    }


def test_4_swaps_linkable():
    # SfSV2aKav4KMGqzEvHM7LvUqBdsGKoEZQMeQ6GEC6zhegJzT48BDePih7JTM3R2mR62442pr6Yn1pMHomZa6Nhr
    swaps = [
        {
            "args": {
                "amm": "SoLFiHG9TfgtdUXUjWAxi3LtvYuFyDLVhBWxdMZxyCe",
                "input_mint": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
                "input_amount": "0x6298dbc",
                "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "output_amount": "0x9c8a005f",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "PhoeNiXZ8ByJGLkxNfZRnkUfjvmuYqLR89jjFHGqdXY",
                "input_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "input_amount": "0x7d3b337f",
                "output_mint": "KENJSUYLASHUMfHyy5o4Hp2FdNqZg1AsUPhfH2kYvEP",
                "output_amount": "0x7ea51cb00",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "2wT8Yq49kHgDzXuPxZSaeLaH1qbmGXtEyPy64bL7aD3c",
                "input_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "input_amount": "0x1f4ecce0",
                "output_mint": "So11111111111111111111111111111111111111112",
                "output_amount": "0xccc6267f",
            },
            "name": "SwapEvent",
        },
        {
            "args": {
                "amm": "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8",
                "input_mint": "So11111111111111111111111111111111111111112",
                "input_amount": "0xccc6267f",
                "output_mint": "KENJSUYLASHUMfHyy5o4Hp2FdNqZg1AsUPhfH2kYvEP",
                "output_amount": "0x1f9df046f",
            },
            "name": "SwapEvent",
        },
    ]

    result = MayanHandler.resolve_swaps("", swaps)
    assert result == {
        "args": {
            "input_mint": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
            "output_mint": "KENJSUYLASHUMfHyy5o4Hp2FdNqZg1AsUPhfH2kYvEP",
            "input_amount": "0x6298dbc",
            "output_amount": "0x9e430cf6f",
        }
    }
