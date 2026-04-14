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

const detailCards = [
  { key: "probability", label: "Probability" },
  { key: "risk", label: "Risk" },
  { key: "action", label: "Action" },
  { key: "urgency", label: "Urgency" }
];

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
    risk: result ? result.risk.toUpperCase() : "--",
    action: result ? result.action : "--",
    urgency: result ? `${result.urgency_window_hours} hours` : "--"
  };

  const currentRisk = result ? result.risk.toLowerCase() : "";

  const getRiskStyle = (risk) => {
    if (!risk) return {};
    if (risk.includes("low")) {
      return { border: "1px solid #166534", backgroundColor: "#dcfce7", color: "#166534" };
    }
    if (risk.includes("medium")) {
      return { border: "1px solid #854d0e", backgroundColor: "#fef08a", color: "#854d0e" };
    }
    if (risk.includes("high")) {
      return { border: "1px solid #991b1b", backgroundColor: "#fee2e2", color: "#991b1b" };
    }
    return {};
  };

  return (
    <section className="panel-card borrower-panel">
      <div className="section-header">
        <div>
          <h2>Borrower Input</h2>
          <p>Review borrower details, run prediction, and push the case into the agent queue.</p>
          
          <div className="preset-selector" style={{ marginTop: "1rem", display: "flex", gap: "1rem", flexWrap: "wrap", alignItems: "center" }}>
            {Object.entries(presets || {}).map(([name, template]) => (
              <button
                key={name}
                type="button"
                className="btn"
                style={{ 
                  ...getRiskStyle(name.toLowerCase()),
                  padding: "0.5rem 1rem", 
                  fontSize: "0.9rem",
                  fontWeight: "bold",
                  borderRadius: "8px",
                  cursor: "pointer",
                  transition: "opacity 0.2s"
                }}
                onMouseOver={(e) => (e.target.style.opacity = 0.8)}
                onMouseOut={(e) => (e.target.style.opacity = 1)}
                onClick={() => onLoadPreset(template)}
              >
                Load {name}
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

        <div className="insight-column">
          {detailCards.map((card) => {
            const isBoxColored = ["risk", "action", "urgency"].includes(card.key) && currentRisk;
            const boxStyle = isBoxColored ? getRiskStyle(currentRisk) : {};
            
            return (
              <article 
                key={card.key} 
                className={`detail-card detail-${card.key}`}
                style={boxStyle}
              >
                <div className="detail-label">{card.label}</div>
                <div className="detail-value">{cardValues[card.key]}</div>
              </article>
            );
          })}
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
