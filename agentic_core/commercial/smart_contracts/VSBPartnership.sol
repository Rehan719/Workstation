// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title VSB Partnership Agreement v128.0
 * ARTICLE 753: Smart Contract for Tiered Partnerships.
 */
contract VSBPartnership {
    enum Tier { Associate, Certified, Strategic }

    struct Partner {
        string name;
        Tier tier;
        bool active;
        uint256 revenueShare; // Basis points (e.g., 500 = 5%)
    }

    mapping(address => Partner) public partners;
    address public vsbOwner;

    event PartnerRegistered(address indexed partner, string name, Tier tier);

    constructor() {
        vsbOwner = msg.sender;
    }

    function registerPartner(address _partner, string memory _name, Tier _tier, uint256 _rev) public {
        require(msg.sender == vsbOwner, "Only VSB CEO can register partners");
        partners[_partner] = Partner(_name, _tier, true, _rev);
        emit PartnerRegistered(_partner, _name, _tier);
    }

    function deactivatePartner(address _partner) public {
        require(msg.sender == vsbOwner, "Only VSB CEO can deactivate");
        partners[_partner].active = false;
    }
}
