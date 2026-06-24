import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';

interface Ruling {
  ruling_id: string;
  dispute_id: string;
  status: 'PENDING_RATIFICATION' | 'RATIFIED' | 'OVERRIDDEN';
  cited_precedent: string;
  decision: string;
  reasoning_trace: string;
  timestamp: string;
}

export default function CouncilJudiciary() {
  const [rulings, setRulings] = useState<Ruling[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch('/api/council/judge/rulings')
      .then(r => r.json())
      .then(data => setRulings(Array.isArray(data) ? data : []))
      .catch(() => setRulings([]));
  }, []);

  const handleOverride = async (rulingId: string) => {
    setLoading(true);
    try {
      const res = await fetch('/api/council/judge/override', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ruling_id: rulingId, reason: "Owner Emergency Veto" })
      });
      if (res.ok) {
        setRulings(prev => prev.map(r => r.ruling_id === rulingId ? {...r, status: 'OVERRIDDEN'} : r));
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">⚖️ Sovereign Judiciary</h1>
      <ScrollArea className="h-[600px]">
        <div className="space-y-4">
          {rulings.length === 0 && (
            <p className="text-sm text-muted-foreground">No rulings on file yet.</p>
          )}
          {rulings.map(ruling => (
            <Card key={ruling.ruling_id} className={ruling.status === 'OVERRIDDEN' ? 'opacity-60' : ''}>
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <CardTitle>Ruling {ruling.ruling_id}</CardTitle>
                  <p className="text-sm text-muted-foreground">Dispute: {ruling.dispute_id}</p>
                </div>
                <Badge variant={ruling.status === 'PENDING_RATIFICATION' ? 'outline' : 'secondary'}>
                  {ruling.status}
                </Badge>
              </CardHeader>
              <CardContent className="space-y-2">
                <p><strong>Precedent:</strong> {ruling.cited_precedent}</p>
                <p><strong>Decision:</strong> {ruling.decision}</p>
                <div className="p-2 bg-secondary rounded text-xs font-mono">
                  {ruling.reasoning_trace}
                </div>
              </CardContent>
              <CardFooter className="flex justify-between items-center text-xs text-muted-foreground">
                <span>Issued: {new Date(ruling.timestamp).toLocaleString()}</span>
                {ruling.status === 'PENDING_RATIFICATION' && (
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => handleOverride(ruling.ruling_id)}
                    disabled={loading}
                  >
                    Override (Constitutional Veto)
                  </Button>
                )}
              </CardFooter>
            </Card>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}
