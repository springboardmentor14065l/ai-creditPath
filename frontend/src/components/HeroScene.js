const CARD_META = {
  "API Status": { icon: "⚡", hint: "Live backend connectivity" },
  "Latest Probability": { icon: "📊", hint: "Last scored borrower" },
  "Active Borrowers": { icon: "👤", hint: "Borrowers processed" },
  "Queue Length": { icon: "📋", hint: "Pending in agent queue" }
};

function HeroScene({ apiStatus, latestResult, borrowerCount, queueLength }) {
  const probability = latestResult ? `${(latestResult.probability * 100).toFixed(2)}%` : "--";

  const cards = [
    {
      label: "API Status",
      value: apiStatus,
      tone: apiStatus === "Online" ? "success" : apiStatus === "Offline" ? "danger" : "neutral"
    },
    {
      label: "Latest Probability",
      value: probability,
      tone: latestResult ? (latestResult.probability > 0.6 ? "danger" : latestResult.probability > 0.3 ? "warn" : "info") : "info"
    },
    {
      label: "Active Borrowers",
      value: borrowerCount,
      tone: borrowerCount > 0 ? "info" : "neutral"
    },
    {
      label: "Queue Length",
      value: queueLength,
      tone: queueLength > 5 ? "danger" : queueLength > 0 ? "warn" : "neutral"
    }
  ];

  return (
    <section className="hero-section">
      <div className="hero-heading">
        <h1>CreditPathAI</h1>
        <p>Portfolio recovery dashboard with live borrower scoring, visual triage, and agent queue management.</p>
      </div>

      <div className="hero-card-grid">
        {cards.map((card) => {
          const meta = CARD_META[card.label] || {};
          return (
            <article key={card.label} className={`hero-stat ${card.tone}`}>
              <div className="hero-stat-label">{card.label}</div>
              <div className="hero-stat-value">{card.value}</div>
              <div className="hero-stat-hint">{meta.hint}</div>
              <div className="hero-stat-icon">{meta.icon}</div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

export default HeroScene;
