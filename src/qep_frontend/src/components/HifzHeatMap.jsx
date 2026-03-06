import React from 'react';

const HifzHeatMap = ({ completedJuz }) => {
  return (
    <div className="card" style={{ marginTop: '2rem' }}>
      <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <span style={{ fontSize: '1.5rem' }}>📖</span> Interactive Hifz Heat Map
      </h3>
      <p className="color-text-muted">Visualizing your memorization across the 114 Surahs.</p>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(12, 1fr)',
        gap: '10px',
        marginTop: '2rem'
      }}>
        {Array.from({ length: 114 }).map((_, i) => {
          const isComplete = completedJuz.includes(i + 1);
          return (
            <div
              key={i}
              title={`Surah ${i + 1}`}
              className={`juz-box ${isComplete ? 'complete' : ''}`}
              style={{
                backgroundColor: isComplete ? 'var(--color-primary-light)' : 'rgba(0,0,0,0.03)',
                borderRadius: '6px',
                aspectRatio: '1',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.6rem',
                border: '1px solid var(--color-border)',
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                cursor: 'pointer'
              }}
              onMouseEnter={(e) => e.target.style.transform = 'scale(1.2)'}
              onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
            >
              {i + 1}
            </div>
          );
        })}
      </div>

      <div style={{ marginTop: '2rem', display: 'flex', gap: '20px', fontSize: '0.8rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <div style={{ width: '12px', height: '12px', background: 'var(--color-primary-light)', borderRadius: '2px' }}></div>
          <span>Memorized</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <div style={{ width: '12px', height: '12px', background: 'rgba(0,0,0,0.03)', borderRadius: '2px', border: '1px solid var(--color-border)' }}></div>
          <span>In Progress</span>
        </div>
      </div>
    </div>
  );
};

export default HifzHeatMap;
