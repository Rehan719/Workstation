// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title Sovereign Liability Fund
 * @notice ARTICLE 1043: Multi-modal authorization for liability operations.
 * Pilot deployment for Polygon Testnet.
 */
contract LiabilityFund {
    address public sovereign;
    uint256 public totalFund;

    struct Claim {
        uint256 amount;
        string reason;
        bool approved;
        bool biometricVerified;
    }

    mapping(uint256 => Claim) public claims;
    uint256 public claimCount;

    event FundDeposited(address indexed sender, uint256 amount);
    event ClaimProposed(uint256 indexed id, uint256 amount);
    event ClaimSettled(uint256 indexed id, uint256 amount);

    modifier onlySovereign() {
        require(msg.sender == sovereign, "Only sovereign authorized");
        _;
    }

    constructor() {
        sovereign = msg.sender;
    }

    function deposit() external payable {
        totalFund += msg.value;
        emit FundDeposited(msg.sender, msg.value);
    }

    function proposeClaim(uint256 _amount, string memory _reason) external {
        claimCount++;
        claims[claimCount] = Claim(_amount, _reason, false, false);
        emit ClaimProposed(claimCount, _amount);
    }

    /**
     * @notice Settles a claim after biometric verification.
     * In the pilot, biometric status is passed via the sovereign bridge.
     */
    function settleClaim(uint256 _id, bool _biometricSuccess) external onlySovereign {
        Claim storage c = claims[_id];
        require(!c.approved, "Already settled");
        require(_biometricSuccess, "Biometric verification mandatory (Article 1043)");

        c.approved = true;
        c.biometricVerified = _biometricSuccess;

        payable(sovereign).transfer(c.amount);
        totalFund -= c.amount;

        emit ClaimSettled(_id, c.amount);
    }
}
