// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title WorkstationDAO
 * @dev Sovereign Governance for the Virtual Sovereign Business Capital Fund.
 * Implements weighted voting proportional to fund ownership.
 * Integrates with a PQC-EVM bridge for sovereign execution.
 */
contract WorkstationDAO {
    string public constant name = "Workstation Capital DAO";
    string public constant symbol = "VSBC";

    address public owner;
    uint256 public totalSupply;
    mapping(address => uint256) public balances;
    mapping(address => mapping(uint256 => bool)) public hasVoted;

    // Trusted bridge address that submits PQC-validated results
    address public pqcBridge;

    struct Proposal {
        uint256 id;
        string description;
        uint256 votesFor;
        uint256 votesAgainst;
        bool executed;
        uint256 expiresAt;
        bytes32 pqcAttestationHash; // Hash of the off-chain PQC signature/bundle
    }

    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;

    event ProposalCreated(uint256 indexed id, string description);
    event Voted(uint256 indexed proposalId, address indexed voter, bool support, uint256 weight);
    event Executed(uint256 indexed id, bytes32 attestation);
    event WeightMinted(address indexed to, uint256 amount);
    event BridgeUpdated(address indexed newBridge);

    constructor(address _pqcBridge) {
        owner = msg.sender;
        pqcBridge = _pqcBridge;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }

    modifier onlyBridge() {
        require(msg.sender == pqcBridge, "Only PQC Bridge can perform this action");
        _;
    }

    /**
     * @dev Mint voting weight to an investor.
     * In production, this would be tied to capital deposits.
     */
    function mint(address _to, uint256 _amount) external onlyOwner {
        balances[_to] += _amount;
        totalSupply += _amount;
        emit WeightMinted(_to, _amount);
    }

    function setBridge(address _newBridge) external onlyOwner {
        pqcBridge = _newBridge;
        emit BridgeUpdated(_newBridge);
    }

    function createProposal(string memory _description) external {
        // Anyone with balance or owner can create a proposal
        require(balances[msg.sender] > 0 || msg.sender == owner, "Unauthorized");

        proposalCount++;
        proposals[proposalCount] = Proposal({
            id: proposalCount,
            description: _description,
            votesFor: 0,
            votesAgainst: 0,
            executed: false,
            expiresAt: block.timestamp + 3 days,
            pqcAttestationHash: bytes32(0)
        });
        emit ProposalCreated(proposalCount, _description);
    }

    function vote(uint256 _proposalId, bool _support) external {
        Proposal storage proposal = proposals[_proposalId];
        require(block.timestamp < proposal.expiresAt, "Voting expired");
        require(!hasVoted[msg.sender][_proposalId], "Already voted");

        uint256 weight = balances[msg.sender];
        require(weight > 0, "No voting weight");

        if (_support) {
            proposal.votesFor += weight;
        } else {
            proposal.votesAgainst += weight;
        }

        hasVoted[msg.sender][_proposalId] = true;
        emit Voted(_proposalId, msg.sender, _support, weight);
    }

    /**
     * @dev PQC-EVM Bridge Execution.
     * Accepts a PQC attestation hash from the trusted bridge to finalize a proposal.
     */
    function executeWithPQC(uint256 _proposalId, bytes32 _attestationHash) external onlyBridge {
        Proposal storage proposal = proposals[_proposalId];
        require(!proposal.executed, "Already executed");
        require(proposal.votesFor > proposal.votesAgainst, "Quorum not met");

        proposal.executed = true;
        proposal.pqcAttestationHash = _attestationHash;

        emit Executed(_proposalId, _attestationHash);
    }

    /**
     * @dev Constitutional Emergency Veto (Article 1135).
     * The owner retains absolute veto power over any proposal.
     */
    function emergencyVeto(uint256 _proposalId) external onlyOwner {
        Proposal storage proposal = proposals[_proposalId];
        proposal.executed = true; // Mark as "executed" (cancelled)
        proposal.expiresAt = block.timestamp; // Expire immediately
    }
}
