// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

interface ISubscriptionManager {
    struct SubscriptionPlan {
        string name;
        uint256 price;
        address token;
        uint256 frequency;
        address owner;
        string logo;
        bool exists;
    }
    
    function plans(uint256) external view returns (SubscriptionPlan memory);
    function senders(uint256, address) external view returns (uint256, uint256, uint256, bool);
}

contract MembershipToken is ERC721, Ownable {
    address public subscriptionManager;
    
    // Mapping from tokenId to planId
    mapping(uint256 => uint256) public tokenToPlan;

    constructor() 
    ERC721("Membership Token", "MEMBER") 
    Ownable(msg.sender){}

    modifier onlySubscriptionManager() {
        require(msg.sender == subscriptionManager, "Not authorized");
        _;
    }

    function setSubscriptionManager(address _manager) external onlyOwner {
        require(_manager != address(0), "Invalid address");
        subscriptionManager = _manager;
    }

    /// @notice Mint membership token — callable only by SubscriptionManager
    function mint(address recipient, uint256 tokenId, uint256 planId)
        external
        onlySubscriptionManager
    {
        _mint(recipient, tokenId);
        tokenToPlan[tokenId] = planId;
    }

    /// @notice Burn membership token — callable only by SubscriptionManager
    function burn(uint256 tokenId)
        external
        onlySubscriptionManager
    {
        delete tokenToPlan[tokenId];
        _burn(tokenId);
    }
    
    /// @notice Returns metadata URI for the membership token
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(ownerOf(tokenId) != address(0), "Token does not exist");
        
        uint256 planId = tokenToPlan[tokenId];
        ISubscriptionManager manager = ISubscriptionManager(subscriptionManager);
        ISubscriptionManager.SubscriptionPlan memory plan = manager.plans(planId);
        
        // Create JSON metadata
        return string(abi.encodePacked(
            'data:application/json;utf8,{"name":"',
            plan.name,
            ' Membership #',
            _toString(tokenId),
            '","description":"Active membership for ',
            plan.name,
            '","image":"',
            plan.logo,
            '","attributes":[{"trait_type":"Plan","value":"',
            plan.name,
            '"},{"trait_type":"Token ID","value":"',
            _toString(tokenId),
            '"}]}'
        ));
    }
    
    /// @notice Convert uint256 to string
    function _toString(uint256 value) internal pure returns (string memory) {
        if (value == 0) {
            return "0";
        }
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }
}
