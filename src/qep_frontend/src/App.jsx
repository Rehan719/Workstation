import React, { useState, useEffect } from 'react';

function App() {
  const [status, setStatus] = useState('Initializing Sanctuary...');
  const [activeTab, setActiveTab] = useState('Dashboard');

  useEffect(() => {
    const timer = setTimeout(() => {
      setStatus('v99.0 Religious Domain: Active');
    }, 1200);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="dashboard-container">
      {/* Sidebar Navigation */}
      <aside className="sidebar" aria-label="Main Navigation">
        <h2 style={{ color: 'var(--color-accent)', marginBottom: '2rem' }}>QEP Sanctuary</h2>
        <nav>
          <NavItem label="Dashboard" active={activeTab === 'Dashboard'} onClick={() => setActiveTab('Dashboard')} />
          <NavItem label="Tajwid Coach" active={activeTab === 'Tajwid'} onClick={() => setActiveTab('Tajwid')} />
          <NavItem label="Hifz Suite" active={activeTab === 'Hifz'} onClick={() => setActiveTab('Hifz')} />
          <NavItem label="Modules" active={activeTab === 'Modules'} onClick={() => setActiveTab('Modules')} />
          <NavItem label="Community" active={activeTab === 'Community'} onClick={() => setActiveTab('Community')} />
        </nav>
      </aside>

      {/* Main Content */}
      <main className="content-area">
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
          <div>
            <h1 style={{ margin: 0, fontSize: '2.2rem' }}>As-salaam Alaykum</h1>
            <p className="color-text-muted">Welcome back to your spiritual journey.</p>
          </div>
          <div className="status-badge" aria-live="polite">
            {status}
          </div>
        </header>

        {/* Global Stats */}
        <section className="stat-grid">
          <StatCard label="Tazkiyah Score" value="84" />
          <StatCard label="Nur Points" value="1,240" />
          <StatCard label="Daily Streak" value="12 Days" />
          <StatCard label="Juz Memorized" value="4 / 30" />
        </section>

        {/* Dynamic Section */}
        <section className="card">
          <h2>{activeTab} Overview</h2>
          <p>This is your primary hub for spiritual growth and Quranic mastery.</p>
          <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
            <button className="btn-primary" aria-label="Resume Learning">Resume Last Lesson</button>
            <button className="btn-primary" style={{ backgroundColor: 'white', color: 'var(--color-primary-light)', border: '1px solid var(--color-primary-light)' }}>
              View Schedule
            </button>
          </div>
        </section>

        <footer style={{ marginTop: 'auto', textAlign: 'center', padding: '2rem', color: 'var(--color-text-muted)', fontSize: '0.85rem' }}>
          Transcendent Workstation v99.0.0 'GENOMIC' Baseline | Expert Refinement Phase
        </footer>
      </main>
    </div>
  );
}

function NavItem({ label, active, onClick }) {
  return (
    <div className={`nav-item ${active ? 'active' : ''}`} onClick={onClick} role="button" tabIndex={0}>
      {label}
    </div>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="stat-card">
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}

export default App;
