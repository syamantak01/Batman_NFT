// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract ErcCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;

    //Types of NFTs
    enum Batype {
        BAT,
        BAT_GAD,
        BAT_SYM
    }

    //mappings
    mapping(uint256 => Batype) public tokenIdToType;
    mapping(bytes32 => address) public requestIdToSender;

    //event
    // Indexed parameters helps you filter the logs by the indexed parameter
    event requestedCollectable(bytes32 indexed requestId, address requester);
    event typeAssigned(uint256 indexed tokenId, Batype batype);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Batman", "BAT")
    {
        tokenCounter = 0;
        keyhash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        //Good Practice is to Emit events whenever we want to update mappings
        emit requestedCollectable(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Batype batype = Batype(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToType[newTokenId] = batype;
        //Good Practice is to Emit events whenever we want to update mappings
        emit typeAssigned(newTokenId, batype);

        //user who called createCollectible to be the same user who gets assigned the tokenID.
        //In this case, VRFCoordinator will be msg.sender since VRFCoordinator is the one that calls fulfilRandomness()
        //but we need original caller of createCollectible() to mint NFTs
        //_safeMint(msg.sender, newTokenId);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        //_setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is nor owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
