from brownie import network, ErcCollectible
import pytest
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
from scripts.deploy_and_create import deploy_and_create


def test_can_create_collectible():
    # deploy the contract
    # create an NFT
    # get a random type back

    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Acting
    collectible, create_tx = deploy_and_create()

    random_number = 777
    requestId = create_tx.events["requestedCollectable"]["requestId"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, collectible.address, {"from": get_account()}
    )

    # Assert
    assert collectible.tokenCounter() == 1
    assert collectible.tokenIdToType(0) == random_number % 3
