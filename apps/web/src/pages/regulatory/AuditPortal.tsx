import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/badge';
import { Search, ShieldCheck, Download, ExternalLink, Scale } from 'lucide-react';

export default function AuditPortal() {
  const [isVerifying, setIsVerifying] = useState(false);
  const [merkleRoot, setMerkleRoot] = useState('0x6284f...92d1');

  return (
    <div className="p-8 space-y-8 bg-[#fdfdfd] min-h-screen text-slate-900 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">
        <header className="flex justify-between items-end border-b pb-6 border-slate-200">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Scale className="text-blue-600" size={24} />
              <h1 className="text-3xl font-bold tracking-tight text-slate-800">REGULATORY AUDIT PORTAL</h1>
            </div>
            <p className="text-slate-500 font-medium">Virtual Sovereign Business Capital Fund · Institutional Compliance Node</p>
          </div>
          <div className="flex gap-3">
            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200 py-1.5 px-3">
              LIVE SYSTEM ATTESTED
            </Badge>
            <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200 py-1.5 px-3">
              FCA SANDBOX ACTIVE
            </Badge>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <Card className="col-span-2 shadow-sm border-slate-200">
            <CardHeader className="bg-slate-50 border-b border-slate-200">
              <CardTitle className="text-sm font-bold uppercase tracking-wider text-slate-500">Query Transaction Integrity</CardTitle>
            </CardHeader>
            <CardContent className="p-8 space-y-6">
              <div className="flex gap-4">
                <div className="flex-1">
                  <p className="text-xs font-bold text-slate-400 mb-2 uppercase">UEG Merkle Root / Transaction Hash</p>
                  <div className="relative">
                    <Input
                      className="w-full bg-white border-slate-200 pl-10 h-12 text-slate-700"
                      placeholder="Enter cryptographic hash for verification..."
                      defaultValue={merkleRoot}
                    />
                    <Search className="absolute left-3 top-3.5 text-slate-400" size={18} />
                  </div>
                </div>
                <Button
                  onClick={() => setIsVerifying(true)}
                  className="mt-6 h-12 px-8 bg-blue-600 hover:bg-blue-700 text-white font-bold"
                >
                  {isVerifying ? 'VERIFYING...' : 'VERIFY INTEGRITY'}
                </Button>
              </div>

              {isVerifying && (
                <div className="p-6 bg-green-50 border border-green-100 rounded-xl flex items-start gap-4">
                  <ShieldCheck className="text-green-600 mt-1" size={24} />
                  <div className="space-y-1">
                    <p className="font-bold text-green-800">Cryptographic Proof Validated</p>
                    <p className="text-sm text-green-700 leading-relaxed">
                      The hash <b>{merkleRoot}</b> was found in the UEG Merkle-DAG.
                      Linked event: <b>CAPITAL_ALLOCATION_V1</b>.
                      Timestamp: <b>2026-05-09 14:22:10 UTC</b>.
                      Statutory Compliance: <b>100% (Equality Act 2010 verified)</b>.
                    </p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          <div className="space-y-6">
            <Card className="shadow-sm border-slate-200">
              <CardHeader className="bg-slate-50 border-b border-slate-200">
                <CardTitle className="text-xs font-bold uppercase text-slate-500">Compliance Reports</CardTitle>
              </CardHeader>
              <CardContent className="p-4 space-y-3">
                <Button variant="outline" className="w-full justify-between text-slate-700 border-slate-200 hover:bg-slate-50">
                  FCA Quarterly (MiFID II) <Download size={16} className="text-slate-400" />
                </Button>
                <Button variant="outline" className="w-full justify-between text-slate-700 border-slate-200 hover:bg-slate-50">
                  ESMA Transparency Bundle <Download size={16} className="text-slate-400" />
                </Button>
                <Button variant="outline" className="w-full justify-between text-slate-700 border-slate-200 hover:bg-slate-50">
                  Islamic Finance Audit <Download size={16} className="text-slate-400" />
                </Button>
              </CardContent>
            </Card>

            <Card className="shadow-sm border-slate-200 bg-blue-600 text-white">
              <CardContent className="p-6 space-y-4">
                <h3 className="font-bold text-lg">Regulator API Access</h3>
                <p className="text-xs text-blue-100 leading-relaxed">
                  Institutional regulators can subscribe to the vΩ∞ Audit Stream
                  for real-time P&L and risk monitoring.
                </p>
                <Button className="w-full bg-white text-blue-600 hover:bg-blue-50 font-bold">
                  REQUEST API KEY <ExternalLink size={14} className="ml-2" />
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
