from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_breed, get_account

ara_kiwi_metadata_dict = {
    "NORMAL" : "https://gateway.pinata.cloud/ipfs/QmNkEYLo6kuBLWmBcTadqWeQ5WaZdUBy2Jm1BbZ4LrdBgr/Normal.json",
    "FREE_BOTTLE": "https://gateway.pinata.cloud/ipfs/QmNkEYLo6kuBLWmBcTadqWeQ5WaZdUBy2Jm1BbZ4LrdBgr/FreeBottle.json",
    "BACKSTAGE": "https://gateway.pinata.cloud/ipfs/QmNkEYLo6kuBLWmBcTadqWeQ5WaZdUBy2Jm1BbZ4LrdBgr/Backstage.json"

}

def main():
    print(f"Working on {network.show_active()} ")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        #We check if tokenURI doesn't exist at the moment
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, ara_kiwi_metadata_dict[breed]  )

def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}")
    print("Please wait up to 20 minutes and refresh ")



