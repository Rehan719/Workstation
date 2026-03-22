import React, { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Globe, Zap, Cpu, Settings, MessageSquare, X } from 'lucide-react'

export const CommandPalette = ({ open, setOpen, setActiveTab }: any) => {
  const [query, setQuery] = useState('')

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen((open: boolean) => !open)
      }
    }
    document.addEventListener('keydown', down)
    return () => document.removeEventListener('keydown', down)
  }, [])

  if (!open) return null

  const items = [
    { icon: Zap, label: "Pulse Dashboard", tab: 'dashboard' },
    { icon: MessageSquare, label: "AI CEO Chat", tab: 'ceo' },
    { icon: Cpu, label: "QEP Engine", tab: 'qep' },
    { icon: Settings, label: "System Settings", tab: 'settings' },
    { icon: Globe, label: "Admin Console", tab: 'admin' },
  ]

  const filtered = items.filter(i => i.label.toLowerCase().includes(query.toLowerCase()))

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-[200] flex items-start justify-center pt-[20vh] bg-sovereign/80 backdrop-blur-sm p-4">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="w-full max-w-2xl bg-slate-950 border border-white/10 rounded-3xl shadow-2xl overflow-hidden"
        >
          <div className="p-6 border-b border-white/5 flex items-center gap-4">
            <Search className="text-aura" size={20} />
            <input
              autoFocus
              placeholder="Search command palette..."
              className="flex-1 bg-transparent border-none outline-none text-lg font-bold text-white"
              value={query}
              onChange={e => setQuery(e.target.value)}
            />
            <button onClick={() => setOpen(false)} className="text-slate-500 hover:text-white">
               <X size={20} />
            </button>
          </div>

          <div className="max-h-[400px] overflow-y-auto p-4 space-y-2">
            {filtered.length > 0 ? (
              filtered.map(item => (
                <button
                  key={item.tab}
                  onClick={() => { setActiveTab(item.tab); setOpen(false); }}
                  className="w-full flex items-center gap-4 px-4 py-4 rounded-2xl hover:bg-aura/10 transition-all group text-left"
                >
                  <div className="p-2 bg-slate-900 rounded-xl group-hover:bg-aura group-hover:text-sovereign transition-all text-aura">
                    <item.icon size={20} />
                  </div>
                  <span className="font-black uppercase tracking-widest text-xs">{item.label}</span>
                </button>
              ))
            ) : (
              <div className="p-10 text-center text-slate-500 font-bold uppercase tracking-widest text-xs">No results found.</div>
            )}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  )
}
