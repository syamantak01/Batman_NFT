We will work with ERC-721 token to created NFTs
Instead of recoding all of the code, we will work with Openzepplin's ERC-721

This NFT contract is a sort of [factory contract](https://research.csiro.au/blockchainpatterns/general-patterns/contract-structural-patterns/factory-contract/). We will use this factory implementation to create multiple NFTs i.e., We make many NFTs, but they are all contained in this one contract.

Creating a new NFT is just mapping a tokenID to a new address/new owner.
We are gonna use _safeMint()
First, we need a way to count token IDs so that every single person has a unique token ID

We will use TokenURI and metadata to store the image on blockchain, more specifially using IPFS. IPFS is a decentralised way to store images **off-chain**.
PS: For full functionality of NFTs, we need on-chain attributes. And just use TokenURI for visuals.

1) Upload image to IPFS
    - Its important to upload images on a decentralised server like IPFS or Filecoin rather than on a centralised server.
    - We need to upload both the image and the metadata containing the uri to the image to the ipfs
    - Use the ipfs command line
    - <https://docs.ipfs.io/reference/http/api/#api-v0-add>
    - We need to keep running the ipfs entire time. Anytime their node goes down, nobody will be able to see the image, unless somebody else pins the image. Alternative is to upload the image to another 3rd party service like **Pinata** along with uploading it to our own ipfs

2) Make NFT more verfiably random and verifiably scarce so that anyone cannot mint an NFT
    - Integrate Chainlink VRF.
    - A common problem in the traditional web2 art and trading card world is the transparency of randomness and scarcity.
    If you buy a trading card, like a Pokémon card for example, you have no way of knowing how rare it really is without talking to the company that printed it. There is a centralized component to the scarcity of the card. They could have printed millions of the card, making it worthless, or just 1, making it incredibly rare.
    With NFTs, if you are the one who can control how rare a card is, you are a centralized component of rarity, and not a decentralized component.
    Now, if you use Chainlink VRF to mint your cards, you have 0 control of how rare the card is, and you can rely on true randomness. This gives uses of the NFTs a proven way to know how rare and how scarce your NFTs are, making them more valuable and tamper-proof.
    This solves the centralized issue of diluting the value of NFTs by printing more "rare" ones, giving them actual value.
    - We are only gonna know what type of batman it is once the **random number** is generated. Create our own new setTokenURI() function that sets the tokenURI based on the type of the batman and update it based on the type of the batman

Automate the testing:
    - To see if the token has been created, we check if the tokenCounter has been increased to 1
    - The bulk of the work actually comes from the fulfillRandomness() function and we have to tell our VRFCoordinator Mock to actually return and call this function.
    - In integration testing, we dont need to manually call the callBackWithRandomness() function and since the chainlink node will respond, we dont need the requestId seperately. That means the type that we are going to get will actually be random. All we need to do is wait for the transaction to be called back.

Order of running scripts/commands
    - `ipfs daemon` to make the ipfs node online
    - `brownie run scripts/deploy_and_create.py --network rinkeby`
    - `brownie run scripts/create_collectible.py --network rinkeby`
        - wait for some time(~30 sec) for the VRFCoordinator to respond
    - `brownie run scripts/create_metadata.py --network rinkeby`
    - `brownie run scripts/upload_to_pinata.py`
        - change the filepath to upload all the images
    - `brownie run scripts/set_tokenuri.py --network rinkeby`

My NFTs
    - https://testnets.opensea.io/assets/0x9b3fBF9DA743801861998E7158054425FB99f878/0
    - https://testnets.opensea.io/assets/0x9b3fBF9DA743801861998E7158054425FB99f878/1
