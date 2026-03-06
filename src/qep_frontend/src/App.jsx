import React, { useState, useEffect } from 'react';

function App() {
  const [status, setStatus] = useState('Initializing Digital Sanctuary...');
  const [activeTab, setActiveTab] = useState('Dashboard');
  const [tazkiyahHistory, setTazkiyahHistory] = useState([78, 79, 81, 84]);

  useEffect(() => {
    const timer = setTimeout(() => {
      setStatus('v99.0 Conscious Business: QEP Sovereign Product Active');
    }, 1500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="dashboard-container">
      {/* Sidebar with Geometric Sublayer */}
      <aside className="sidebar">
        <div style={{ marginBottom: '3rem' }}>
          <h2 style={{ color: 'var(--color-accent)', margin: 0 }}>QEP</h2>
          <small style={{ opacity: 0.7, letterSpacing: '1px' }}>SOVEREIGN PRODUCT</small>
        </div>
        <nav style={{ flex: 1 }}>
          <NavItem label="Spiritual Dashboard" active={activeTab === 'Dashboard'} onClick={() => setActiveTab('Dashboard')} />
          <NavItem label="Tajwid Coach" active={activeTab === 'Tajwid'} onClick={() => setActiveTab('Tajwid')} />
          <NavItem label="Hifz Progress" active={activeTab === 'Hifz'} onClick={() => setActiveTab('Hifz')} />
          <NavItem label="Learning Vault" active={activeTab === 'Modules'} onClick={() => setActiveTab('Modules')} />
          <NavItem label="Commercial Hub" active={activeTab === 'Business'} onClick={() => setActiveTab('Business')} />
        </nav>
        <div style={{ borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '1.5rem' }}>
          <div style={{ fontSize: '0.8rem', opacity: 0.8 }}>AI Commander Status:</div>
          <div style={{ fontSize: '0.9rem', color: 'var(--color-accent)' }}>STRATEGIC_ALIGNMENT_OK</div>
        </div>
      </aside>

      {/* Main Sanctuary Area */}
      <main className="content-area">
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '3.5rem' }}>
          <div>
            <h1 style={{ margin: 0, fontSize: '2.5rem', fontWeight: 800 }}>As-salaam Alaykum, Abdullah</h1>
            <p style={{ color: 'var(--color-text-muted)', fontSize: '1.1rem', marginTop: '0.5rem' }}>
              Your journey of spiritual refinement continues.
            </p>
          </div>
          <div className="status-badge" style={{ backgroundColor: '#e0f2f1', color: '#004d40', padding: '0.75rem 1.5rem', borderRadius: '30px', fontWeight: 600 }}>
            {status}
          </div>
        </header>

        {/* Cumulative Data Visualizations */}
        <section className="stat-grid">
          <StatCard label="Current Tazkiyah" value="84" sub="+5.2% this week" trend="up" />
          <StatCard label="Nur Points (XP)" value="1,240" sub="Top 5% of Students" />
          <StatCard label="Streak" value="12 Days" sub="Ramadan Ready" />
          <StatCard label="Dawah Ready" value="Level 2" sub="Article 249 Compliant" />
        </section>

        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
          {/* Interactive Hifz Map */}
          <div className="card">
            <h3 style={{ marginTop: 0 }}>Interactive Hifz Map (114 Surahs)</h3>
            <p style={{ color: 'var(--color-text-muted)', marginBottom: '1.5rem' }}>Visualizing your memorization across the Quranic landscape.</p>
            <div className="juz-map">
              {Array.from({ length: 40 }).map((_, i) => (
                <div key={i} className={`juz-box ${i < 12 ? 'complete' : ''}`}>
                  {i + 1}
                </div>
              ))}
              <div style={{ gridColumn: 'span 10', textAlign: 'center', padding: '1rem', color: 'var(--color-text-muted)', fontSize: '0.8rem' }}>
                ... and 74 more surahs in progress
              </div>
            </div>
          </div>

          {/* Adaptive Actions */}
          <div className="card" style={{ borderLeft: '6px solid var(--color-accent)' }}>
            <h3 style={{ marginTop: 0 }}>Adaptive Actions</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <button className="btn-primary">Tajwid: Improve Makharij</button>
              <button className="btn-primary" style={{ background: 'white', color: 'var(--color-primary)', border: '2px solid var(--color-primary)' }}>
                Review Surah Al-Kahf
              </button>
              <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', marginTop: '1rem', fontStyle: 'italic' }}>
                * Recommended based on your morning usage pattern.
              </div>
            </div>
          </div>
        </div>

        <footer style={{ marginTop: '4rem', opacity: 0.6, fontSize: '0.85rem', textAlign: 'center' }}>
          Sovereign Business Entity: SOV_V99 | Powered by Transcendent Workstation | No Incurred Costs Policy Active
        </footer>
      </main>
    </div>
  );
}

function NavItem({ label, active, onClick }) {
  return (
    <div className={`nav-item ${active ? 'active' : ''}`}
         onClick={onClick}
         role="button"
         tabIndex={0}
         style={{
           padding: '1.2rem',
           marginBottom: '0.5rem',
           borderRadius: '12px',
           cursor: 'pointer',
           transition: 'all 0.3s',
           fontWeight: active ? 700 : 400,
           backgroundColor: active ? 'rgba(255,255,255,0.1)' : 'transparent'
         }}>
      {label}
    </div>
  );
}

function StatCard({ label, value, sub, trend }) {
  return (
    <div className="stat-card" style={{ background: 'white', padding: '2rem', borderRadius: '16px', boxShadow: '0 10px 20px rgba(0,0,0,0.03)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div className="stat-value" style={{ fontSize: '2.2rem', fontWeight: 800, color: 'var(--color-primary)' }}>{value}</div>
        {trend === 'up' && <div style={{ color: '#2e7d32', fontWeight: 700 }}>↑</div>}
      </div>
      <div className="stat-label" style={{ fontWeight: 600, marginTop: '0.2rem' }}>{label}</div>
      <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)', marginTop: '0.4rem' }}>{sub}</div>
    </div>
  );
}

export default App;
