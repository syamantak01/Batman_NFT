from brownie import ErcCollectible
from scripts.utils import fund_LINK, get_account
from web3 import Web3


def main():
    account = get_account()
    erc_collectible = ErcCollectible[-1]
    fund_LINK(erc_collectible.address, amount=Web3.toWei(0.1, "ether"))
    creation_tx = erc_collectible.createCollectible({"from": account})
    creation_tx.wait(1)
    print("Collectible created")
