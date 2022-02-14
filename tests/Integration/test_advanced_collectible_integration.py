from brownie import network, AdvancedCollectible, Contract
import pytest
import time
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
from scripts.advanced_collectible.deploy_and_create import deploy_and_create

#V


def test_can_create_advanced_collectible_integrations():
    #deploy the contract
    #create an nft
    #get a random breed back
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for integration testing")
    #Act
    advanced_collectible, creation_transaction = deploy_and_create()
    # wait 60 seconds (can be longer depending on the response of the VRF Coordinator)
    time.sleep(60)
    
    #we can use creation_transaction to get our events

    #Assert
    assert advanced_collectible.tokenCounter() == 1




