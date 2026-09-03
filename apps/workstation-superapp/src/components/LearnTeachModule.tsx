import React, { useState } from 'react';
import { Card, Button, toast } from '@workstation/ui';
import { useNavigate } from 'react-router-dom';
import { apiJson, errorMessage } from '../lib/api';
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

  const generateReport = async () => {
    setReportLoading(true);
    setReportError("");
    setReport("");
    try {
      const data = await apiJson<{ curriculum?: string; output?: string }>(
        "/api/v1/education/curriculum",
        {
          method: "POST",
          body: {
            subject: "Quran & Islamic Studies",
            level: "Intermediate",
            duration_weeks: 12,
          },
        },
      );
      const text = data.curriculum ?? data.output ?? "";
      if (!text.trim()) {
        setReportError("The curriculum service returned an empty plan.");
      } else {
        setReport(text);
      }
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
          <Button onClick={generateReport} disabled={reportLoading} className="w-full mt-6 bg-highlight text-sovereign uppercase font-black text-xs py-4">{reportLoading ? 'Generating…' : 'Generate Class Report'}</Button>
          {reportError && (
            <p role="alert" className="mt-3 text-[10px] font-bold text-vital leading-relaxed">{reportError}</p>
          )}
          {report && (
            <div className="mt-4 max-h-72 overflow-y-auto rounded-2xl border border-slate-800 bg-slate-950 p-4">
              <pre className="whitespace-pre-wrap text-[10px] text-slate-300 leading-relaxed font-medium">{report}</pre>
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
        <p className="text-xs text-slate-500 font-semibold leading-relaxed max-w-2xl">
           No scholars are verified on this deployment. Scholar verification needs a real registry
           of credentials and an authority that issues them; neither exists here yet, so no names
           are shown. This board will list scholars only once there is something behind the word
           &ldquo;verified&rdquo;.
        </p>
      </Card>
    </div>
  );
};
