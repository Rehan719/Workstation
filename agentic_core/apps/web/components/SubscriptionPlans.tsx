import React, { useState, useEffect } from 'react';

const PricingPlans = ({ user }) => {
  const [loading, setLoading] = useState(false);
  const [recommendedPlan, setRecommendedPlan] = useState(null);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    // Guided Autonomy: Suggest plan based on simulated user metrics
    fetch('/api/user/metrics').then(r => r.json()).then(m => {
      if (m.adaptationScore > 15 || m.continuity > 99) setRecommendedPlan('price_pro');
    }).catch(() => setRecommendedPlan('price_pro')); // Default recommendation for demo
  }, []);

  const handleSubscribe = async (priceId) => {
    setLoading(true);
    try {
      const res = await fetch('/api/stripe/create-checkout-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ uid: user.uid, price_id: priceId, success_url: '/dashboard', cancel_url: '/pricing' }),
      });
      const { url } = await res.json();
      if (url) window.location.href = url;
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const plans = [
    { id: 'price_pro', name: 'Pro', price: '$29/mo', features: ['2k Executions', '10 Projects'] },
    { id: 'price_team', name: 'Team', price: '$99/mo', features: ['10k Executions', 'Unlimited Projects'] }
  ];

  const display = showAll ? plans : plans.filter(p => p.id === recommendedPlan || !recommendedPlan);

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold mb-4">Sovereign Plan Selection</h2>
      {!showAll && <button onClick={() => setShowAll(true)} className="text-blue-500 underline mb-4">See all plans (Manual Override)</button>}
      <div className="flex gap-4">
        {display.map(plan => (
          <div key={plan.id} className={`p-4 border rounded ${plan.id === recommendedPlan ? 'border-blue-500 shadow-lg' : ''}`}>
            {plan.id === recommendedPlan && <span className="bg-blue-500 text-white px-2 py-1 rounded text-xs">Recommended</span>}
            <h3 className="font-bold">{plan.name}</h3>
            <p className="text-xl">{plan.price}</p>
            <button
              onClick={() => handleSubscribe(plan.id)}
              disabled={loading}
              className="mt-4 bg-black text-white px-4 py-2 rounded"
            >
              Start 30-day Free Trial
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PricingPlans;
