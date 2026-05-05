import { useState, useEffect } from 'react';

export default function PricingPlans({ user }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [recommendedPlan, setRecommendedPlan] = useState(null);
  const [showAll, setShowAll] = useState(false);
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    fetch('/api/user/metrics')
      .then(r => r.json())
      .then(data => {
        setMetrics(data);
        if (data.adaptationScore > 15 || data.continuity > 99)
          setRecommendedPlan('price_pro');
      })
      .catch(err => console.error("Metrics fetch failed", err));
  }, []);

  const handleSubscribe = async (priceId) => {
    setLoading(true);
    try {
      const res = await fetch('/api/stripe/create-checkout-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          uid: user.uid,
          price_id: priceId,
          success_url: window.location.origin + '/dashboard',
          cancel_url: window.location.origin + '/pricing',
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      const { url } = await res.json();
      window.location.href = url;
    } catch (err) { setError(err.message); }
    finally { setLoading(false); }
  };

  const plans = [
    { name: "Pro", price: "$29/mo", priceId: "price_pro", features: ["2,000 executions/month", "10 projects", "Biomimetic analytics"] },
    { name: "Team", price: "$99/mo", priceId: "price_team", features: ["10,000 executions/month", "Unlimited projects", "Consultative governance"] }
  ];
  const displayed = showAll ? plans : plans.filter(p => p.priceId === recommendedPlan || !recommendedPlan);

  return (
    <div className="pricing-container">
      {error && <p className="error">{error}</p>}
      <div className="autonomy-header">
        {!showAll && recommendedPlan && <p className="ai-insight">✨ Twin's recommendation based on your adaptation score.</p>}
        <button onClick={() => setShowAll(!showAll)} className="toggle-btn">
          {showAll ? "Show twin guidance" : "See all plans (no AI)"}
        </button>
      </div>
      <div className="plans-grid">
        {displayed.map(plan => (
          <div key={plan.priceId} className={`plan-card ${plan.priceId === recommendedPlan ? 'recommended' : ''}`}>
             <h3>{plan.name}</h3>
             <p className="price">{plan.price}</p>
             <ul className="features">
               {plan.features.map(f => <li key={f}>{f}</li>)}
             </ul>
             <button onClick={() => handleSubscribe(plan.priceId)} disabled={loading}>
               {loading ? "Processing..." : "Start 30-day free trial"}
             </button>
          </div>
        ))}
      </div>
    </div>
  );
}
