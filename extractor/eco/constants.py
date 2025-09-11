BRIDGE_CONFIG = {
    "blockchains": {
        #opopulate as addresses become known; structure mirrors other bridges
    "ethereum": [
            {
                "abi": "intent",
                "contracts": [
                    "0x2020ae689ED3e017450280CEA110d0ef6E640Da4"
                ],
                "topics": [
                    "0x6653a45d3871e4110fa55dac0269f9f93a6d9078d402f7153594e50573d7f0cd", #withdrawal
                    "0x2da42efda5225344c30e729dc0eafc2e56292ac9b9b5c2b16e0e74c86ea5921d", #intent funded
                    "0xd802f2610d0c85b3f19be4413f3cf49de1d4e787edecd538274437a5b9aa648d", #intent created
                ],
            },
            {
                "abi": "inbox",
                "contracts": [
                    "0x04c816032A076dF65b411Bb3F31c8d569d411ee2"
                ],
                "topics": [
                    "0x4a817ec64beb8020b3e400f30f3b458110d5765d7a9d1ace4e68754ed2d082de" #fulfillment
                ],
            },
        ],
        "arbitrum": [
            {
                "abi": "intent",
                "contracts": [
                    "0x2020ae689ED3e017450280CEA110d0ef6E640Da4"
                ],
                "topics": [
                    "0x6653a45d3871e4110fa55dac0269f9f93a6d9078d402f7153594e50573d7f0cd", #withdrawal
                    "0x2da42efda5225344c30e729dc0eafc2e56292ac9b9b5c2b16e0e74c86ea5921d", #intent funded
                    "0xd802f2610d0c85b3f19be4413f3cf49de1d4e787edecd538274437a5b9aa648d", #intent created
                ],
            },
            {
                "abi": "inbox",
                "contracts": [
                    "0x04c816032A076dF65b411Bb3F31c8d569d411ee2"
                ],
                "topics": [
                    "0x4a817ec64beb8020b3e400f30f3b458110d5765d7a9d1ace4e68754ed2d082de" #fulfillment
                ],
            },
        ],
    "base": [
            {
                "abi": "intent",
                "contracts": [
                    "0x2020ae689ED3e017450280CEA110d0ef6E640Da4"
                ],
                "topics": [
                    "0x6653a45d3871e4110fa55dac0269f9f93a6d9078d402f7153594e50573d7f0cd", #withdrawal
                    "0x2da42efda5225344c30e729dc0eafc2e56292ac9b9b5c2b16e0e74c86ea5921d", #intent funded
                    "0xd802f2610d0c85b3f19be4413f3cf49de1d4e787edecd538274437a5b9aa648d", #intent created
                ],
            },
            {
                "abi": "inbox",
                "contracts": [
                    "0x04c816032A076dF65b411Bb3F31c8d569d411ee2"
                ],
                "topics": [
                    "0x4a817ec64beb8020b3e400f30f3b458110d5765d7a9d1ace4e68754ed2d082de" #fulfillment
                ],
            },
        ],
        "optimism": [
            {
                "abi": "intent",
                "contracts": [
                    "0x2020ae689ED3e017450280CEA110d0ef6E640Da4"
                ],
                "topics": [
                    "0x6653a45d3871e4110fa55dac0269f9f93a6d9078d402f7153594e50573d7f0cd", #withdrawal
                    "0x2da42efda5225344c30e729dc0eafc2e56292ac9b9b5c2b16e0e74c86ea5921d", #intent funded
                    "0xd802f2610d0c85b3f19be4413f3cf49de1d4e787edecd538274437a5b9aa648d", #intent created
                ],
            },
            {
                "abi": "inbox",
                "contracts": [
                    "0x04c816032A076dF65b411Bb3F31c8d569d411ee2"
                ],
                "topics": [
                    "0x4a817ec64beb8020b3e400f30f3b458110d5765d7a9d1ace4e68754ed2d082de" #fulfillment
                ],
            },
        ],
        "polygon": [
            {
                "abi": "intent",
                "contracts": [
                    "0x2020ae689ED3e017450280CEA110d0ef6E640Da4"
                ],
                "topics": [
                    "0x6653a45d3871e4110fa55dac0269f9f93a6d9078d402f7153594e50573d7f0cd", #withdrawal
                    "0x2da42efda5225344c30e729dc0eafc2e56292ac9b9b5c2b16e0e74c86ea5921d", #intent funded
                    "0xd802f2610d0c85b3f19be4413f3cf49de1d4e787edecd538274437a5b9aa648d", #intent created
                ],
            },
            {
                "abi": "inbox",
                "contracts": [
                    "0x04c816032A076dF65b411Bb3F31c8d569d411ee2"
                ],
                "topics": [
                    "0x4a817ec64beb8020b3e400f30f3b458110d5765d7a9d1ace4e68754ed2d082de" #fulfillment
                ],
            },
        ],
        # Add other chains (arbitrum, optimism, base, etc.) as needed
    }
}
