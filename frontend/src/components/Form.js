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

  return (
    <section className="panel-card borrower-panel">
      <div className="section-header">
        <div>
          <h2>Borrower Input</h2>
          <p>Review borrower details, run prediction, and push the case into the agent queue.</p>
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
          {detailCards.map((card) => (
            <article key={card.key} className={`detail-card detail-${card.key}`}>
              <div className="detail-label">{card.label}</div>
              <div className="detail-value">{cardValues[card.key]}</div>
            </article>
          ))}
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
