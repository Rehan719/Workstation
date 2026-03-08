import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, HelpCircle, MessageSquare, ExternalLink } from 'lucide-react';

const SupportPanel = () => {
  const [feedback, setFeedback] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Feedback submitted:", feedback);
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 3000);
    setFeedback("");
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-12">
      <div className="bg-white p-8 rounded-3xl shadow-xl border border-slate-100">
        <h3 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
          <MessageSquare size={20} className="text-amber-500" />
          In-App Feedback
        </h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="How can we improve your Digital Sanctuary?"
            className="w-full h-32 p-4 bg-slate-50 border border-slate-200 rounded-2xl text-sm focus:ring-2 focus:ring-amber-500 outline-none transition-all"
            required
          />
          <button
            type="submit"
            className="w-full py-4 bg-slate-900 text-white font-black rounded-xl hover:bg-amber-500 transition-all flex items-center justify-center gap-2"
          >
            {submitted ? "BarakAllah Feek!" : "Send Feedback"}
            <Send size={16} />
          </button>
        </form>
      </div>

      <div className="bg-slate-900 p-8 rounded-3xl shadow-xl text-white">
        <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
          <HelpCircle size={20} className="text-amber-400" />
          Community & Support
        </h3>
        <div className="space-y-4">
          <SupportLink
            title="Community Discussions"
            desc="Join fellow seekers and developers on GitHub."
            url="https://github.com/Rehan719/Workstation/discussions"
          />
          <SupportLink
            title="Knowledge Base"
            desc="Explore our comprehensive User Guide and FAQs."
            url="/USER_GUIDE.md"
          />
          <SupportLink
            title="Live Support"
            desc="Connect with moderators in the Seeker Support Halaqa."
            url="#halaqat"
          />
        </div>
      </div>
    </div>
  );
};

const SupportLink = ({ title, desc, url }) => (
  <a
    href={url}
    target="_blank"
    rel="noreferrer"
    className="block p-4 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 transition-all group"
  >
    <div className="flex justify-between items-start mb-1">
      <h4 className="font-bold text-amber-400">{title}</h4>
      <ExternalLink size={14} className="opacity-0 group-hover:opacity-100 transition-opacity" />
    </div>
    <p className="text-xs text-white/50">{desc}</p>
  </a>
);

export default SupportPanel;
