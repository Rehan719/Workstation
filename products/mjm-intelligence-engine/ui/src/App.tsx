import React, { useState } from 'react';
import MushahidaStep from './components/Mushahida/MushahidaStep';
import JaizaStep from './components/Jaiza/JaizaStep';
import MuainaStep from './components/Muaina/MuainaStep';
import LivingDashboard from './components/shared/LivingDashboard';
import DomainSelector from './components/shared/DomainSelector';

const App = () => {
  const [step, setStep] = useState(1);
  const [domainId, setDomainId] = useState('patient_safety');
  const [data, setData] = useState({});
  const [lang, setLang] = useState('en');

  const handleNext = (stepData) => {
    setData({ ...data, ...stepData });
    setStep(step + 1);
  };

  const handleBack = () => {
    setStep(step - 1);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex" dir={lang === 'ur' ? 'rtl' : 'ltr'}>
      {/* Sidebar with Metrics */}
      <aside className="w-80 bg-white border-r border-slate-200 p-6 hidden lg:block">
        <div className="sticky top-6 space-y-6">
          <LivingDashboard metrics={data.metrics} />

          <div className="p-4 bg-indigo-50 rounded-lg border border-indigo-100">
            <h4 className="text-xs font-bold text-indigo-800 uppercase mb-2">Active Domain</h4>
            <div className="text-sm font-semibold">{domainId.replace(/_/g, ' ').toUpperCase()}</div>
            <div className="text-xs text-indigo-400 mt-1 italic">v1.0.0 Stable</div>
          </div>
        </div>
      </aside>

      <div className="flex-1 p-8 overflow-y-auto">
        <header className="max-w-4xl mx-auto mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
              MJM Intelligence Engine <span className="text-indigo-600">v1.0</span>
            </h1>
            <p className="text-slate-500 text-sm mt-1">Sovereign Digital Organism Architecture</p>
          </div>
          <button
            onClick={() => setLang(lang === 'en' ? 'ur' : 'en')}
            className="bg-white border border-slate-200 px-4 py-2 rounded-lg shadow-sm hover:bg-slate-50 transition-colors font-semibold text-slate-700"
          >
            {lang === 'en' ? 'اردو' : 'English'}
          </button>
        </header>

        <main className="max-w-4xl mx-auto">
          {step === 1 && (
            <>
              <DomainSelector selectedDomain={domainId} onSelect={setDomainId} />
              <MushahidaStep onNext={handleNext} />
            </>
          )}

          {step > 1 && (
            <div className="mb-8 flex justify-between bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <div className={`flex items-center space-x-2 ${step >= 1 ? 'text-green-600 font-bold' : 'text-slate-400'}`}>
                <span className="w-6 h-6 rounded-full border-2 border-current flex items-center justify-center text-xs">1</span>
                <span>Mushahida</span>
              </div>
              <div className={`flex items-center space-x-2 ${step >= 2 ? 'text-yellow-600 font-bold' : 'text-slate-400'}`}>
                <span className="w-6 h-6 rounded-full border-2 border-current flex items-center justify-center text-xs">2</span>
                <span>Jaiza</span>
              </div>
              <div className={`flex items-center space-x-2 ${step >= 3 ? 'text-red-600 font-bold' : 'text-slate-400'}`}>
                <span className="w-6 h-6 rounded-full border-2 border-current flex items-center justify-center text-xs">3</span>
                <span>Muaina</span>
              </div>
            </div>
          )}

          {step === 2 && <JaizaStep evidence={data} onNext={handleNext} onBack={handleBack} />}
          {step === 3 && <MuainaStep analysis={data} onBack={handleBack} />}
        </main>

        <footer className="max-w-4xl mx-auto mt-12 pt-8 border-t border-slate-200 text-center text-slate-400 text-xs">
          <p>© 2026 Rehan719/Workstation | Zero-Placeholder Certified | Biomimetic Adaptation Enabled</p>
        </footer>
      </div>
    </div>
  );
};

export default App;
