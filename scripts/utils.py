from brownie import network, accounts, config, LinkToken, VRFCoordinatorMock, Contract
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache-local",
    "mainnet-fork",
    "mainnet-fork-dev",
]

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

TYPE_MAPPING = {0: "BAT", 1: "BAT_GAD", 2: "BAT_SYM"}


def get_type(type_idx):
    return TYPE_MAPPING[type_idx]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


# mapping contract name to its type
contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    # getting the contract address from the brownie config if defined, otherwise it will deploy a mock version of
    # that contract and return the mock contract
    contract_type = contract_to_mock[contract_name]

    # When we deploy to development network
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # check if one of these contracts have already been deployed
        if len(contract_type) <= 0:
            # analogous to MockV3Aggregator.length<=0; we only need 1 mock i.e if a mock already exists we dont need another mock
            deploy_mocks()
        # Get that contract
        contract = contract_type[-1]  # Ananlogous to MockV3Aggregator[-1]
    # When we want to deploy to testnets
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # Creating a Contract from an ABI will allow you to call or send transactions to the contract, but functionality such as debugging will not be available.
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract


def deploy_mocks():
    """
    Use this function if you want to deploy mocks to a testnet
    """
    print("Deploying mocks...")
    account = get_account()
    # MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    print("Deploying Mock Link Token...")
    link_token = LinkToken.deploy({"from": account})
    print("Deploying Mock VRF Coordinator...")
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Done!")


# default amount is 0.1 LINK or 100000000000000000 wei
def fund_LINK(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, "ether")
):
    """
    Use this to fund the contract with LINK tokens
    """
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})

    # Another way to create a contract and interact with them is by using interfaces.
    # first create LinkTokenInterface.sol inside interfaces folder and then copy the contents of "https://github.com/smartcontractkit/chainlink-mix/blob/master/interfaces/LinkTokenInterface.sol"
    # and paste it to the LinkTokenInterface.sol

    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {'from': account})

    tx.wait(1)
    print(f"Funded the contract {contract_address}")
    return tx
