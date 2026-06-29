import React from 'react';
import { Link } from 'react-router-dom';
import { Layers } from 'lucide-react';

/**
 * §7 — the reconfigurable Resource Fabric is ONE Composer (select · reconfigure · combine · simulate · run ·
 * reuse), reachable ACROSS the three surfaces the vision names: Synthesis Lab · Build-to-Order · Forge.
 * This shared CTA gives every surface a consistent entry into it.
 */
export const FabricLink: React.FC<{ className?: string }> = ({ className = '' }) => (
  <Link to="/resource-fabric"
    title="Open the reconfigurable Resource Fabric — access, select, reconfigure and combine resources, model & simulate before commit"
    className={`inline-flex items-center gap-2 px-3 py-2 rounded-xl border border-aura/40 text-aura text-[10px] font-black uppercase tracking-widest hover:bg-aura/10 transition-all ${className}`}>
    <Layers size={13} /> Resource Fabric — select · reconfigure · combine
  </Link>
);
