from brownie import network, AdvancedCollectible, Contract
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
from scripts.advanced_collectible.deploy_and_create import deploy_and_create

#VRF coord not understood with the callbackwithrandomness

vrfABI = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_link",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_blockHashStore",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "keyHash",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "fee",
                "type": "uint256"
            }
        ],
        "name": "NewServiceAgreement",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "keyHash",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "seed",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "jobID",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "fee",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "requestID",
                "type": "bytes32"
            }
        ],
        "name": "RandomnessRequest",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "requestId",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "output",
                "type": "uint256"
            }
        ],
        "name": "RandomnessRequestFulfilled",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "PRESEED_OFFSET",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "PROOF_LENGTH",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "PUBLIC_KEY_OFFSET",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "name": "callbacks",
        "outputs": [
            {
                "internalType": "address",
                "name": "callbackContract",
                "type": "address"
            },
            {
                "internalType": "uint96",
                "name": "randomnessFee",
                "type": "uint96"
            },
            {
                "internalType": "bytes32",
                "name": "seedAndBlockNum",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes",
                "name": "_proof",
                "type": "bytes"
            }
        ],
        "name": "fulfillRandomnessRequest",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256[2]",
                "name": "_publicKey",
                "type": "uint256[2]"
            }
        ],
        "name": "hashOfKey",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_fee",
                "type": "uint256"
            },
            {
                "internalType": "bytes",
                "name": "_data",
                "type": "bytes"
            }
        ],
        "name": "onTokenTransfer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_fee",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "_oracle",
                "type": "address"
            },
            {
                "internalType": "uint256[2]",
                "name": "_publicProvingKey",
                "type": "uint256[2]"
            },
            {
                "internalType": "bytes32",
                "name": "_jobID",
                "type": "bytes32"
            }
        ],
        "name": "registerProvingKey",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "name": "serviceAgreements",
        "outputs": [
            {
                "internalType": "address",
                "name": "vRFOracle",
                "type": "address"
            },
            {
                "internalType": "uint96",
                "name": "fee",
                "type": "uint96"
            },
            {
                "internalType": "bytes32",
                "name": "jobID",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_recipient",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            }
        ],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "withdrawableTokens",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

def test_can_create_advanced_collectible():
    #deploy the contract
    #create an nft
    #get a random breed back
    #if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    #    pytest.skip("only for local testing")
    #Act
    advanced_collectible, creation_transaction = deploy_and_create()
    requestId = creation_transaction.events["requestedCollectible"]["requestId"]
    #we can use creation_transaction to get our events
    random_number= 777
    vrf_coord = Contract.from_abi("vrf_coord", "0xb3dCcb4Cf7a26f6cf6B120Cf5A73875B7BBc655B", vrfABI )
    vrf_coord.callBackWithRandomness( requestId, random_number, advanced_collectible.address, {"from": get_account()})
    #Assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3




