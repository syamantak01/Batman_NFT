from brownie import network, ErcCollectible
import time
import pytest
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
from scripts.deploy_and_create import deploy_and_create


def test_can_create_collectible_integration():
    # deploy the contract
    # create an NFT
    # get a random type back

    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Act
    collectible, create_tx = deploy_and_create()
    time.sleep(60)  # wait for the transaction to be called back

    # Assert
    assert collectible.tokenCounter() == 1
