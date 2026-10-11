import React, { useEffect, useState } from 'react';
import { apiJson } from '../lib/api';

type Dict = Record<string, any>;

/**
 * W620 (FU-492, M2 v8 R3.5) — the §17.3 living cadence had NO surface: refreshes, their triggers and what
 * each displaced were readable only through the API. This shows each layer's last refresh, whether it is
 * due and why, and the fact that no market or KPI signal is observed by anything.
 */
export const CadencePanel: React.FC<{ scope: string }> = ({ scope }) => {
  const [st, setSt] = useState<Dict | null>(null);
  const [err, setErr] = useState('');
  useEffect(() => {
    apiJson<Dict>(`/api/v1/organism/cadence?scope=${encodeURIComponent(scope)}`)
      .then(setSt).catch(e => setErr(`The cadence could not be read: ${String(e?.message ?? e)}`));
  }, [scope]);
  return (
    <div className="space-y-2" data-testid="cadence-panel">
      <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400">Living cadence (§17.3)</h3>
      {err && <p className="text-[10px] text-vital">{err}</p>}
      {st && Object.entries(st.layers || {}).map(([layer, l]: [string, any]) => (
        <p key={layer} className="text-[10px] text-slate-400" data-testid={`cadence-layer-${layer}`}>
          <span className="font-black uppercase text-slate-300">{layer.replace('_', ' ')}</span> ({l.period}):{' '}
          {l.ever_refreshed ? `last refreshed ${String(l.last_refresh_at).slice(0, 10)} · ${l.refresh_count} on record` : 'never refreshed'}
          {' · '}{l.due?.due ? 'DUE' : 'not due'} — {l.due?.reason}
          {/* P3.30 (ledger v13 R3[7], v16 R3.9) — what served the latest refresh and on what basis, as body text:
              the layer's sentence is derived from the plan's own counts unless a caller supplied it. */}
          {l.latest && (
            <span className="block text-[9px] text-amber-300/80" data-testid={`cadence-source-${layer}`}>
              latest refresh served by {String(l.latest.served_by ?? 'not recorded')}
              {l.latest.applied === false ? ' — kept as a proposal, not written to the plan' : ''}
              {l.latest.provenance_basis ? `. ${String(l.latest.provenance_basis)}` : '. No basis was recorded for it.'}
            </span>
          )}
        </p>
      ))}
      {st?.signals_basis && <p className="text-[9px] text-amber-300/80" data-testid="cadence-signals">{st.signals_basis}.</p>}
    </div>
  );
};

export default CadencePanel;
