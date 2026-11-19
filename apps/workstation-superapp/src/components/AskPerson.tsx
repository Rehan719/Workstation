// W968 (P5.14 clause 6, the Owner's ruling of 2026-10-12) — ONE SHAPE FOR EVERY QUESTION THE PLATFORM PUTS TO A
// PERSON. "Every question the platform puts to a person states what differs between the options, what it costs to
// undo, which is recommended, and whether it is a confirmation or a decision; an act that cannot be undone is not
// performed on a general yes." Until now the four acts that cannot be undone ran on a bare window.confirm: one
// sentence and an OK button.
//
// A question here names its kind, and for each option what differs and what undoing it costs; exactly one option is
// recommended. An act that cannot be undone waits for its own name to be typed back, so a general yes cannot perform
// it. The page that asks writes the words, because only it knows the act; this component holds the shape.
import React, { useState } from 'react';

export interface AskOption {
  id: string;
  label: string;          // the words on the option's button
  differs: string;        // what choosing it does that the other options do not
  undo: string;           // what undoing it costs, or that it cannot be undone
  recommended?: boolean;  // exactly one option of a question is recommended
}

export interface AskPersonProps {
  question: string;
  kind: 'confirmation' | 'decision';
  options: AskOption[];
  // an act that cannot be undone: its option waits until `text` is typed back exactly
  typeBack?: { optionId: string; text: string; label: string };
  onChoose: (optionId: string) => void;
}

export const KIND_SAID: Record<AskPersonProps['kind'], string> = {
  confirmation: 'A confirmation: you asked for this, and nothing happens unless you confirm it here.',
  decision: 'A decision: choose one of these. Each is said below with what it does and what undoing it costs.',
};

export const AskPerson: React.FC<AskPersonProps> = ({ question, kind, options, typeBack, onChoose }) => {
  const [typed, setTyped] = useState('');
  const waiting = (o: AskOption) => !!typeBack && typeBack.optionId === o.id && typed !== typeBack.text;
  return (
    <div role="dialog" aria-label={question} data-testid="ask-person"
      className="p-4 rounded-xl border border-amber-500/40 bg-slate-950 space-y-3">
      <p data-testid="ask-question" className="text-sm font-black text-white">{question}</p>
      <p data-testid="ask-kind" className="text-[10px] text-slate-400">{KIND_SAID[kind]}</p>
      <ul className="space-y-2">
        {options.map(o => (
          <li key={o.id} data-testid={`ask-option-${o.id}`} className="text-[10px] text-slate-300 leading-relaxed">
            <span className="font-black uppercase tracking-widest text-[9px] text-white">{o.label}</span>
            {o.recommended && <span data-testid={`ask-recommended-${o.id}`} className="ml-2 text-emerald-400 font-black">Recommended</span>}
            <span className="block">What it does: {o.differs}</span>
            <span className="block">To undo it: {o.undo}</span>
          </li>
        ))}
      </ul>
      {typeBack && (
        <label className="block text-[10px] text-slate-400">
          {typeBack.label}
          <input aria-label={typeBack.label} data-testid="ask-type-back" value={typed} onChange={e => setTyped(e.target.value)}
            className="block w-full mt-1 text-xs bg-slate-900 border border-slate-800 rounded-lg p-2 text-slate-200" />
        </label>
      )}
      <div className="flex gap-2 flex-wrap">
        {options.map(o => (
          <button key={o.id} type="button" data-testid={`ask-choose-${o.id}`} disabled={waiting(o)} onClick={() => onChoose(o.id)}
            className="text-[9px] font-black uppercase tracking-widest px-3 py-2 rounded-lg bg-slate-800 text-slate-200 disabled:opacity-40">
            {o.label}
          </button>
        ))}
      </div>
    </div>
  );
};
