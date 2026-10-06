import React, { useState } from 'react';
import { Card, Button, toast } from '@workstation/ui';
import { useNavigate } from 'react-router-dom';
import { apiJson, errorMessage, provenanceBadge } from '../lib/api';
import { GraduationCap, Users, Shield, BookOpen, User } from 'lucide-react';

export const LearnTeachModule: React.FC = () => {
  const navigate = useNavigate();
  const [reportLoading, setReportLoading] = useState(false);

  // W403 — this sent { topic, grade_level, learning_objectives } but the endpoint requires
  // { subject, level }, so every call returned 422. There was no res.ok check, so the UI toasted
  // "Class report generated — 12-week curriculum plan ready for 42 students" regardless. The button
  // had therefore NEVER worked and had always reported success — and the 42 students were invented
  // too, since nothing counts students anywhere.
  const [report, setReport] = useState<string>("");
  const [reportError, setReportError] = useState<string>("");
  // W593 (FU-420) — the response's own ai_provenance was never read, so the panel rendered
  // floor-composed Qur'an curriculum with no badge. It is kept and rendered below.
  const [reportServedBy, setReportServedBy] = useState<string>("");
  //  P3.10 — the gate's verdict on this text and its reason, which a learner must be able to read
  const [reviewState, setReviewState] = useState<string>("");
  const [reviewNote, setReviewNote] = useState<string>("");
  const [gateScholars, setGateScholars] = useState<number | null>(null);

  const generateReport = async () => {
    setReportLoading(true);
    setReportError("");
    setReport("");
    setReviewState("");
    setReviewNote("");
    try {
      // P3.10 — THE GATED ROUTE. This posted "Quran & Islamic Studies" to the GENERAL
      // /api/v1/education/curriculum and rendered whatever came back under a disclaimer. Owner ruling
      // 2026-10-05b R7 (§A.12.3) requires a named human scholar to approve AI-composed religious
      // teaching content before a learner sees it and records that A DISCLAIMER IS NOT A REVIEW, so the
      // request now goes through the gate and a learner sees the approved text or the reason there is none.
      const data = await apiJson<{ curriculum?: string | null; review_state?: string;
                                   review_note?: string; served_by?: string;
                                   gate?: { scholars_on_roster?: number; roster_is_empty?: boolean } }>(
        "/api/v1/qep/curriculum",
        {
          method: "POST",
          body: {
            subject: "Quran & Islamic Studies",
            level: "Intermediate",
            duration_weeks: 12,
          },
        },
      );
      setReportServedBy(data.served_by ?? "");
      setReviewState(data.review_state ?? "");
      setReviewNote(data.review_note ?? "");
      setGateScholars(data.gate?.scholars_on_roster ?? null);
      // A WITHHELD PLAN IS NOT AN ERROR. The old code set an error string whenever the text was blank,
      // which would present a deliberate withholding as a service fault — the reader would think the
      // platform had broken rather than that a review is required. The two are kept apart.
      setReport(data.curriculum ?? "");
    } catch (e) {
      setReportError(errorMessage(e));
    } finally {
      setReportLoading(false);
    }
  };
  return (
    <div className="space-y-10">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
        <Card className="p-10 border-aura/20 bg-aura/5">
          <div className="flex items-center gap-6 mb-8">
            <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign">
              <User size={32} />
            </div>
            <div>
              <h3 className="text-2xl font-black text-white uppercase">Learner Dashboard</h3>
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Personalized Learning Path</p>
            </div>
          </div>
          {/* W439 refuter catch: two hardcoded rows ("Surah Al-Baqarah (1-5)" with Resume,
              "Introduction to Tajwid Rules" with Start) posed as the learner's own recorded path —
              constants presented as state; "Resume" asserted progress nothing recorded. The real
              per-learner record lives in the QEP hifz store; this card points there instead of
              inventing a path. (The navs also targeted /qep-religion, which is not a route.) */}
          <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
             <p className="text-xs text-slate-400 font-semibold leading-relaxed mb-4">
                Your real learning path is your hifz schedule — the ayaat you scheduled, what is
                due today, and your recorded reviews live in the QEP studio.
             </p>
             <Button onClick={() => navigate('/qep')} variant="outline" className="text-[10px]">Open QEP studio</Button>
          </div>
        </Card>

        <Card className="p-10 border-highlight/20 bg-highlight/5">
          <div className="flex items-center gap-6 mb-8">
            <div className="w-16 h-16 rounded-2xl bg-highlight flex items-center justify-center text-sovereign">
              <GraduationCap size={32} />
            </div>
            <div>
              <h3 className="text-2xl font-black text-white uppercase">Educator Portal</h3>
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Class Management & Analytics</p>
            </div>
          </div>
          {/* W439 — "Total Students: 42" and "Avg. Mastery: 88%" tiles sat here as literals.
              This file's own W403 comment already said "the 42 students were invented too, since
              nothing counts students anywhere" — the toast was fixed then, the tiles were not. */}
          <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
             <p className="text-xs text-slate-500 font-semibold leading-relaxed">
                No class roster exists on this deployment — student counts and mastery analytics
                appear when a real roster records them, never before.
             </p>
          </div>
          <Button onClick={generateReport} disabled={reportLoading} className="w-full mt-6 bg-highlight text-sovereign uppercase font-black text-xs py-4">{reportLoading ? 'Generating…' : 'Generate a study-plan frame'}</Button>
          {reportError && (
            <p role="alert" className="mt-3 text-[10px] font-bold text-vital leading-relaxed">{reportError}</p>
          )}
          {/* P3.10 — WHY THERE IS NOTHING, when there is nothing. A withheld plan with an empty panel
              beneath it reads as a broken feature; the gate returns a sentence saying whether no scholar
              is engaged, whether the text awaits review or whether a reviewer rejected it, and those are
              different things to tell a learner. The item's own instruction is that this must not be
              dressed, so the reason is shown plainly and no plan is implied. */}
          {reviewState && !report && (
            <div data-testid="learnteach-review-state"
                 className="mt-4 rounded-2xl border border-amber-500/30 bg-amber-500/5 p-4">
              <p className="text-[8px] font-black uppercase tracking-widest text-amber-400/80 mb-2">
                withheld — {reviewState}
              </p>
              <p data-testid="learnteach-review-note" className="text-[10px] text-slate-300 leading-relaxed font-medium">
                {reviewNote}
              </p>
            </div>
          )}
          {report && (
            <div className="mt-4 rounded-2xl border border-slate-800 bg-slate-950 p-4">
              {/* W593 (FU-420, M1 R1.1) — WHAT SERVED IT, AND WHAT IT IS NOT. This rendered a bare <pre>
                  of floor-composed Qur'an curriculum with no badge, no AI-assisted label and no teacher
                  referral, while every sibling tool on this hub carries all three. §11 binds hardest on
                  faith content, and an unlabelled frame is an assertion. */}
              <div className="mb-3 flex items-center gap-2">
                {(() => {
                  const pb = provenanceBadge(reportServedBy);
                  return <span title={pb.title}
                               data-testid="qep-studyframe-provenance"
                               className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${pb.cls}`}>
                    {pb.label}
                  </span>;
                })()}
              </div>
              {/* The caption must now tell the truth about a REVIEWED plan too. It read "not reviewed
                  curriculum" unconditionally, which was true while nothing was gated and becomes false
                  the moment a scholar approves something — and a page that understates its own review
                  is as wrong as one that overstates it. The referral to a teacher stays either way:
                  an approved study plan is still not a substitute for one. */}
              <p data-testid="learnteach-plan-caption" className="mb-3 text-[10px] font-bold text-highlight leading-relaxed">
                {reviewState === "approved"
                  ? <>Reviewed study plan for Qur'an study. {reviewNote} It remains a study plan and not
                      scholarship: study with a qualified teacher.</>
                  : <>AI-assisted study-plan FRAME for Qur'an study — not reviewed curriculum, and not
                      scholarship. The structured floor arranges the headings it was asked for; it does not
                      select what a learner should study. Study with a qualified teacher.</>}
              </p>
              <div className="max-h-72 overflow-y-auto">
                <pre className="whitespace-pre-wrap text-[10px] text-slate-300 leading-relaxed font-medium">{report}</pre>
              </div>
            </div>
          )}
        </Card>
      </div>

      <Card className="p-10">
        <h4 className="text-xl font-black text-white uppercase tracking-tight mb-8 flex items-center gap-4">
           <Shield size={24} className="text-aura" />
           Scholar Governance Board
        </h4>
        {/* W403 — this listed three invented names ("Sheikh Al-Ghauri", "Dr. Fatima Zahra",
            "Ustadh Ibrahim") each captioned "Verified Scholar". No scholar registry exists
            anywhere in the platform — there is no route, no store, and nothing that verifies
            anyone. In a religious-guidance context a user could reasonably trust guidance on the
            strength of a named, "verified" scholar, so inventing them is not a placeholder. */}
        {/* W403 removed three invented "Verified Scholar" names from here and wrote that no registry
            existed anywhere in the platform. That was true then. W594 BUILT one for Owner ruling
            2026-10-05b R7 — agentic_core/api/scholar_review.py, with a roster, an approval bound to the
            exact text approved, and a refusal that distinguishes an empty roster from an unknown
            reviewer. So the old sentence is now false in its reason while still true in its conclusion:
            the registry exists and NOBODY IS ON IT. Narrowing a true statement is a defect of its own,
            so the conclusion is kept and only the reason is corrected. */}
        <p data-testid="learnteach-scholar-board" className="text-xs text-slate-500 font-semibold leading-relaxed max-w-2xl">
           No scholars are verified on this deployment{typeof gateScholars === "number" ? ` — the roster holds ${gateScholars}` : ""}.
           A scholar registry now exists: a roster, an approval bound to the exact text it approved, and a
           refusal that tells an empty roster apart from an unrecognised reviewer. It is EMPTY, which is
           why no names are shown and why no religious curriculum is servable here — nothing can be
           approved until the Owner engages a reviewer. That is the designed state, not a fault, and it
           is not papered over with a disclaimer: a disclaimer is not a review.
        </p>
      </Card>
    </div>
  );
};
