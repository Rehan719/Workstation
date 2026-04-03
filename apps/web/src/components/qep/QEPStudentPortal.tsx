import React, { useState } from 'react';
import { Card, Button, Badge } from '@workstation/ui';
import {
  BookOpen,
  Award,
  Users,
  Play,
  CheckCircle,
  GraduationCap,
  Star,
  Activity,
  User,
  Layout,
  MessageCircle,
  HelpCircle,
  Settings
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const QEPStudentPortal = () => {
  const [activeTab, setActiveTab] = useState('lessons');
  const [currentLevel, setCurrentLevel] = useState(1);
  const [juzMemorized, setJuzMemorized] = useState(1);

  const lessons = [
    { id: 1, title: 'Al-Fatihah', type: 'Recitation', status: 'Completed', level: 1 },
    { id: 2, title: 'Introduction to Tajweed', type: 'Rules', status: 'In Progress', level: 1 },
    { id: 3, title: 'Noon Sakinah Rules', type: 'Tajweed', status: 'Locked', level: 2 },
  ];

  const badges = [
    { name: 'Beginner (Mubtadi)', tier: 1, icon: '🥉' },
    { name: 'First Surah Complete', tier: 1, icon: '🌟' },
  ];

  return (
    <div className="flex min-h-screen bg-slate-950 text-white font-sans selection:bg-aura/30 selection:text-white">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-900 flex flex-col p-6 space-y-8 bg-slate-950/50 backdrop-blur-xl sticky top-0 h-screen">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-aura to-sovereign flex items-center justify-center text-white shadow-lg shadow-aura/20">
            <GraduationCap size={20} />
          </div>
          <div>
            <h1 className="text-sm font-black tracking-widest uppercase">QEP Portal</h1>
            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">v8.0 Religion Domain</p>
          </div>
        </div>

        <nav className="space-y-1">
          {[
            { id: 'lessons', label: 'Curriculum', icon: BookOpen },
            { id: 'hifz', label: 'Hifz Tracker', icon: Activity },
            { id: 'achievements', label: 'Achievements', icon: Award },
            { id: 'community', label: 'Community', icon: Users },
            { id: 'profile', label: 'Student Profile', icon: User },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 text-xs font-black uppercase tracking-widest group ${
                activeTab === item.id ? 'bg-aura text-sovereign shadow-lg shadow-aura/10' : 'text-slate-500 hover:text-white hover:bg-slate-900/50'
              }`}
            >
              <item.icon size={16} className={`transition-transform duration-300 ${activeTab === item.id ? 'scale-110' : 'group-hover:scale-110'}`} />
              {item.label}
            </button>
          ))}
        </nav>

        <div className="mt-auto pt-6 border-t border-slate-900">
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-slate-500 hover:text-white hover:bg-slate-900/50 transition-all text-xs font-black uppercase tracking-widest">
            <Settings size={16} />
            Settings
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-10 overflow-y-auto">
        <header className="flex justify-between items-center mb-12">
          <div>
            <h2 className="text-3xl font-black uppercase tracking-tight mb-2">As-Salamu Alaykum, Rehan!</h2>
            <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              Current Progress: Level {currentLevel} • {juzMemorized} Juz Memorized
            </p>
          </div>
          <div className="flex items-center gap-4">
             <div className="p-3 bg-slate-900 border border-slate-800 rounded-xl flex items-center gap-3">
               <div className="w-8 h-8 rounded-lg bg-aura/20 text-aura flex items-center justify-center">
                 <Star size={16} />
               </div>
               <div className="text-right">
                 <p className="text-[10px] font-black uppercase text-slate-500">Tier Progress</p>
                 <p className="text-xs font-black uppercase text-white">Mubtadi Candidate</p>
               </div>
             </div>
             <Button className="rounded-xl px-6 py-3 font-black text-[10px] uppercase tracking-widest">Resume Learning</Button>
          </div>
        </header>

        <AnimatePresence mode="wait">
          {activeTab === 'lessons' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-8"
            >
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {lessons.map((lesson) => (
                  <Card
                    key={lesson.id}
                    className={`p-6 border-2 transition-all duration-300 relative overflow-hidden group ${
                      lesson.status === 'Locked' ? 'border-slate-900 opacity-50 grayscale' : 'border-slate-900 hover:border-aura/30 cursor-pointer'
                    }`}
                  >
                    <div className="flex justify-between items-start mb-6">
                      <div className="w-10 h-10 rounded-lg bg-slate-900 text-aura flex items-center justify-center">
                        <BookOpen size={18} />
                      </div>
                      <Badge variant={lesson.status === 'Completed' ? 'success' : 'outline'} className="text-[9px] uppercase tracking-tighter">
                        {lesson.status}
                      </Badge>
                    </div>
                    <h3 className="text-sm font-black uppercase tracking-widest mb-1">{lesson.title}</h3>
                    <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-6">Level {lesson.level} • {lesson.type}</p>
                    <Button
                      variant={lesson.status === 'Locked' ? 'ghost' : 'outline'}
                      className="w-full py-2 text-[9px] font-black uppercase tracking-widest"
                      disabled={lesson.status === 'Locked'}
                    >
                      {lesson.status === 'Completed' ? 'Review Lesson' : lesson.status === 'Locked' ? 'Unlock Lesson' : 'Resume Lesson'}
                    </Button>
                  </Card>
                ))}
              </div>
            </motion.div>
          )}

          {activeTab === 'achievements' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="grid grid-cols-2 md:grid-cols-4 gap-6"
            >
              {badges.map((badge, idx) => (
                <Card key={idx} className="p-8 text-center border-slate-900 hover:border-aura/30 transition-all group">
                  <div className="text-5xl mb-6 grayscale group-hover:grayscale-0 transition-all duration-500 scale-90 group-hover:scale-110">{badge.icon}</div>
                  <h4 className="text-[10px] font-black uppercase tracking-widest text-white mb-2">{badge.name}</h4>
                  <Badge className="bg-aura text-sovereign text-[8px] uppercase tracking-widest">Tier {badge.tier}</Badge>
                </Card>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
};

export default QEPStudentPortal;
