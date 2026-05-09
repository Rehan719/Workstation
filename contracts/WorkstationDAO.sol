// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title WorkstationDAO
 * @dev Sovereign Governance for the Virtual Sovereign Business Capital Fund.
 * Implements weighted voting proportional to fund ownership.
 */
contract WorkstationDAO {
    string public constant name = "Workstation Capital DAO";
    string public constant symbol = "VSBC";

    address public owner;
    uint256 public totalSupply;
    mapping(address => uint256) public balances;

    struct Proposal {
        uint256 id;
        string description;
        uint256 votesFor;
        uint256 votesAgainst;
        bool executed;
        uint256 expiresAt;
    }

    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;

    event ProposalCreated(uint256 indexed id, string description);
    event Voted(uint256 indexed proposalId, address indexed voter, bool support, uint256 weight);
    event Executed(uint256 indexed id);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can override");
        _;
    }

    function createProposal(string memory _description) external onlyOwner {
        proposalCount++;
        proposals[proposalCount] = Proposal({
            id: proposalCount,
            description: _description,
            votesFor: 0,
            votesAgainst: 0,
            executed: false,
            expiresAt: block.timestamp + 3 days
        });
        emit ProposalCreated(proposalCount, _description);
    }

    function vote(uint256 _proposalId, bool _support) external {
        Proposal storage proposal = proposals[_proposalId];
        require(block.timestamp < proposal.expiresAt, "Voting expired");

        uint256 weight = balances[msg.sender];
        require(weight > 0, "No voting weight");

        if (_support) {
            proposal.votesFor += weight;
        } else {
            proposal.votesAgainst += weight;
        }

        emit Voted(_proposalId, msg.sender, _support, weight);
    }
}
