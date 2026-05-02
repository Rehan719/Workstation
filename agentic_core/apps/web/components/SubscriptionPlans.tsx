import React, { useState } from "react";

const PlanCard = ({ name, priceId, onSubscribe, loading }) => (
  <div className="p-4 border rounded shadow">
    <h3>{name} Plan</h3>
    <button
      onClick={() => onSubscribe(priceId)}
      disabled={loading}
      className="mt-2 px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-400"
    >
      {loading ? "Processing..." : "Start 30-day free trial"}
    </button>
  </div>
);

export default function PricingPlans({ user }) {
  const [loading, setLoading] = useState(false);

  const handleSubscribe = async (priceId) => {
    setLoading(true);
    try {
      const res = await fetch("/api/stripe/create-checkout-session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          uid: user.uid,
          price_id: priceId,
          success_url: window.location.origin + "/dashboard",
          cancel_url: window.location.origin + "/pricing",
        }),
      });
      const data = await res.json();
      if (data.url) {
        window.location.href = data.url;
      }
    } catch (error) {
      console.error("Subscription error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex gap-4 p-8">
      <PlanCard name="Pro" priceId="price_pro" onSubscribe={handleSubscribe} loading={loading} />
      <PlanCard name="Team" priceId="price_team" onSubscribe={handleSubscribe} loading={loading} />
    </div>
  );
}
