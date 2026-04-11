import React, { useState } from 'react';
import MushahidaStep from './components/Mushahida/MushahidaStep';
import JaizaStep from './components/Jaiza/JaizaStep';
import MuainaStep from './components/Muaina/MuainaStep';

const App = () => {
  const [step, setStep] = useState(1);
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
    <div className="min-h-screen bg-gray-100 p-8" dir={lang === 'ur' ? 'rtl' : 'ltr'}>
      <header className="max-w-4xl mx-auto mb-8 flex justify-between items-center">
        <h1 className="text-3xl font-extrabold text-gray-900">
          MJM Intelligence Engine <span className="text-sm font-normal text-gray-500">v1.0</span>
        </h1>
        <button
          onClick={() => setLang(lang === 'en' ? 'ur' : 'en')}
          className="bg-white border border-gray-300 px-3 py-1 rounded shadow-sm hover:bg-gray-50"
        >
          {lang === 'en' ? 'اردو' : 'English'}
        </button>
      </header>

      <main className="max-w-4xl mx-auto">
        <div className="mb-8 flex justify-between border-b border-gray-200 pb-4">
          <div className={`flex items-center ${step >= 1 ? 'text-green-600 font-bold' : 'text-gray-400'}`}>
            <span className="mr-2">1. Mushahida</span>
          </div>
          <div className={`flex items-center ${step >= 2 ? 'text-yellow-600 font-bold' : 'text-gray-400'}`}>
            <span className="mr-2">2. Jaiza</span>
          </div>
          <div className={`flex items-center ${step >= 3 ? 'text-red-600 font-bold' : 'text-gray-400'}`}>
            <span className="mr-2">3. Muaina</span>
          </div>
        </div>

        {step === 1 && <MushahidaStep onNext={handleNext} />}
        {step === 2 && <JaizaStep evidence={data} onNext={handleNext} onBack={handleBack} />}
        {step === 3 && <MuainaStep analysis={data} onBack={handleBack} />}
      </main>

      <footer className="max-w-4xl mx-auto mt-12 text-center text-gray-500 text-sm">
        <p>Sovereign Digital Organism Architecture | Zero-Placeholder Certified</p>
      </footer>
    </div>
  );
};

export default App;
