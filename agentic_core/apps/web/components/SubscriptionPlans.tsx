import { useState, useEffect } from 'react';

export default function PricingPlans({ user }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [recommendedPlan, setRecommendedPlan] = useState<string | null>(null);
  const [showAll, setShowAll] = useState(false);
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    // Fetch metrics for guided autonomy
    fetch('/api/user/metrics')
      .then(r => r.json())
      .then(data => {
        setMetrics(data);
        // AI-based recommendation logic
        if (data.adaptationScore > 15 || data.continuity > 99) {
          setRecommendedPlan('price_pro');
        }
      })
      .catch(console.error);
  }, []);

  const handleSubscribe = async (priceId: string) => {
    setLoading(true);
    setError(null);
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
      window.location.href = url; // Redirect to Stripe
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const plans = [
    { name: "Pro", price: "$29/mo", priceId: "price_pro", features: ["2,000 executions/month", "10 projects", "Priority support"] },
    { name: "Team", price: "$99/mo", priceId: "price_team", features: ["10,000 executions/month", "Unlimited projects", "Enterprise governance"] }
  ];

  const displayedPlans = showAll ? plans : (recommendedPlan ? plans.filter(p => p.priceId === recommendedPlan) : plans);

  return (
    <div className="pricing-wrapper">
      {error && <div className="error-message">{error}</div>}

      <div className="autonomy-toggle">
        {!showAll && recommendedPlan && (
          <div className="recommendation-notice">
            ✨ Twin recommendation active.
            <button onClick={() => setShowAll(true)} className="override-link">
              See all plans (Override AI)
            </button>
          </div>
        )}
      </div>

      <div className="plans-grid">
        {displayedPlans.map(plan => (
          <div key={plan.priceId} className={`plan-card ${plan.priceId === recommendedPlan ? 'recommended' : ''}`}>
             <h3>{plan.name}</h3>
             <p className="price">{plan.price}</p>
             <ul>
               {plan.features.map(f => <li key={f}>{f}</li>)}
             </ul>
             <button onClick={() => handleSubscribe(plan.priceId)} disabled={loading}>
               {loading ? "Processing..." : "Start 30-day Free Trial"}
             </button>
          </div>
        ))}
      </div>

      <p className="autonomy-disclaimer">
        Your choice always overrides AI suggestions. Your sovereignty is absolute.
      </p>
    </div>
  );
}
