// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./MembershipToken.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract SubscriptionManager {

    MembershipToken public membershipToken;

    constructor(address _membershipToken) {
        membershipToken = MembershipToken(_membershipToken);
    }

    // ---------------------------------------------
    // ------------ STRUCT DEFINITIONS --------------
    // ---------------------------------------------

    struct SubscriptionPlan {
        string name;            // plan name
        uint256 price;          // subscription price in ERC20 tokens
        address token;          // ERC20 token accepted for payment
        uint256 frequency;      // billing cycle in seconds
        address owner;          // receiver who created the plan
        string logo;            // logo URL for the plan
        bool exists;            // sanity flag
    }

    struct Sender {
        uint256 startDate;
        uint256 nextPayment;
        uint256 tokenId;
        bool subscribed;
    }

    // ---------------------------------------------
    // ----------------- STORAGE --------------------
    // ---------------------------------------------

    uint256 public planCount;
    uint256 public tokenCounter;

    // planId => SubscriptionPlan
    mapping(uint256 => SubscriptionPlan) public plans;

    // planId => userAddress => Sender
    mapping(uint256 => mapping(address => Sender)) public senders;

    // ---------------------------------------------
    // ------------------- EVENTS -------------------
    // ---------------------------------------------

    event PlanCreated(uint256 planId, string name, address indexed owner, uint256 price, address token, uint256 frequency);
    event Subscribed(uint256 indexed planId, address indexed user, uint256 tokenId);
    event Unsubscribed(uint256 indexed planId, address indexed user);

    // ---------------------------------------------
    // ------------ PLAN CREATION LOGIC -------------
    // ---------------------------------------------

    function createPlan(string memory name, uint256 price, address token, uint256 frequency, string memory logo)
        external
    {
        require(bytes(name).length > 0, "Name cannot be empty");
        require(price > 0, "Price must be > 0");
        require(token != address(0), "Invalid ERC20 token");

        plans[planCount] = SubscriptionPlan({
            name: name,
            price: price,
            token: token,
            frequency: frequency,
            owner: msg.sender,
            logo: logo,
            exists: true
        });

        emit PlanCreated(planCount, name, msg.sender, price, token, frequency);
        planCount++;
    }

    // ---------------------------------------------
    // ------------ SUBSCRIBE / UNSUBSCRIBE --------
    // ---------------------------------------------

    function subscribe(uint256 planId) external {
        SubscriptionPlan memory plan = plans[planId];
        require(plan.exists, "Plan does not exist");

        Sender storage s = senders[planId][msg.sender];
        require(!s.subscribed, "Already subscribed");

        // Take first payment immediately
        IERC20(plan.token).transferFrom(
            msg.sender,
            plan.owner,
            plan.price
        );

        // Mint membership token
        uint256 tokenId = tokenCounter++;
        membershipToken.mint(msg.sender, tokenId, planId);

        // Store sender info
        s.startDate = block.timestamp;
        s.nextPayment = block.timestamp + plan.frequency;
        s.tokenId = tokenId;
        s.subscribed = true;

        emit Subscribed(planId, msg.sender, tokenId);
    }

    function unsubscribe(uint256 planId) external {
        Sender storage s = senders[planId][msg.sender];
        require(s.subscribed, "Not subscribed");

        // Burn their membership token
        membershipToken.burn(s.tokenId);

        // Clear subscription data
        delete senders[planId][msg.sender];

        emit Unsubscribed(planId, msg.sender);
    }

    // ---------------------------------------------
    // -------------------- GETTERS -----------------
    // ---------------------------------------------

    function getPlan(uint256 planId)
        external
        view
        returns (SubscriptionPlan memory)
    {
        return plans[planId];
    }

    function getSenderStatus(uint256 planId, address user)
        external
        view
        returns (Sender memory)
    {
        return senders[planId][user];
    }
}
