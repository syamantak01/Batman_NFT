#!/usr/bin/python3
from brownie import ErcCollectible, accounts, network, config
from scripts.utils import OPENSEA_FORMAT, get_account, get_contract, fund_LINK


def deploy_and_create():
    account = get_account()
    # We want to be able to use the deployed contracts if we are on a testnet
    # Otherwise, we want to deploy some mocks and use those
    # OpenSea testnet only works with Rinkeby
    collectible = ErcCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=True,  #uncomment this line to verify the contract. Once verified, comment it again
    )
    fund_LINK(collectible.address)
    create_tx = collectible.createCollectible({"from": account})
    create_tx.wait(1)
    print("New Token has been created!")

    return collectible, create_tx


def main():
    deploy_and_create()
