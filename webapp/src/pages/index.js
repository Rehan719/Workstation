import React from 'react';
import Head from 'next/head';
import ConsciousnessPanel from '../components/ConsciousnessPanel';
import QEPBrowser from '../components/QEPBrowser';
import { LayoutGrid, Book, Users, Settings, LogOut } from 'lucide-react';

export default function Dashboard() {
  return (
    <div className="min-h-screen flex bg-gray-50">
      <Head>
        <title>Jules AI | Command Center</title>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </Head>

      {/* Sidebar */}
      <aside className="w-64 bg-indigo-950 text-white p-6 hidden lg:flex flex-col">
        <div className="text-2xl font-black mb-12 tracking-tighter text-gold-400">JULES AI v118</div>

        <nav className="flex-1 space-y-4">
          <a href="#" className="flex items-center text-gold-400 font-bold bg-indigo-900 p-3 rounded-lg"><LayoutGrid className="mr-3" size={20}/> Command Center</a>
          <a href="#" className="flex items-center text-indigo-300 hover:text-white transition-colors p-3"><Book className="mr-3" size={20}/> QEP browser</a>
          <a href="#" className="flex items-center text-indigo-300 hover:text-white transition-colors p-3"><Users className="mr-3" size={20}/> Community</a>
          <a href="#" className="flex items-center text-indigo-300 hover:text-white transition-colors p-3"><Settings className="mr-3" size={20}/> Infrastructure</a>
        </nav>

        <div className="mt-auto pt-6 border-t border-indigo-900">
           <a href="#" className="flex items-center text-indigo-300 hover:text-red-400 transition-colors"><LogOut className="mr-3" size={20}/> Sign Out</a>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Bismillah, welcome back.</h1>
            <p className="text-gray-500">Your Workstation is running at peak biological fidelity.</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm font-bold text-gray-900">Repo Owner</p>
              <p className="text-xs text-green-600 font-medium uppercase">Master Directive v118</p>
            </div>
            <div className="h-10 w-10 bg-indigo-200 rounded-full flex items-center justify-center text-indigo-900 font-bold">RO</div>
          </div>
        </header>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          {/* Left/Center Column */}
          <div className="xl:col-span-2 space-y-8">
            <QEPBrowser />
          </div>

          {/* Right Column */}
          <div className="space-y-8">
            <ConsciousnessPanel />

            <div className="bg-gradient-to-br from-indigo-900 to-indigo-800 p-6 rounded-xl text-white shadow-lg">
              <h3 className="font-bold mb-2 flex items-center text-gold-400"><Shield className="mr-2" size={18}/> System Security</h3>
              <p className="text-sm text-indigo-100 mb-4">Adaptive Immune System is monitoring 14 parallel threads. No anomalies detected.</p>
              <div className="h-2 bg-indigo-950 rounded-full overflow-hidden">
                <div className="h-full bg-green-400 w-full"></div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
