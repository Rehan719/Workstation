import React from 'react';

const LanguageSwitcher = ({ currentLang, setLang }) => {
  const languages = [
    { code: 'en', name: 'English', rtl: false },
    { code: 'ar', name: 'العربية', rtl: true },
    { code: 'ur', name: 'اردو', rtl: true },
    { code: 'bn', name: 'বাংলা', rtl: false }
  ];

  return (
    <div className="flex gap-2 p-1 bg-white/10 rounded-xl backdrop-blur-md border border-white/10">
      {languages.map(lang => (
        <button
          key={lang.code}
          onClick={() => setLang(lang)}
          className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
            currentLang.code === lang.code
              ? 'bg-amber-500 text-slate-900 shadow-md'
              : 'text-white/60 hover:text-white hover:bg-white/5'
          }`}
        >
          {lang.name}
        </button>
      ))}
    </div>
  );
};

export default LanguageSwitcher;
