import React from 'react';

const riskConfig = {
  Low: {
    color:    '#27AE60',
    bg:       '#EAFAF1',
    border:   '#27AE60',
    icon:     '✅',
    label:    'LOW RISK',
    message:  'This borrower shows a low probability of default. A simple reminder is sufficient.',
  },
  Medium: {
    color:    '#E67E22',
    bg:       '#FEF9E7',
    border:   '#F39C12',
    icon:     '⚠️',
    label:    'MEDIUM RISK',
    message:  'This borrower carries moderate risk. Direct contact is recommended to prevent default.',
  },
  High: {
    color:    '#C0392B',
    bg:       '#FDEDEC',
    border:   '#E74C3C',
    icon:     '🚨',
    label:    'HIGH RISK',
    message:  'This borrower is at high risk of default. Immediate recovery action must be initiated.',
  },
};

function Dashboard({ result, inputData }) {
  if (!result) return null;

  if (result.error) {
    return (
      <div className="result-card error-card">
        <p>⛔ {result.error}</p>
      </div>
    );
  }

  const cfg         = riskConfig[result.risk] || riskConfig.Medium;
  const probPercent = Math.round(result.probability * 100);

  return (
    <div className="result-card" style={{ borderLeft: `6px solid ${cfg.border}`, background: cfg.bg }}>

      <div className="result-header">
        <span className="result-icon">{cfg.icon}</span>
        <div>
          <h2 style={{ color: cfg.color }}>{cfg.label}</h2>
          <p className="result-sub">{cfg.message}</p>
        </div>
      </div>

      <div className="result-metrics">
        <div className="metric-box">
          <span className="metric-label">Default Probability</span>
          <span className="metric-value" style={{ color: cfg.color }}>{probPercent}%</span>
          <div className="prob-bar-bg">
            <div className="prob-bar-fill" style={{ width: `${probPercent}%`, background: cfg.color }} />
          </div>
        </div>

        <div className="metric-box">
          <span className="metric-label">Risk Level</span>
          <span className="metric-badge" style={{ background: cfg.color }}>{result.risk}</span>
        </div>

        <div className="metric-box action-box">
          <span className="metric-label">Recommended Action</span>
          <span className="action-text" style={{ color: cfg.color }}>{result.action}</span>
        </div>
      </div>

      {inputData && (
        <div className="input-summary">
          <h4>Input Summary</h4>
          <div className="summary-grid">
            <span><b>Age:</b> {inputData.age}</span>
            <span><b>Income:</b> ₹{parseInt(inputData.income).toLocaleString()}</span>
            <span><b>Loan Amount:</b> ₹{parseInt(inputData.loan_amount).toLocaleString()}</span>
            <span><b>Credit Score:</b> {inputData.credit_score}</span>
            <span><b>DTI Ratio:</b> {inputData.dti_ratio}</span>
            <span><b>Employment:</b> {inputData.employment_type}</span>
            <span><b>Loan Purpose:</b> {inputData.loan_purpose}</span>
            <span><b>Interest Rate:</b> {inputData.interest_rate}%</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
