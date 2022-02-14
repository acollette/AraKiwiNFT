from brownie import AdvancedCollectible, accounts, config
from scripts.helpful_scripts import fund_with_link, get_breed
from web3 import Web3
import time

def main():
    dev = accounts.add(config["wallets"]["from_key"])
    #i = 0
   # while i < 5:

    advanced_collectiblev1 = AdvancedCollectible[-1]
    fund_with_link(advanced_collectiblev1.address, amount = Web3.toWei(0.1, "ether"))
    creation_transaction = advanced_collectiblev1.createCollectible({"from": dev})
    creation_transaction.wait(1)
    time.sleep(35)
    #now we look for an event in the transaction
    requestId = creation_transaction.events["requestedCollectible"]["requestId"] 
    token_id = advanced_collectiblev1.requestIdToTokenId(requestId)
    #we do get_breed because the part between brackets will return integer (the enum is considered as 0,1,2.. that will give 0=normal, 1=Free...)
    breed = get_breed(advanced_collectiblev1.tokenIdToBreed(token_id))
    print("Dog breed of tokenId {} is {}".format(token_id, breed))
        #i = i +1





