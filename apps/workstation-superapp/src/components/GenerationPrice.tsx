import React, { useEffect, useState } from 'react';
import { apiJson } from '../lib/api';

// The price of generating an entity, in the server's words (OWNER RULING 2026-10-13). Every sentence here is a
// field of the answer; the figure is written in one place on the server and nowhere on this page. Nothing is
// charged, and the line says so and why.
interface Condition { condition: string; met: boolean; basis: string }
interface Price {
  price_gbp: number; price_basis: string; credited_against_first_profit_share: boolean; credit_basis: string;
  waived: boolean; waived_basis: string | null; charged_now: boolean; chargeable: boolean;
  conditions: Condition[]; not_charged_basis: string;
}

export const GenerationPrice: React.FC = () => {
  const [price, setPrice] = useState<Price | null>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    apiJson<Price>('/api/v1/genesis/price').then(setPrice).catch(() => setFailed(true));
  }, []);
  if (failed) {
    return <p data-testid="generation-price-unread" className="text-[9px] text-amber-400/80">The price of generating an entity could not be read just now, so none is shown.</p>;
  }
  if (!price) return null;
  return (
    <div data-testid="generation-price" className="p-3 rounded-xl border border-slate-900 bg-slate-950/40">
      <p className="text-[9px] font-black uppercase tracking-widest text-slate-500 mb-1">what generating an entity costs</p>
      <p data-testid="generation-price-basis" className="text-[11px] text-white leading-relaxed">{price.price_basis}.</p>
      {price.credited_against_first_profit_share && (
        <p data-testid="generation-price-credit" className="text-[9px] text-slate-500 leading-relaxed">{price.credit_basis}.</p>
      )}
      {price.waived && price.waived_basis && (
        <p data-testid="generation-price-waived" className="text-[9px] text-slate-500 leading-relaxed">{price.waived_basis}.</p>
      )}
      {!price.charged_now && (
        <p data-testid="generation-price-not-charged" className="text-[9px] text-amber-300/90 leading-relaxed mt-1">{price.not_charged_basis}.</p>
      )}
      <ul className="mt-1 space-y-0.5">
        {price.conditions.map(c => (
          <li key={c.condition} data-testid="generation-price-condition" className="text-[9px] text-slate-500">
            <span className={c.met ? 'text-emerald-400' : 'text-slate-400'}>{c.met ? 'exists' : 'does not exist yet'}</span> · {c.condition} <span className="text-slate-600">— {c.basis}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};
