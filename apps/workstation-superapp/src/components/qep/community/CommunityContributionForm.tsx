import React from 'react';

const CommunityContributionForm: React.FC = () => {
  const [formData, setFormData] = React.useState({
    title: '',
    category: 'Knowledge',
    content: '',
    tags: '',
    contributor: 'User_123'
  });

  const [status, setStatus] = React.useState<null | 'submitting' | 'success' | 'error'>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('submitting');
    // Simulated backend submission to community_contribution_orchestrator
    setTimeout(() => {
      setStatus('success');
    }, 1500);
  };

  return (
    <div className="contribution-form p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-700">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-bold text-emerald-400">Share Your Knowledge</h2>
        <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded-full text-xs font-mono border border-emerald-500/30">v8.3 Contribution Flow</span>
      </div>

      {status === 'success' ? (
        <div className="bg-emerald-900/30 border border-emerald-500/40 p-6 rounded-lg text-center animate-pulse">
          <div className="text-4xl mb-4">✅</div>
          <h3 className="text-xl font-bold text-emerald-400 mb-2">BarakAllahu Feek!</h3>
          <p className="text-sm text-emerald-500/80 mb-6">Your contribution has been submitted for scholar review and pipeline routing.</p>
          <div className="text-[10px] text-slate-500 bg-slate-800 p-2 rounded">
            Audit Trail Hash: SHA256-V83-COMM-POC-001
          </div>
          <button type="button" onClick={() => setStatus(null)} className="mt-8 px-4 py-2 bg-emerald-600 rounded text-sm hover:bg-emerald-500 transition-colors">
            New Submission
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-emerald-500/70 mb-1 uppercase tracking-wider">Module Title</label>
            <input
              type="text"
              className="w-full bg-slate-800 border border-slate-700 p-2 rounded text-sm focus:border-emerald-500 outline-none transition-colors"
              placeholder="e.g. Advanced Tajweed Audio (Warsh)"
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="contrib-category" className="block text-xs font-bold text-emerald-500/70 mb-1 uppercase tracking-wider">Category</label>
              <select
                id="contrib-category"
                className="w-full bg-slate-800 border border-slate-700 p-2 rounded text-sm focus:border-emerald-500 outline-none transition-colors"
                value={formData.category}
                onChange={(e) => setFormData({...formData, category: e.target.value})}
              >
                <option>Knowledge</option>
                <option>Audio</option>
                <option>Interactive</option>
                <option>Tafsir</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-emerald-500/70 mb-1 uppercase tracking-wider">Tags</label>
              <input
                type="text"
                className="w-full bg-slate-800 border border-slate-700 p-2 rounded text-sm focus:border-emerald-500 outline-none transition-colors"
                placeholder="Tajweed, Audio, Intermediate"
                value={formData.tags}
                onChange={(e) => setFormData({...formData, tags: e.target.value})}
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-emerald-500/70 mb-1 uppercase tracking-wider">Description/Content</label>
            <textarea
              rows={4}
              className="w-full bg-slate-800 border border-slate-700 p-2 rounded text-sm focus:border-emerald-500 outline-none transition-colors"
              placeholder="Describe your module or paste the content..."
              value={formData.content}
              onChange={(e) => setFormData({...formData, content: e.target.value})}
              required
            ></textarea>
          </div>

          <div className="pt-4">
            <button
              type="submit"
              disabled={status === 'submitting'}
              className={`w-full py-3 ${status === 'submitting' ? 'bg-slate-700 text-slate-400' : 'bg-emerald-600 hover:bg-emerald-500'} text-white font-bold rounded transition-colors text-sm shadow-lg shadow-emerald-900/20`}
            >
              {status === 'submitting' ? 'Processing Pipelines...' : 'Submit to VSB Community'}
            </button>
          </div>

          <p className="text-[10px] text-center text-slate-500 mt-4 italic">
            By submitting, you agree to the VSB Community License (CC BY-NC-SA 4.0).
          </p>
        </form>
      )}
    </div>
  );
};

export default CommunityContributionForm;
