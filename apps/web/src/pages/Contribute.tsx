import React, { useState } from 'react';
import axios from 'axios';
import { Send, MessageSquare, Lightbulb, Code } from 'lucide-react';

export const Contribute: React.FC = () => {
  const [feedback, setFeedback] = useState('');
  const [type, setType] = useState('feedback');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await axios.post('/api/v200/contribute/feedback', { type, feedback });
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 3000);
    setFeedback('');
  };

  return (
    <div className="space-y-10 max-w-4xl">
      <header>
        <h1 className="text-4xl font-black mb-2">Empower the Ecosystem</h1>
        <p className="text-slate-500">Your contributions directly influence the Workstation's learning trajectories.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
         <ContributionTypeCard
           icon={MessageSquare}
           label="Feedback"
           active={type === 'feedback'}
           onClick={() => setType('feedback')}
         />
         <ContributionTypeCard
           icon={Lightbulb}
           label="Propose Idea"
           active={type === 'proposal'}
           onClick={() => setType('proposal')}
         />
         <ContributionTypeCard
           icon={Code}
           label="Code Snippet"
           active={type === 'code'}
           onClick={() => setType('code')}
         />
      </div>

      <form onSubmit={handleSubmit} className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 space-y-6">
        <textarea
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder={`Enter your ${type} here...`}
          className="w-full bg-sovereign border border-slate-700 rounded-2xl p-6 h-48 focus:outline-none focus:border-aura transition-all"
        />
        <div className="flex justify-between items-center">
          <p className="text-[10px] text-slate-500 uppercase font-black">All contributions are archived in the Merkle-DAG.</p>
          <button
            type="submit"
            className="flex items-center gap-2 px-8 py-4 bg-aura text-sovereign font-bold rounded-xl hover:scale-105 transition-all"
          >
            <Send size={18} />
            Submit Contribution
          </button>
        </div>
      </form>

      {submitted && (
        <div className="fixed bottom-10 right-10 p-6 bg-vital text-sovereign font-black rounded-2xl shadow-2xl animate-bounce">
          Contribution Ingested Successfully!
        </div>
      )}
    </div>
  );
};

const ContributionTypeCard = ({ icon: Icon, label, active, onClick }: any) => (
  <button
    onClick={onClick}
    className={`p-6 rounded-2xl border flex flex-col items-center gap-4 transition-all ${
      active ? 'bg-aura/10 border-aura shadow-[0_0_15px_rgba(56,189,248,0.2)]' : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'
    }`}
  >
    <Icon size={24} className={active ? 'text-aura' : 'text-slate-500'} />
    <span className={`text-xs font-bold uppercase ${active ? 'text-white' : 'text-slate-500'}`}>{label}</span>
  </button>
);
