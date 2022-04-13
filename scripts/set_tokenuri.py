from brownie import network, ErcCollectible
from scripts.utils import OPENSEA_FORMAT, get_type, get_account
import json


def main():
    erc_collectible = ErcCollectible[-1]
    n_collectibles = erc_collectible.tokenCounter()
    print(f"You have {n_collectibles} tokenIds")

    for token_id in range(n_collectibles):
        type = get_type(erc_collectible.tokenIdToType(token_id))

        metadata_uri_file = f"./metadata/uri/{token_id}-{type}.json"
        f = open(metadata_uri_file)
        data = json.load(f)
        metadata_uri = data["uri"]

        if not erc_collectible.tokenURI(token_id).startswith("ipfs://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, erc_collectible, metadata_uri)


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_FORMAT.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
