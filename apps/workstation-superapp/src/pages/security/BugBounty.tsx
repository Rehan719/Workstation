import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';

export default function BugBountyPortal() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const [report, setReport] = useState({
    title: '',
    description: '',
    severity: 'MEDIUM'
  });

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/security/bounty/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(report)
      });
      const data = await res.json();
      setStatus(`Submitted: ${data.report_id}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-10 space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-extrabold tracking-tight">🐞 Autonomous Bug Bounty</h1>
        <p className="text-xl text-muted-foreground mt-2">
          Help harden the Sovereign Mesh. Bounties paid in WORKREP + USDC.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Submit Vulnerability Report</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Issue Title</label>
            <Input
              value={report.title}
              onChange={e => setReport({...report, title: e.target.value})}
              placeholder="e.g. Invariant breach in Water Cycle PID"
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Severity</label>
            <select
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
              value={report.severity}
              onChange={e => setReport({...report, severity: e.target.value})}
            >
              <option value="LOW">Low</option>
              <option value="MEDIUM">Medium</option>
              <option value="HIGH">High</option>
              <option value="CRITICAL">Critical (Existential)</option>
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Description & Reproduction</label>
            <Textarea
              className="h-32"
              value={report.description}
              onChange={e => setReport({...report, description: e.target.value})}
              placeholder="Provide technical details and steps to reproduce..."
            />
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          {status ? (
            <Badge variant="secondary" className="text-lg py-2 px-4">{status}</Badge>
          ) : (
            <div />
          )}
          <Button onClick={handleSubmit} disabled={loading || !report.title}>
            {loading ? "Triage in Progress..." : "Submit to AI Triage"}
          </Button>
        </CardFooter>
      </Card>

      <div className="text-center text-xs text-muted-foreground">
        Every submission is logged to the UEG and triaged by the Sovereign Resilience Engine.
      </div>
    </div>
  );
}
