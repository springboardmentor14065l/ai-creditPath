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
      tone: "info"
    },
    {
      label: "Active Borrowers",
      value: borrowerCount,
      tone: "info"
    },
    {
      label: "Queue Length",
      value: queueLength,
      tone: "neutral"
    }
  ];

  return (
    <section className="hero-section">
      <div className="hero-heading">
        <h1>CreditPathAI</h1>
        <p>Portfolio recovery dashboard with live borrower scoring, visual triage, and agent queue management.</p>
      </div>

      <div className="hero-card-grid">
        {cards.map((card) => (
          <article key={card.label} className={`hero-stat ${card.tone}`}>
            <div className="hero-stat-label">{card.label}</div>
            <div className="hero-stat-value">{card.value}</div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default HeroScene;
