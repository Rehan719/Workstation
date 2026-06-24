import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button, Badge, notImplemented} from '@workstation/ui';
import { progressWidthClass } from '../../lib/progressWidth';
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
  Settings,
  Target,
  Plus
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import HifzProgress from './progress/HifzProgress';
import TajweedMeter from './progress/TajweedMeter';

const QEPStudentPortal = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('lessons');
  const [currentLevel, setCurrentLevel] = useState(1);
  const [juzMemorized, setJuzMemorized] = useState(1);
  const [tajweedScore, setTajweedScore] = useState(85);

  const lessons = [
    { id: 1, title: 'Al-Fatihah', type: 'Recitation', status: 'Completed', level: 1 },
    { id: 2, title: 'Introduction to Tajweed', type: 'Rules', status: 'In Progress', level: 1 },
    { id: 3, title: 'Noon Sakinah Rules', type: 'Tajweed', status: 'Locked', level: 2 },
  ];

  const badges = [
    { name: 'Beginner (Mubtadi)', tier: 1, icon: '🥉' },
    { name: 'First Surah Complete', tier: 1, icon: '🌟' },
    { name: 'Ijazah Verified', tier: 3, icon: '📜' },
  ];

  const goals = [
    { title: "Complete Juz 30", progress: 80, color: "aura" },
    { title: "Master Noon Sakinah", progress: 45, color: "emerald" },
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
            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">v8.2 Sovereign Signature</p>
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
          <button type="button" onClick={() => navigate('/settings')} className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-slate-500 hover:text-white hover:bg-slate-900/50 transition-all text-xs font-black uppercase tracking-widest">
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
             <Button onClick={() => notImplemented('Resume Learning')} className="rounded-xl px-6 py-3 font-black text-[10px] uppercase tracking-widest">Resume Learning</Button>
          </div>
        </header>

        {/* Enhanced Progress Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
           <HifzProgress juzMemorized={juzMemorized} />
           <TajweedMeter score={tajweedScore} />
        </div>

        <AnimatePresence mode="wait">
          {activeTab === 'lessons' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-8"
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xl font-black uppercase tracking-tight">Active Modules</h3>
                <Badge variant="outline" className="text-[9px] uppercase tracking-tighter border-aura/30 text-aura">48 Lessons Remaining</Badge>
              </div>
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
                    <Button onClick={() => notImplemented('This action')}
                      variant={lesson.status === 'Locked' ? 'ghost' : 'outline'}
                      className="w-full py-2 text-[9px] font-black uppercase tracking-widest"
                      disabled={lesson.status === 'Locked'}
                    >
                      {lesson.status === 'Completed' ? 'Review Lesson' : lesson.status === 'Locked' ? 'Unlock Lesson' : 'Resume Lesson'}
                    </Button>
                  </Card>
                ))}
              </div>

              {/* Goal Setting Section */}
              <div className="mt-12">
                <div className="flex items-center justify-between mb-8">
                  <h3 className="text-xl font-black uppercase tracking-tight flex items-center gap-3">
                    <Target size={24} className="text-aura" />
                    Learning Goals
                  </h3>
                  <Button onClick={() => notImplemented('Add Goal')} variant="outline" size="sm" className="rounded-lg gap-2 text-[10px] uppercase font-black tracking-widest border-aura/20">
                    <Plus size={14} /> Add Goal
                  </Button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {goals.map((goal, idx) => (
                    <Card key={idx} className="p-8 border-slate-900 group hover:border-aura/20 transition-all">
                      <div className="flex justify-between items-center mb-6">
                        <p className="text-[10px] font-black uppercase tracking-widest text-slate-500">{goal.title}</p>
                        <span className={`text-xs font-black text-${goal.color}-500`}>{goal.progress}%</span>
                      </div>
                      <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div className={`h-full bg-${goal.color}-500 ${progressWidthClass(goal.progress)}`} />
                      </div>
                    </Card>
                  ))}
                </div>
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
