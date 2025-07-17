# Mapping of bridges to their supported blockchains and contracts
BRIDGE_CONFIG = {
    "blockchains": {
        "ethereum": [
            {
                "abi": "mayan_swift",
                "contracts": [
                    "0xC38e4e6A15593f908255214653d3D947CA1c2338",  # Mayan Swift
                ],
                "topics": [
                    "0x6ec9b1b5a9f54d929394f18dac4ba1b1cc79823f2266c2d09cab8a3b4700b40b",  # OrderFulfilled
                    "0x918554b6bd6e2895ce6553de5de0e1a69db5289aa0e4fe193a0dcd1f14347477",  # OrderCreated
                    "0x4bdcff348c4d11383c487afb95f732f243d93fbfc478aa736a4981cf6a640911",  # OrderUnlocked
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x337685fdaB40D39bd02028545a4FfA7D287cC3E2",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x0654874eb7F59C6f5b39931FC45dC45337c967c3",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
        ],
        "optimism": [
            {
                "abi": "mayan_swift",
                "contracts": [
                    "0xC38e4e6A15593f908255214653d3D947CA1c2338",  # Mayan Swift
                ],
                "topics": [
                    "0x6ec9b1b5a9f54d929394f18dac4ba1b1cc79823f2266c2d09cab8a3b4700b40b",  # OrderFulfilled
                    "0x918554b6bd6e2895ce6553de5de0e1a69db5289aa0e4fe193a0dcd1f14347477",  # OrderCreated
                    "0x4bdcff348c4d11383c487afb95f732f243d93fbfc478aa736a4981cf6a640911",  # OrderUnlocked
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x337685fdaB40D39bd02028545a4FfA7D287cC3E2",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x0654874eb7F59C6f5b39931FC45dC45337c967c3",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
        ],
        "arbitrum": [
            {
                "abi": "mayan_swift",
                "contracts": [
                    "0xC38e4e6A15593f908255214653d3D947CA1c2338",  # Mayan Swift
                ],
                "topics": [
                    "0x6ec9b1b5a9f54d929394f18dac4ba1b1cc79823f2266c2d09cab8a3b4700b40b",  # OrderFulfilled
                    "0x918554b6bd6e2895ce6553de5de0e1a69db5289aa0e4fe193a0dcd1f14347477",  # OrderCreated
                    "0x4bdcff348c4d11383c487afb95f732f243d93fbfc478aa736a4981cf6a640911",  # OrderUnlocked
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x337685fdaB40D39bd02028545a4FfA7D287cC3E2",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x0654874eb7F59C6f5b39931FC45dC45337c967c3",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
        ],
        "avalanche": [
            {
                "abi": "mayan_swift",
                "contracts": [
                    "0xC38e4e6A15593f908255214653d3D947CA1c2338",  # Mayan Swift
                ],
                "topics": [
                    "0x6ec9b1b5a9f54d929394f18dac4ba1b1cc79823f2266c2d09cab8a3b4700b40b",  # OrderFulfilled
                    "0x918554b6bd6e2895ce6553de5de0e1a69db5289aa0e4fe193a0dcd1f14347477",  # OrderCreated
                    "0x4bdcff348c4d11383c487afb95f732f243d93fbfc478aa736a4981cf6a640911",  # OrderUnlocked
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x337685fdaB40D39bd02028545a4FfA7D287cC3E2",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x0654874eb7F59C6f5b39931FC45dC45337c967c3",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
        ],
        "base": [
            {
                "abi": "mayan_swift",
                "contracts": [
                    "0xC38e4e6A15593f908255214653d3D947CA1c2338",  # Mayan Swift
                ],
                "topics": [
                    "0x6ec9b1b5a9f54d929394f18dac4ba1b1cc79823f2266c2d09cab8a3b4700b40b",  # OrderFulfilled
                    "0x918554b6bd6e2895ce6553de5de0e1a69db5289aa0e4fe193a0dcd1f14347477",  # OrderCreated
                    "0x4bdcff348c4d11383c487afb95f732f243d93fbfc478aa736a4981cf6a640911",  # OrderUnlocked
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x337685fdaB40D39bd02028545a4FfA7D287cC3E2",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x0654874eb7F59C6f5b39931FC45dC45337c967c3",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
        ],
        "bnb": [
            {
                "abi": "mayan_swift",
                "contracts": [
                    "0xC38e4e6A15593f908255214653d3D947CA1c2338",  # Mayan Swift
                ],
                "topics": [
                    "0x6ec9b1b5a9f54d929394f18dac4ba1b1cc79823f2266c2d09cab8a3b4700b40b",  # OrderFulfilled
                    "0x918554b6bd6e2895ce6553de5de0e1a69db5289aa0e4fe193a0dcd1f14347477",  # OrderCreated
                    "0x4bdcff348c4d11383c487afb95f732f243d93fbfc478aa736a4981cf6a640911",  # OrderUnlocked
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x337685fdaB40D39bd02028545a4FfA7D287cC3E2",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x0654874eb7F59C6f5b39931FC45dC45337c967c3",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
        ],
        "polygon": [
            {
                "abi": "mayan_swift",
                "contracts": [
                    "0xC38e4e6A15593f908255214653d3D947CA1c2338",  # Mayan Swift
                ],
                "topics": [
                    "0x6ec9b1b5a9f54d929394f18dac4ba1b1cc79823f2266c2d09cab8a3b4700b40b",  # OrderFulfilled
                    "0x918554b6bd6e2895ce6553de5de0e1a69db5289aa0e4fe193a0dcd1f14347477",  # OrderCreated
                    "0x4bdcff348c4d11383c487afb95f732f243d93fbfc478aa736a4981cf6a640911",  # OrderUnlocked
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x337685fdaB40D39bd02028545a4FfA7D287cC3E2",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x0654874eb7F59C6f5b39931FC45dC45337c967c3",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
        ],
        "linea": [
            {
                "abi": "mayan_swift",
                "contracts": [
                    "0xC38e4e6A15593f908255214653d3D947CA1c2338",  # Mayan Swift
                ],
                "topics": [
                    "0x6ec9b1b5a9f54d929394f18dac4ba1b1cc79823f2266c2d09cab8a3b4700b40b",  # OrderFulfilled
                    "0x918554b6bd6e2895ce6553de5de0e1a69db5289aa0e4fe193a0dcd1f14347477",  # OrderCreated
                    "0x4bdcff348c4d11383c487afb95f732f243d93fbfc478aa736a4981cf6a640911",  # OrderUnlocked
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x337685fdaB40D39bd02028545a4FfA7D287cC3E2",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
            {
                "abi": "mayan_forwarder",
                "contracts": [
                    "0x0654874eb7F59C6f5b39931FC45dC45337c967c3",  # Mayan Forwarder
                ],
                "topics": [
                    "0x7cbff921ae1f3ea71284120d2aabde13587df067f2bb5c831ea6e35d7a9242ac",  # SwapAndForwardedEth
                    "0x23278f58875126c795a4072b98b5851fe9b21cea19895b02a6224fefbb1e3298",  # SwapAndForwardedERC20
                    "0xb8543d214cab9591941648db8d40126a163bfd0db4a865678320b921e1398043",  # ForwardedEth
                    "0xbf150db6b4a14b084f7346b4bc300f552ce867afe55be27bce2d6b37e3307cda",  # ForwardedERC20
                ],
            },
        ],
    }
}

MAIN_BRIDGE_CONTRACT = "0xc38e4e6a15593f908255214653d3d947ca1c2338"  # Mayan Swift


BLOCKCHAIN_IDS = {
    "30": {
        "nativeChainId": 8453,
        "name": "base",
    },
    "24": {
        "nativeChainId": 10,
        "name": "optimism",
    },
    "23": {
        "nativeChainId": 42161,
        "name": "arbitrum",
    },
    "5": {
        "nativeChainId": 137,
        "name": "polygon",
    },
    "6": {
        "nativeChainId": 43114,
        "name": "avalanche",
    },
    "2": {
        "nativeChainId": 1,
        "name": "ethereum",
    },
    "38": {
        "nativeChainId": 59144,
        "name": "linea",
    },
    "4": {
        "nativeChainId": 56,
        "name": "bnb",
    },
    "1": {
        "nativeChainId": None,
        "name": "solana",
    },
}

SOLANA_PROGRAM_ADDRESSES = [
    "BLZRi6frs4X4DNLw56V4EXai1b6QVESN1BhHBTYM9VcY", # Mayan Swift
    "9w1D9okTM8xNE7Ntb7LpaAaoLc6LfU9nHFs2h2KTpX1H", # Auction
]
