import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Folders, ArrowRight } from 'lucide-react';

interface StartProjectCTAProps {
  realm: string;
  domain?: string;
  label?: string;
}

/**
 * Drop-in banner for any domain/realm page.
 * Navigates to /projects with query params so ProjectsHub
 * auto-opens the create form pre-filled for this realm.
 */
export const StartProjectCTA: React.FC<StartProjectCTAProps> = ({
  realm,
  domain = 'product',
  label,
}) => {
  const navigate = useNavigate();
  const displayLabel = label ?? `Start a ${realm.charAt(0).toUpperCase() + realm.slice(1)} Project`;

  return (
    <button
      type="button"
      onClick={() => navigate(`/projects?realm=${realm}&domain=${domain}&new=1`)}
      className="group flex items-center justify-between w-full px-5 py-4 rounded-2xl border border-aura/20 bg-aura/5 hover:border-aura/50 hover:bg-aura/10 transition-all"
    >
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-xl bg-aura/20 flex items-center justify-center">
          <Folders size={14} className="text-aura" />
        </div>
        <div className="text-left">
          <p className="text-[10px] font-black uppercase tracking-[0.25em] text-aura">{displayLabel}</p>
          <p className="text-[9px] text-slate-500 mt-0.5">Generate a Concept, Prototype, and Commercialisation plan using AI</p>
        </div>
      </div>
      <ArrowRight size={14} className="text-aura opacity-0 group-hover:opacity-100 transition-opacity" />
    </button>
  );
};
