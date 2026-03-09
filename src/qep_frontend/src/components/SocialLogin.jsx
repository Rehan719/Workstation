import React from 'react';

const SocialLogin = () => (
  <div className="space-y-4">
    <p className="text-[10px] font-black uppercase text-white/40 tracking-widest text-center">OAuth 2.0 Secure Access</p>
    <div className="grid grid-cols-2 gap-3">
      {['Google', 'Apple', 'Facebook', 'Twitter'].map(plat => (
        <button key={plat} className="py-2 bg-white/5 border border-white/10 rounded-lg text-xs font-bold hover:bg-white/10 transition-all">
          {plat}
        </button>
      ))}
    </div>
  </div>
);

export default SocialLogin;
