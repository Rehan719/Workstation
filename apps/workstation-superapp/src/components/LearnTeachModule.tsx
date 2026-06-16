import React from 'react';
import { Card, Button, notImplemented} from '@workstation/ui';
import { GraduationCap, Users, Shield, BookOpen, User } from 'lucide-react';

export const LearnTeachModule: React.FC = () => {
  return (
    <div className="space-y-10">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
        <Card className="p-10 border-aura/20 bg-aura/5">
          <div className="flex items-center gap-6 mb-8">
            <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign">
              <User size={32} />
            </div>
            <div>
              <h3 className="text-2xl font-black text-white uppercase">Learner Dashboard</h3>
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Personalized Learning Path</p>
            </div>
          </div>
          <div className="space-y-4">
             <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 flex justify-between items-center">
                <span className="text-sm font-bold text-white">Surah Al-Baqarah (1-5)</span>
                <Button onClick={() => notImplemented('Resume')} variant="outline" className="text-[10px]">Resume</Button>
             </div>
             <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 flex justify-between items-center">
                <span className="text-sm font-bold text-white">Introduction to Tajwid Rules</span>
                <Button onClick={() => notImplemented('Start')} variant="outline" className="text-[10px]">Start</Button>
             </div>
          </div>
        </Card>

        <Card className="p-10 border-highlight/20 bg-highlight/5">
          <div className="flex items-center gap-6 mb-8">
            <div className="w-16 h-16 rounded-2xl bg-highlight flex items-center justify-center text-sovereign">
              <GraduationCap size={32} />
            </div>
            <div>
              <h3 className="text-2xl font-black text-white uppercase">Educator Portal</h3>
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Class Management & Analytics</p>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-6">
             <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
                <p className="text-[10px] font-black text-slate-500 uppercase mb-2">Total Students</p>
                <p className="text-2xl font-black text-white">42</p>
             </div>
             <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
                <p className="text-[10px] font-black text-slate-500 uppercase mb-2">Avg. Mastery</p>
                <p className="text-2xl font-black text-white">88%</p>
             </div>
          </div>
          <Button onClick={() => notImplemented('Generate Class Report')} className="w-full mt-6 bg-highlight text-sovereign uppercase font-black text-xs py-4">Generate Class Report</Button>
        </Card>
      </div>

      <Card className="p-10">
        <h4 className="text-xl font-black text-white uppercase tracking-tight mb-8 flex items-center gap-4">
           <Shield size={24} className="text-aura" />
           Scholar Governance Board
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
           {['Sheikh Al-Ghauri', 'Dr. Fatima Zahra', 'Ustadh Ibrahim'].map((scholar) => (
             <div key={scholar} className="p-6 rounded-2xl bg-slate-950 border border-slate-900 flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center">
                   <Users size={20} className="text-slate-500" />
                </div>
                <div>
                   <p className="text-sm font-black text-white">{scholar}</p>
                   <p className="text-[8px] font-bold text-slate-600 uppercase tracking-widest">Verified Scholar</p>
                </div>
             </div>
           ))}
        </div>
      </Card>
    </div>
  );
};
