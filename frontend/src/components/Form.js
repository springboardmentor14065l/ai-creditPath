const borrowerFields = [
  { name: "borrower_id", label: "Borrower ID", type: "text" },
  { name: "year", label: "Year", type: "number", step: 1 },
  { name: "Credit_Score", label: "Credit Score", type: "number", step: 1 },
  { name: "property_value", label: "Value", type: "number", step: 100 },
  { name: "income", label: "Income", type: "number", step: 100 },
  { name: "dtir1", label: "Debt to income", type: "number", step: 0.1 }
];

const loanFields = [
  { name: "loan_amount", label: "Loan Amount", type: "number", step: 100 },
  { name: "term", label: "Term", type: "number", step: 1 },
  { name: "rate_of_interest", label: "Rate", type: "number", step: 0.001 },
  { name: "Interest_rate_spread", label: "Spread", type: "number", step: 0.001 },
  { name: "Upfront_charges", label: "Charges", type: "number", step: 50 },
  { name: "LTV", label: "LTV", type: "number", step: 0.1 }
];

/* Maps risk level → card theme tokens */
const RISK_THEMES = {
  low: {
    bg: "linear-gradient(135deg, #ecfdf5 60%, #d1fae5)",
    border: "#34d399",
    accent: "#059669",
    badge: { bg: "#059669", color: "#fff" },
    icon: "🟢",
    glow: "rgba(52,211,153,0.18)"
  },
  medium: {
    bg: "linear-gradient(135deg, #fffbeb 60%, #fef3c7)",
    border: "#fbbf24",
    accent: "#d97706",
    badge: { bg: "#d97706", color: "#fff" },
    icon: "🟡",
    glow: "rgba(251,191,36,0.18)"
  },
  high: {
    bg: "linear-gradient(135deg, #fff1f2 60%, #ffe4e6)",
    border: "#f87171",
    accent: "#dc2626",
    badge: { bg: "#dc2626", color: "#fff" },
    icon: "🔴",
    glow: "rgba(248,113,113,0.18)"
  }
};




function Form({
  formData,
  onChange,
  onSubmit,
  onReset,
  onAddToQueue,
  onLoadPreset,
  presets,
  loading,
  result,
  formatPercent,
  driverSummary
}) {
  const cardValues = {
    probability: result ? formatPercent(result.probability) : "--",
    risk:        result ? result.risk.toUpperCase() : "--",
    action:      result ? result.action : "--",
    urgency:     result ? `${result.urgency_window_hours} hours` : "--"
  };

  const currentRisk = result ? result.risk.toLowerCase() : null;
  const theme = currentRisk ? RISK_THEMES[currentRisk] : null;

  /* Button border colour for preset load buttons */
  const presetBorderColor = (name) => {
    const n = name.toLowerCase();
    if (n.includes("low")) return { border: "1.5px solid #059669", color: "#059669", background: "#ecfdf5" };
    if (n.includes("medium")) return { border: "1.5px solid #d97706", color: "#d97706", background: "#fffbeb" };
    if (n.includes("high")) return { border: "1.5px solid #dc2626", color: "#dc2626", background: "#fff1f2" };
    return {};
  };

  return (
    <section className="panel-card borrower-panel">
      <div className="section-header">
        <div>
          <h2>Borrower Input</h2>
          <p>Review borrower details, run prediction, and push the case into the agent queue.</p>

          <div className="preset-selector">
            {Object.entries(presets || {}).map(([name, template]) => (
              <button
                key={name}
                type="button"
                className="btn preset-btn"
                style={presetBorderColor(name)}
                onClick={() => onLoadPreset(template)}
              >
                {name.includes("Low") ? "🟢" : name.includes("Medium") ? "🟡" : "🔴"} Load {name}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="borrower-layout">
        <div className="form-columns">
          <div className="form-block">
            <h3>Borrower Info</h3>
            <div className="field-grid">
              {borrowerFields.map((field) => (
                <label key={field.name} className={`field ${field.name === "borrower_id" ? "field-span-2" : ""}`}>
                  <span>{field.label}</span>
                  <input
                    name={field.name}
                    type={field.type}
                    step={field.step}
                    value={formData[field.name]}
                    onChange={onChange}
                  />
                </label>
              ))}
            </div>
          </div>

          <div className="form-block">
            <h3>Loan Details</h3>
            <div className="field-grid">
              {loanFields.map((field) => (
                <label key={field.name} className={field.name === "loan_amount" ? "field field-span-2" : "field"}>
                  <span>{field.label}</span>
                  <input
                    name={field.name}
                    type={field.type}
                    step={field.step}
                    value={formData[field.name]}
                    onChange={onChange}
                  />
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* ── Insight Cards Column ── */}
        <div className="insight-column">
          {/* Probability card — always neutral styling */}
          <article className="detail-card detail-probability result-card-prob">
            <div className="result-card-top">
              <span className="result-card-label">📊 Probability</span>
            </div>
            <div className="result-card-value">{cardValues.probability}</div>
          </article>

          {/* Risk card */}
          <article
            className="result-card"
            style={theme ? {
              background: theme.bg,
              border: `2px solid ${theme.border}`,
              boxShadow: `0 4px 18px ${theme.glow}`
            } : {}}
          >
            <div className="result-card-top">
              <span className="result-card-label">⚠ Risk Level</span>
              {theme && <span className="result-card-icon">{theme.icon}</span>}
            </div>
            <div
              className="result-card-value"
              style={theme ? { color: theme.accent } : {}}
            >
              {cardValues.risk}
            </div>
            {theme && (
              <span
                className="result-card-badge"
                style={{ background: theme.badge.bg, color: theme.badge.color }}
              >
                {currentRisk.charAt(0).toUpperCase() + currentRisk.slice(1)} Risk
              </span>
            )}
          </article>

          {/* Action card */}
          <article
            className="result-card"
            style={theme ? {
              background: theme.bg,
              border: `2px solid ${theme.border}`,
              boxShadow: `0 4px 18px ${theme.glow}`
            } : {}}
          >
            <div className="result-card-top">
              <span className="result-card-label">▶ Action</span>
            </div>
            <div
              className="result-card-value result-card-value--sm"
              style={theme ? { color: theme.accent } : {}}
            >
              {cardValues.action}
            </div>
          </article>

          {/* Urgency card */}
          <article
            className="result-card"
            style={theme ? {
              background: theme.bg,
              border: `2px solid ${theme.border}`,
              boxShadow: `0 4px 18px ${theme.glow}`
            } : {}}
          >
            <div className="result-card-top">
              <span className="result-card-label">⏱ Urgency</span>
            </div>
            <div
              className="result-card-value"
              style={theme ? { color: theme.accent } : {}}
            >
              {cardValues.urgency}
            </div>
          </article>
        </div>
      </div>

      <div className="driver-strip">
        <span className="driver-title">Top drivers</span>
        <span>{driverSummary || "Run a prediction to surface the strongest risk signals."}</span>
      </div>

      <div className="action-row">
        <button type="button" className="btn btn-primary" onClick={onSubmit} disabled={loading}>
          {loading ? "Running..." : "Run Prediction"}
        </button>
        <button type="button" className="btn btn-secondary" onClick={onAddToQueue}>
          Add to Agent Queue
        </button>
        <button type="button" className="btn btn-ghost" onClick={onReset}>
          Reset Input
        </button>
      </div>
    </section>
  );
}

export default Form;
