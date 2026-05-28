import React, { useEffect, useState } from 'react'
import { Command } from 'cmdk'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Globe, Zap, Cpu, Settings, MessageSquare } from 'lucide-react'

export const CommandPalette = ({ open, setOpen, setActiveTab }: any) => {
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

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-[200] flex items-start justify-center pt-[20vh] bg-sovereign/80 backdrop-blur-sm">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="w-full max-w-2xl bg-surface border border-white/10 rounded-3xl shadow-2xl overflow-hidden glass-card"
        >
          <Command className="p-4">
            <div className="flex items-center gap-3 border-b border-white/5 pb-4 mb-4">
              <Search className="text-aura" size={20} />
              <Command.Input
                placeholder="Search command palette..."
                className="flex-1 bg-transparent border-none outline-none text-lg font-bold placeholder-slate-600"
              />
            </div>
            <Command.List className="max-h-[300px] overflow-y-auto custom-scrollbar space-y-2">
              <Command.Empty className="p-4 text-center text-slate-500 font-bold">No results found.</Command.Empty>

              <Command.Group heading="Navigation" className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em] mb-2 px-2">
                <Item icon={Zap} label="Pulse Dashboard" onSelect={() => { setActiveTab('dashboard'); setOpen(false); }} />
                <Item icon={MessageSquare} label="AI CEO Chat" onSelect={() => { setActiveTab('ceo'); setOpen(false); }} />
                <Item icon={Globe} label="Federation Portal" onSelect={() => { setActiveTab('fed-portal'); setOpen(false); }} />
                <Item icon={Cpu} label="QEP Engine" onSelect={() => { setActiveTab('qep'); setOpen(false); }} />
              </Command.Group>

              <Command.Group heading="Domains" className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em] mt-4 mb-2 px-2">
                <Item icon={Globe} label="Religion Hub" onSelect={() => { setActiveTab('religion'); setOpen(false); }} />
                <Item icon={Zap} label="Science Hub" onSelect={() => { setActiveTab('science'); setOpen(false); }} />
                <Item icon={Settings} label="Law Hub" onSelect={() => { setActiveTab('law'); setOpen(false); }} />
                <Item icon={Globe} label="Employment Hub" onSelect={() => { setActiveTab('employment'); setOpen(false); }} />
                <Item icon={Globe} label="Education Hub" onSelect={() => { setActiveTab('education'); setOpen(false); }} />
              </Command.Group>

              <Command.Group heading="Settings" className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em] mt-4 mb-2 px-2">
                <Item icon={Settings} label="System Settings" onSelect={() => { setActiveTab('settings'); setOpen(false); }} />
                <Item icon={Globe} label="Admin Console" onSelect={() => { setActiveTab('admin'); setOpen(false); }} />
              </Command.Group>
            </Command.List>
          </Command>
        </motion.div>
      </div>
    </AnimatePresence>
  )
}

const Item = ({ icon: Icon, label, onSelect }: any) => (
  <Command.Item
    onSelect={onSelect}
    className="flex items-center gap-4 px-4 py-3 rounded-xl cursor-pointer hover:bg-aura/10 transition-colors group"
  >
    <div className="p-2 bg-white/5 rounded-lg group-hover:text-aura">
      <Icon size={18} />
    </div>
    <span className="font-bold text-sm">{label}</span>
  </Command.Item>
)
