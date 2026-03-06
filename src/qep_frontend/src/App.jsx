import React, { useState, useEffect } from 'react';
import HifzHeatMap from './components/HifzHeatMap';

function App() {
  const [status, setStatus] = useState('Initializing Digital Sanctuary...');
  const [activeTab, setActiveTab] = useState('Dashboard');
  const [userProfile, setUserProfile] = useState({
    name: 'Abdullah',
    tazkiyah: 84,
    nurPoints: 1240,
    completedJuz: [1, 2, 3, 4, 18, 36, 67, 112, 113, 114]
  });

  useEffect(() => {
    const timer = setTimeout(() => {
      setStatus('v99.0 Conscious Business: QEP Sovereign Product Active');
    }, 1500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="dashboard-container">
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
          <NavItem label="Scholar Portal" active={activeTab === 'Scholar'} onClick={() => setActiveTab('Scholar')} />
        </nav>
        <div style={{ borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '1.5rem' }}>
          <div style={{ fontSize: '0.8rem', opacity: 0.8 }}>AI Commander Status:</div>
          <div style={{ fontSize: '0.9rem', color: 'var(--color-accent)' }}>STRATEGIC_ALIGNMENT_OK</div>
        </div>
      </aside>

      <main className="content-area">
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '3.5rem' }}>
          <div>
            <h1 style={{ margin: 0, fontSize: '2.5rem', fontWeight: 800 }}>As-salaam Alaykum, {userProfile.name}</h1>
            <p style={{ color: 'var(--color-text-muted)', fontSize: '1.1rem', marginTop: '0.5rem' }}>
              Your journey of spiritual refinement continues.
            </p>
          </div>
          <div className="status-badge" style={{ backgroundColor: '#e0f2f1', color: '#004d40', padding: '0.75rem 1.5rem', borderRadius: '30px', fontWeight: 600 }}>
            {status}
          </div>
        </header>

        <section className="stat-grid">
          <StatCard label="Current Tazkiyah" value={userProfile.tazkiyah} sub="+5.2% this week" trend="up" />
          <StatCard label="Nur Points (XP)" value={userProfile.nurPoints} sub="Top 5% of Students" />
          <StatCard label="Streak" value="12 Days" sub="Ramadan Ready" />
          <StatCard label="Dawah Ready" value="Level 2" sub="Article 249 Compliant" />
        </section>

        <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '2rem' }}>
          {activeTab === 'Dashboard' && <HifzHeatMap completedJuz={userProfile.completedJuz} />}

          {activeTab === 'Scholar' && (
            <div className="card" style={{ gridColumn: 'span 2' }}>
              <h2 style={{ color: 'var(--color-primary)' }}>Scholar Governance Portal</h2>
              <div className="alert-list">
                <ReviewItem title="New AI Tafsir Module" type="CONTENT" status="PENDING" />
                <ReviewItem title="Educator: Omar Farooq" type="IDENTITY" status="PENDING" />
                <ReviewItem title="Policy Update: Tajwid Threshold" type="POLICY" status="APPROVED" />
              </div>
              <button className="btn-primary" style={{ marginTop: '2rem' }}>Access Full Audit Ledger</button>
            </div>
          )}

          {activeTab === 'Dashboard' && (
            <div className="card" style={{ borderLeft: '6px solid var(--color-accent)' }}>
              <h3 style={{ marginTop: 0 }}>Personalized Recommendations</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div className="rec-item">
                  <strong>Next Milestone:</strong>
                  <p className="color-text-muted">Complete Surah Al-Kahf to reach Tazkiyah Level 85.</p>
                </div>
                <button className="btn-primary">Improve Makharij Analysis</button>
                <button className="btn-primary" style={{ background: 'white', color: 'var(--color-primary)', border: '2px solid var(--color-primary)' }}>
                  Review Revision Schedule
                </button>
                <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', marginTop: '1rem', fontStyle: 'italic' }}>
                  * Adapting to your {new Date().getHours() < 12 ? 'morning' : 'evening'} focus pattern.
                </div>
              </div>
            </div>
          )}
        </div>

        <footer style={{ marginTop: '4rem', opacity: 0.6, fontSize: '0.85rem', textAlign: 'center' }}>
          Sovereign Business Entity: SOV_V99 | Powered by Transcendent Workstation | No Incurred Costs Policy Active
        </footer>
      </main>
    </div>
  );
}

function ReviewItem({ title, type, status }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '1rem', borderBottom: '1px solid #eee' }}>
      <div>
        <strong>{title}</strong>
        <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>Type: {type}</div>
      </div>
      <div style={{ color: status === 'PENDING' ? '#f57c00' : '#2e7d32', fontWeight: 700 }}>{status}</div>
      <button style={{ background: 'none', border: '1px solid #ddd', cursor: 'pointer', borderRadius: '4px' }}>Review</button>
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
