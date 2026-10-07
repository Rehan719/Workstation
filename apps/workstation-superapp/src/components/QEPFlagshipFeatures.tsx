import React, { useState, useEffect } from 'react';
import { Card, Button, Badge, notImplemented} from '@workstation/ui';
import {
  Mic,
  Book,
  Trophy,
  Glasses,
  GraduationCap,
  Palette,
  Users,
  LineChart,
  Award,
  WifiOff,
  CreditCard,
  MessageCircle,
  Share2,
  Play,
  CheckCircle
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const QEPFlagshipFeatures: React.FC = () => {
  const [activeFeature, setActiveFeature] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  const features = [
    // W613 (FU-476/FU-499, M1 v8 R1.1 R5.0) — three of these cards misstated what exists and what a ruling
    // forbids. Recitation analysis is not PLANNED: Appendix A.9.1 RULES that recitation is never scored, and
    // only an Owner ruling over a validated, scholar-reviewed phonetic model could reopen it. A certificate is
    // not planned: A.12.2 RULES that QEP issues none in its own name. And the leaderboard is not missing: it
    // is live in the QEP studio. A boundary shown as a backlog item is the defect, so each card now says which
    // it is, and `kind` drives the panel so a click cannot say 'no backend' about a live module.
    { id: 'tajwid', name: 'AI Tajwīd Coach', icon: Mic, color: 'text-aura', kind: 'refused', desc: 'Not offered, by ruling: recitation is never scored (Appendix A.9.1). Only an Owner ruling over a validated, scholar-reviewed phonetic model could reopen it. Written-recall and Tajwīd teaching tools ARE live in the QEP studio.' },
    { id: 'memorization', name: 'Memorization Suite', icon: Book, color: 'text-highlight', kind: 'live', desc: 'LIVE (W439): real SM-2 scheduling, reviews and progress — in the QEP studio above.' },
    { id: 'competitions', name: 'Competitions', icon: Trophy, color: 'text-aura', kind: 'live', desc: 'LIVE: the leaderboard in the QEP studio above ranks recorded XP, with its formula shown. Tournaments are not built, and a recitation contest never will be: recitation is never scored (A.9.1).' },
    { id: 'ar_vr', name: 'AI/AR Immersion', icon: Glasses, color: 'text-vital', desc: 'Planned: 360° history and Tajwīd overlays — no WebXR code and no scene asset exist yet.' },
    { id: 'education', name: 'Learn-Teach', icon: GraduationCap, color: 'text-aura', desc: 'Guided playlists are fixed syllabus content. No cohort, session or retention data is recorded, so no student analytics are reported.' },
    // W593 (FU-433, M1 R5.0) — this read 'Interface adjusts to age and emotion.' Appendix A.9.4
    // RATIFIES the opposite: adaptation follows an explicit SAVED PREFERENCE (the W428 profile),
    // never inferred affect, and reopening it needs an Owner ruling. The live mechanism is already
    // honest — AdaptiveUIProvider derives its label from the stored ui.tone preference and the hubs
    // render it as "TONE (saved pref.)" — so only this card claimed it. Stating what is true and
    // what is refused, rather than deleting the card, is ACCEPT clause (4).
    { id: 'adaptive_ui', name: 'Adaptive UI', icon: Palette, color: 'text-highlight', desc: 'Planned: layout follows a chosen age band. Tone follows your SAVED PREFERENCE — emotion is never inferred (a ratified boundary, Appendix A.9.4).' },
    { id: 'community', name: 'Community', icon: Users, color: 'text-aura', desc: 'Planned: forums and virtual study circles — nothing stores a forum, a post or a circle yet.' },
    { id: 'analytics', name: 'Growth Analytics', icon: LineChart, color: 'text-vital', desc: 'Your memorisation review counts are real, from your own records. Fluency, accuracy and consistency are NOT measured, so they are reported empty.' },
    { id: 'credentials', name: 'Certifications', icon: Award, color: 'text-aura', kind: 'refused', desc: 'Not offered, by ruling: QEP issues no certificate in its own name (Appendix A.12.2). A record of completion is issued instead, and it states that it is not a credential.' },
    { id: 'offline', name: 'Offline Access', icon: WifiOff, color: 'text-highlight', desc: 'Planned: learn without connectivity — no offline sync and no service worker exist yet.' },
    { id: 'finance', name: 'Islamic Finance', icon: CreditCard, color: 'text-aura', desc: 'Planned: zakat-eligible donations — no payment rails are enabled (Owner-gated).' },
    { id: 'assistant', name: 'AI Assistant', icon: MessageCircle, color: 'text-vital', desc: 'Planned: conversational guidance — no reasoning resource is wired here, so no answer is produced. A ruling belongs to a qualified scholar.' },
    { id: 'swarm', name: 'Swarm Learning', icon: Share2, color: 'text-aura', desc: 'Planned: AI-coordinated group pacing — not implemented; nothing writes a study swarm yet.' },
  ];

  // Ledger cluster 3 — this used to sleep 1.2s and render hardcoded mock results for all 13
  // cards (fake tajwid scores, a fabricated "ISSUED" certificate id, invented active-user counts,
  // a zakat eligibility flag) with a success tick, calling no backend. None of these modules has
  // an endpoint yet, so selecting a card now says so honestly instead of inventing an outcome.
  const activeKind = features.find(f => f.id === activeFeature)?.kind;
  const launchFeature = (id: string) => {
    setActiveFeature(id);
    // W439 refuter catch: the one LIVE module (memorization) opened a panel claiming
    // "not yet built" — the panel now matches the card's truth
    const k = features.find(f => f.id === id)?.kind;
    setData({ status: k === 'live' ? 'live' : k === 'refused' ? 'not offered (a ratified boundary)' : 'not yet built' });
  };

  return (
    <div className="space-y-12">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {features.map((f) => (
          <Card
            key={f.id}
            className={`p-6 border-2 transition-all cursor-pointer group hover:scale-[1.02] ${activeFeature === f.id ? 'border-aura bg-aura/5' : 'border-slate-900 hover:border-aura/30'}`}
            onClick={() => launchFeature(f.id)}
          >
            <div className="flex justify-between items-start mb-4">
              <div className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${activeFeature === f.id ? 'bg-aura text-sovereign shadow-xl shadow-aura/20' : 'bg-slate-900 text-aura group-hover:bg-aura/10'}`}>
                <f.icon size={24} />
              </div>
              {/* W439 — the CheckCircle success tick on selection signalled completion for
                  unbuilt modules; a selection is not a success */}
              <span className="text-[7px] font-black uppercase px-1.5 py-0.5 rounded bg-amber-500/15 text-amber-400">{f.id === 'memorization' ? 'live' : 'planned'}</span>
            </div>
            <h3 className="text-lg font-black text-white mb-2">{f.name}</h3>
            <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest leading-relaxed">{f.desc}</p>
          </Card>
        ))}
      </div>

      <AnimatePresence mode="wait">
        {activeFeature && data && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
          >
            <Card className="p-10 bg-slate-950 border-aura/30 relative overflow-hidden group">
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(100,255,218,0.03)_0%,transparent_70%)]"></div>

              <div className="relative z-10">
                <div className="flex justify-between items-center mb-10 border-b border-white/5 pb-8">
                  <div className="flex items-center gap-6">
                    <div className="w-16 h-16 rounded-3xl bg-aura flex items-center justify-center text-sovereign shadow-2xl shadow-aura/30">
                       {React.createElement(features.find(f => f.id === activeFeature)?.icon || Play, { size: 32 })}
                    </div>
                    <div>
                      <h3 className="text-3xl font-black text-white uppercase tracking-tighter">
                        {features.find(f => f.id === activeFeature)?.name} Module
                      </h3>
                      <p className="text-[10px] font-black text-amber-400 uppercase tracking-widest">{activeKind === 'live' ? 'LIVE — use the QEP studio above' : activeKind === 'refused' ? 'Not offered — a ratified boundary, not a backlog item' : 'Not yet built — nothing was run'}</p>
                    </div>
                  </div>
                  <Button variant="outline" onClick={() => setActiveFeature(null)}>Minimize</Button>
                </div>

                <p className="text-sm text-slate-400 font-bold leading-relaxed mb-8 max-w-2xl">
                  {activeKind === 'live'
                    ? `This module IS live in the QEP studio rendered above this roadmap: ${features.find(f => f.id === activeFeature)?.desc ?? ''} `
                    : activeKind === 'refused'
                      ? `This is not a module waiting to be built. ${features.find(f => f.id === activeFeature)?.desc ?? ''} `
                      : 'This module is described in the platform plan but has no backend yet, so no result can be shown — a fabricated one would be worse than none. '} The capabilities that ARE live for this
                  domain are the AI-mediated domain tools on this page, the{' '}
                  <a href="/native-ai" className="text-aura underline underline-offset-2">Native AI fabric</a>, and{' '}
                  <a href="/genesis" className="text-aura underline underline-offset-2">Genesis</a> for establishing a living enterprise.
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                  {Object.entries(data).map(([key, val]: [string, any]) => (
                    <div key={key} className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 hover:border-aura/20 transition-all">
                      <p className="text-[10px] font-black text-slate-500 uppercase mb-2 tracking-[0.2em]">{key.replace('_', ' ')}</p>
                      <p className="text-2xl font-black text-white">
                        {Array.isArray(val) ? val.length : (typeof val === 'number' ? (val * 100).toFixed(0) + '%' : String(val))}
                      </p>
                    </div>
                  ))}
                </div>

                <div className="mt-10 pt-8 border-t border-white/5 flex justify-between items-center">
                   <div className="flex gap-4">
                      {/* W412 — a "GaaS Verified" badge used to sit here on every result panel.
                          Nothing ran a GaaS verification on these results; the badge asserted a
                          governance check that never happened. The version tag is a fact and stays. */}
                      <Badge color="highlight">v0.9-P0</Badge>
                   </div>
                   <Button onClick={() => notImplemented('Launch Full Dashboard')} className="bg-aura text-sovereign px-8 py-4 rounded-xl font-black uppercase tracking-widest text-[10px]">
                      Launch Full Dashboard
                   </Button>
                </div>
              </div>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
