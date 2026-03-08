import React from 'react';
import { Share2 } from 'lucide-react';

const ShareWidget = () => (
  <button className="p-3 bg-emerald-500/20 text-emerald-400 rounded-xl border border-emerald-500/30 flex items-center gap-2 hover:bg-emerald-500/30 transition-all">
    <Share2 size={16} />
    <span className="text-xs font-black uppercase tracking-tighter">Spread the Message (Dawah)</span>
  </button>
);

export default ShareWidget;
