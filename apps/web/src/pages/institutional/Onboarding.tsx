import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Shield, Globe, Landmark, Fingerprint, CheckCircle2, ArrowRight, Lock } from 'lucide-react';

const InstitutionalOnboarding: React.FC = () => {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<'idle' | 'processing' | 'success' | 'error'>('idle');
  const [formData, setFormData] = useState({
    entityName: '',
    jurisdiction: '',
    pqcIdentity: '',
    intendedAUM: '0',
  });

  const nextStep = () => setStep(prev => prev + 1);
  const prevStep = () => setStep(prev => prev - 1);

  const handleSimulateHandshake = () => {
    setLoading(true);
    setStatus('processing');
    setTimeout(() => {
      setLoading(false);
      setStatus('success');
      nextStep();
    }, 2000);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <div className="flex flex-col space-y-2">
        <h1 className="text-4xl font-black tracking-tighter uppercase text-slate-900 flex items-center gap-3">
          <Landmark className="w-10 h-10" />
          Institutional Sovereign Onboarding
        </h1>
        <p className="text-slate-500 font-medium">
          Phase 7: Federated Mesh Integration & Regulatory Handshake Protocol vΩ∞
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        {[
          { id: 1, label: 'Entity Auth', icon: Shield },
          { id: 2, label: 'PQC Identity', icon: Lock },
          { id: 3, label: 'Handshake', icon: Globe },
          { id: 4, label: 'Governance', icon: CheckCircle2 }
        ].map((s) => (
          <div
            key={s.id}
            className={`flex items-center gap-2 p-3 rounded-lg border-2 transition-all ${
              step === s.id ? 'border-indigo-600 bg-indigo-50/50' : 'border-slate-200'
            }`}
          >
            <s.icon className={`w-5 h-5 ${step >= s.id ? 'text-indigo-600' : 'text-slate-400'}`} />
            <span className={`text-xs font-bold uppercase tracking-wider ${step >= s.id ? 'text-indigo-900' : 'text-slate-400'}`}>
              {s.label}
            </span>
          </div>
        ))}
      </div>

      {step === 1 && (
        <Card className="border-4 border-slate-900 shadow-[8px_8px_0px_0px_rgba(0,0,0,0.1)]">
          <CardHeader className="bg-slate-900 text-white">
            <CardTitle className="text-xl uppercase tracking-widest flex items-center gap-2">
              <Shield className="w-6 h-6" />
              1. Entity Authentication & Jurisdiction
            </CardTitle>
          </CardHeader>
          <CardContent className="p-8 space-y-6">
            <div className="space-y-4">
              <div>
                <label className="text-xs font-black uppercase text-slate-500 mb-1 block tracking-widest">Entity Name</label>
                <Input
                  placeholder="e.g. Sovereign Wealth Fund v7"
                  value={formData.entityName}
                  onChange={(e) => setFormData({...formData, entityName: e.target.value})}
                  className="border-2 border-slate-200 font-bold"
                />
              </div>
              <div>
                <label className="text-xs font-black uppercase text-slate-500 mb-1 block tracking-widest">Regulatory Jurisdiction</label>
                <select
                  className="w-full h-10 px-3 rounded-md border-2 border-slate-200 font-bold bg-white"
                  value={formData.jurisdiction}
                  onChange={(e) => setFormData({...formData, jurisdiction: e.target.value})}
                >
                  <option value="">Select Jurisdiction...</option>
                  <option value="UK">United Kingdom (FCA/MiFID II)</option>
                  <option value="WY">Wyoming (DAO Sovereign)</option>
                  <option value="EU">European Union (ESMA)</option>
                  <option value="CH">Switzerland (FINMA)</option>
                </select>
              </div>
            </div>
            <div className="p-4 bg-slate-50 border-2 border-slate-200 rounded-lg">
              <p className="text-xs text-slate-600 leading-relaxed italic">
                Note: Institutional onboarding triggers an automatic GaaS v4 Audit trail.
                All jurisdictional data is encrypted via Kyber-1024 before transmission to the Mesh.
              </p>
            </div>
          </CardContent>
          <CardFooter className="p-6 bg-slate-50 border-t-2 border-slate-200 flex justify-end">
            <Button
              onClick={nextStep}
              disabled={!formData.entityName || !formData.jurisdiction}
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-black uppercase tracking-widest"
            >
              Verify & Continue <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          </CardFooter>
        </Card>
      )}

      {step === 2 && (
        <Card className="border-4 border-slate-900 shadow-[8px_8px_0px_0px_rgba(0,0,0,0.1)]">
          <CardHeader className="bg-slate-900 text-white">
            <CardTitle className="text-xl uppercase tracking-widest flex items-center gap-2">
              <Lock className="w-6 h-6" />
              2. Quantum-Resistant Identity Setup
            </CardTitle>
          </CardHeader>
          <CardContent className="p-8 space-y-6">
            <div className="flex items-center gap-4 p-4 bg-indigo-50 border-2 border-indigo-200 rounded-lg">
              <Fingerprint className="w-12 h-12 text-indigo-600" />
              <div>
                <h4 className="font-black text-indigo-900 uppercase">Dilithium-5 Signature Generated</h4>
                <p className="text-xs text-indigo-700">A new institutional PQC seed has been generated for your entity.</p>
              </div>
            </div>
            <div>
              <label className="text-xs font-black uppercase text-slate-500 mb-1 block tracking-widest">Public Identity (PQC-DID)</label>
              <Input
                readOnly
                value="did:vsb:pqc:inst:0x7a2...9f3e"
                className="bg-slate-100 border-2 border-slate-200 font-mono text-xs"
              />
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="border-green-500 text-green-700">Kyber-1024 ACTIVE</Badge>
              <Badge variant="outline" className="border-green-500 text-green-700">ISO 20022 READY</Badge>
            </div>
          </CardContent>
          <CardFooter className="p-6 bg-slate-50 border-t-2 border-slate-200 flex justify-between">
            <Button variant="outline" onClick={prevStep} className="font-black uppercase tracking-widest border-2 border-slate-900">Back</Button>
            <Button onClick={nextStep} className="bg-indigo-600 hover:bg-indigo-700 text-white font-black uppercase tracking-widest">
              Register ID <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          </CardFooter>
        </Card>
      )}

      {step === 3 && (
        <Card className="border-4 border-slate-900 shadow-[8px_8px_0px_0px_rgba(0,0,0,0.1)]">
          <CardHeader className="bg-slate-900 text-white">
            <CardTitle className="text-xl uppercase tracking-widest flex items-center gap-2">
              <Globe className="w-6 h-6" />
              3. Federated Mesh Handshake
            </CardTitle>
          </CardHeader>
          <CardContent className="p-8 space-y-6 text-center">
            {status === 'processing' ? (
              <div className="space-y-4 py-10">
                <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-indigo-600 mx-auto"></div>
                <p className="text-sm font-black uppercase text-slate-600 animate-pulse tracking-widest">Negotiating Sovereignty Treaty...</p>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="p-6 bg-slate-50 border-2 border-dashed border-slate-300 rounded-xl">
                  <Globe className="w-16 h-16 text-slate-300 mx-auto mb-4" />
                  <h3 className="text-lg font-black uppercase text-slate-900">Ready for Mesh Discovery</h3>
                  <p className="text-sm text-slate-500">Your entity will be broadcasted to the Sovereign Mesh for bilateral arbitrage treaty negotiation.</p>
                </div>
                <Button
                  onClick={handleSimulateHandshake}
                  className="w-full h-16 bg-slate-900 hover:bg-slate-800 text-white font-black text-xl uppercase tracking-[0.2em]"
                >
                  Initiate Handshake vΩ∞
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {step === 4 && (
        <Card className="border-4 border-green-600 shadow-[8px_8px_0px_0px_rgba(34,197,94,0.1)]">
          <CardHeader className="bg-green-600 text-white">
            <CardTitle className="text-xl uppercase tracking-widest flex items-center gap-2">
              <CheckCircle2 className="w-6 h-6" />
              4. Sovereign Integration Complete
            </CardTitle>
          </CardHeader>
          <CardContent className="p-8 space-y-6">
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center">
                <CheckCircle2 className="w-12 h-12 text-green-600" />
              </div>
              <h2 className="text-2xl font-black text-slate-900 uppercase">Institution Active</h2>
              <p className="text-slate-600 max-w-md">
                {formData.entityName} is now a validated node in the JULES vΩ∞ Mesh.
                Institutional arbitrage limits are set to 5% of AUM per treaty.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-slate-50 border-2 border-slate-200 rounded-lg">
                <p className="text-[10px] font-black uppercase text-slate-400 mb-1">MiFID II ID</p>
                <p className="text-xs font-mono font-bold">RTS-22-Ω-{Math.random().toString(36).substr(2, 9).toUpperCase()}</p>
              </div>
              <div className="p-4 bg-slate-50 border-2 border-slate-200 rounded-lg">
                <p className="text-[10px] font-black uppercase text-slate-400 mb-1">Audit Root</p>
                <p className="text-xs font-mono font-bold">0xFD...{Math.random().toString(16).substr(2, 6)}</p>
              </div>
            </div>
          </CardContent>
          <CardFooter className="p-6 bg-slate-50 border-t-2 border-slate-200 flex flex-col gap-3">
            <Button className="w-full bg-slate-900 text-white font-black uppercase tracking-widest py-6">
              Enter Institutional Dashboard
            </Button>
            <Button variant="ghost" className="text-slate-500 font-bold uppercase text-xs" onClick={() => setStep(1)}>
              Register Another Entity
            </Button>
          </CardFooter>
        </Card>
      )}
    </div>
  );
};

export default InstitutionalOnboarding;
