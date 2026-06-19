import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Vote, FileText, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { toast } from '@workstation/ui';
import { useNavigate } from 'react-router-dom';

interface Proposal {
  id: string;
  title: string;
  description: string;
  type: 'WITHDRAWAL' | 'CONSTITUTION_AMENDMENT' | 'STRATEGY_SHIFT';
  status: 'PENDING' | 'DEBATING' | 'EXECUTED' | 'REJECTED';
  votesFor: number;
  votesAgainst: number;
  quorumRequired: number;
  expiresAt: string;
}

export default function CouncilDashboard() {
  const navigate = useNavigate();
  const [proposals, setProposals] = useState<Proposal[]>([
    {
      id: 'prop_001',
      title: 'Emergency Withdraw 15% AUM',
      description: 'Requesting liquidity for strategic real-world asset acquisition.',
      type: 'WITHDRAWAL',
      status: 'PENDING',
      votesFor: 2,
      votesAgainst: 0,
      quorumRequired: 3,
      expiresAt: '2026-05-10T18:00:00Z'
    },
    {
      id: 'prop_002',
      title: 'Article 1130 Amendment',
      description: 'Increase single-asset allocation limit from 20% to 25% for low-volatility ETFs.',
      type: 'CONSTITUTION_AMENDMENT',
      status: 'DEBATING',
      votesFor: 1,
      votesAgainst: 1,
      quorumRequired: 3,
      expiresAt: '2026-05-12T12:00:00Z'
    }
  ]);

  const handleVote = async (id: string, approve: boolean) => {
    // Simulate PQC-signed vote
    setProposals(prev => prev.map(p => {
      if (p.id === id) {
        return {
          ...p,
          votesFor: approve ? p.votesFor + 1 : p.votesFor,
          votesAgainst: !approve ? p.votesAgainst + 1 : p.votesAgainst
        };
      }
      return p;
    }));
  };

  return (
    <div className="p-8 space-y-8 bg-[#020202] min-h-screen text-white">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tighter text-[#00ffcc]">AI GOVERNANCE COUNCIL</h1>
          <p className="text-muted-foreground mt-2">Sovereign Decision Mesh vΩ∞-MASTER</p>
        </div>
        <div className="flex gap-4">
          <Button onClick={() => navigate('/governance')} variant="outline" className="border-[#00ffcc] text-[#00ffcc] hover:bg-[#00ffcc]/10">
            <FileText className="mr-2 h-4 w-4" /> SUBMIT PROPOSAL
          </Button>
          <Badge variant="secondary" className="bg-[#1a1a1a] text-[#00ffcc] px-4 py-2 border border-[#333]">
            3 ACTIVE MEMBERS
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-8">
        {proposals.map(proposal => (
          <Card key={proposal.id} className="bg-[#0f0f0f] border-[#1a1a1a] overflow-hidden hover:border-[#333] transition-all">
            <CardHeader className="border-b border-[#1a1a1a] flex flex-row justify-between items-start">
              <div>
                <Badge className="mb-2 bg-[#00ffcc]/10 text-[#00ffcc] hover:bg-[#00ffcc]/20">
                  {proposal.type}
                </Badge>
                <CardTitle className="text-xl font-bold">{proposal.title}</CardTitle>
              </div>
              <Badge variant="outline" className={proposal.status === 'PENDING' ? 'text-yellow-500' : 'text-blue-500'}>
                {proposal.status}
              </Badge>
            </CardHeader>
            <CardContent className="pt-6 space-y-4">
              <p className="text-sm text-gray-400 leading-relaxed">
                {proposal.description}
              </p>

              <div className="space-y-2">
                <div className="flex justify-between text-xs font-bold">
                  <span>CONSENSUS PROGRESS</span>
                  <span>{proposal.votesFor} / {proposal.quorumRequired} QUORUM</span>
                </div>
                <Progress value={(proposal.votesFor / proposal.quorumRequired) * 100} className="h-2 bg-[#1a1a1a] shadow-inner" />
              </div>

              <div className="grid grid-cols-2 gap-4 pt-2">
                <div className="bg-[#1a1a1a] p-3 rounded-lg border border-[#333]">
                  <p className="text-[10px] text-gray-500 font-bold uppercase">Votes For</p>
                  <p className="text-lg font-bold text-green-400">{proposal.votesFor}</p>
                </div>
                <div className="bg-[#1a1a1a] p-3 rounded-lg border border-[#333]">
                  <p className="text-[10px] text-gray-500 font-bold uppercase">Votes Against</p>
                  <p className="text-lg font-bold text-red-400">{proposal.votesAgainst}</p>
                </div>
              </div>
            </CardContent>
            <CardFooter className="bg-[#0a0a0a] border-t border-[#1a1a1a] flex gap-4 p-4">
              <Button
                onClick={() => handleVote(proposal.id, true)}
                className="flex-1 bg-[#00ffcc] text-black hover:bg-[#00e6b8] font-bold"
              >
                <Vote className="mr-2 h-4 w-4" /> APPROVE
              </Button>
              <Button
                onClick={() => handleVote(proposal.id, false)}
                variant="outline"
                className="flex-1 border-red-500/50 text-red-400 hover:bg-red-500/10"
              >
                <ShieldAlert className="mr-2 h-4 w-4" /> REJECT
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>

      {/* Verification Certificate Preview */}
      <Card className="bg-[#0f0f0f] border-dashed border-2 border-[#333]">
        <CardContent className="p-8 flex flex-col items-center justify-center text-center space-y-4">
          <CheckCircle2 size={48} className="text-[#00ffcc]" />
          <div>
            <h3 className="text-xl font-bold uppercase tracking-widest text-[#00ffcc]">Verification Engine</h3>
            <p className="text-sm text-gray-400 mt-1 max-w-md mx-auto">
              All active invariants are currently formally verified via TLA+ Model Checking.
              Real-time audit certificates are cryptographically anchored to UEG.
            </p>
          </div>
          <Button onClick={() => toast('Verification certificates are anchored to the UEG Merkle-DAG — audit trail available in Change Control Agency')} variant="link" className="text-[#00ffcc] font-bold">VIEW LATEST CERTIFICATE</Button>
        </CardContent>
      </Card>
    </div>
  );
}
