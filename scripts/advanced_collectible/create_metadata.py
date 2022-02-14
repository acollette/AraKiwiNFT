from brownie import AdvancedCollectible, network, config
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
#from python to check path (in our case if already exists)
from pathlib import Path
import requests
import json
import os


PinataApiKey = config["pinata"]["pinata_api_key"]
PinataSecretApiKey = config["pinata"]["pinata_secret_api_key"]

breed_to_image_uri = {
    "NORMAL":"https://gateway.pinata.cloud/ipfs/QmcWYYWnpLxcfWd5CXTekpzNv8xwigEm2ywokffXy4PPZc", 
    "FREE_BOTTLE": "https://gateway.pinata.cloud/ipfs/QmTPCFtsswbDkTb5BapZsKhyMSY6zndrTkfa94xzdtnNBU", 
    "BACKSTAGE": "https://gateway.pinata.cloud/ipfs/QmdP8GXekzKtCuz5E7CusZz1nY5Aj9AdHUdyq8fwoXfeU5"
    
}

headers = {"pinata_api_key": PinataApiKey, "pinata_secret_api_key":  PinataSecretApiKey}
PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"

def main():
    #we take the latest version of the deployed contracts
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        #we do get_breed because the part between brackets will return integer (the enum is considered as 0,1,2.. that will give 0=normal, 1=Free...)
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (f"./metadata/{network.show_active()}/{token_id}-{breed}.json")
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists, delete it to overwrite")
        else: 
            print(f"Creating Metadata File: {metadata_file_name} ")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"You've received a {breed} access !"
            image_path = "./img/" + breed.lower().replace("_", "") + ".png"

            #If we want to use same picture for multiple tokens, than we can use the following block,
            #Here we don't want to upload more pictures on IPFS thus we set in .env UPLOAD_IPFS to false.
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_pinata(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]

            image_uri = upload_to_pinata(image_path)
            collectible_metadata["image"] = image_uri
            #now we write in the metadata file folder "w" from write
            ##will dump this dictionary as json in metadata file
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") =="true":
                upload_to_pinata(metadata_file_name)




def upload_to_pinata(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        filename = filepath.split("/")[-1:][0]
        response = requests.post(PINATA_BASE_URL + endpoint, files= {"file": (image_binary)}, headers=headers)
        print(response.json())
        ipfs_hash = response.json()["IpfsHash"]
        #Now we split to take only the last part
        #We should add "filename" at the end of image_uri in the case we work in a directory
        image_uri = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
        return image_uri


