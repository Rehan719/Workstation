import React, { useState, useEffect } from 'react';

export default function PricingPlans({ user }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [recommendedPlan, setRecommendedPlan] = useState(null);

  useEffect(() => {
    fetch('/api/user/profile').then(r => r.json()).then(profile => {
      // Simple heuristic: if adaptation score > 0.8, recommend Pro
      if (profile.adaptationScore > 0.8) setRecommendedPlan('price_pro');
    });
  }, []);

  const handleSubscribe = async (priceId) => {
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
      window.location.href = url;
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const plans = [
    { name: "Pro", price: "$29/mo", priceId: "price_pro", features: ["2,000 executions/month", "10 projects"] },
    { name: "Team", price: "$99/mo", priceId: "price_team", features: ["10,000 executions/month", "Unlimited projects"] }
  ];

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold mb-6 text-center">Workstation Subscription Plans</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
        {plans.map((plan) => (
          <PlanCard
            key={plan.priceId}
            name={plan.name}
            price={plan.price}
            features={plan.features}
            recommended={recommendedPlan === plan.priceId}
            onSubscribe={() => handleSubscribe(plan.priceId)}
            loading={loading}
          />
        ))}
      </div>
      <div className="mt-8 text-center">
        <button onClick={() => window.location.href = '/pricing/all'} className="text-blue-600 hover:underline">
          See all plans (no AI)
        </button>
      </div>
    </div>
  );
}

function PlanCard({ name, price, features, recommended, onSubscribe, loading }) {
  return (
    <div className={`p-6 border rounded-lg shadow-lg relative ${recommended ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}`}>
      {recommended && (
        <span className="absolute top-0 right-0 transform translate-x-2 -translate-y-2 bg-blue-500 text-white text-xs px-2 py-1 rounded-full">
          Recommended for you
        </span>
      )}
      <h3 className="text-xl font-bold mb-2">{name} Plan</h3>
      <p className="text-3xl font-extrabold mb-4">{price}</p>
      <ul className="mb-6 space-y-2">
        {features.map(f => <li key={f} className="flex items-center">✅ {f}</li>)}
      </ul>
      <button
        onClick={onSubscribe}
        disabled={loading}
        className="w-full py-3 px-4 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? 'Processing...' : 'Start 30-day free trial'}
      </button>
    </div>
  );
}
