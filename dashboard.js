import React from 'react';
import Charts from './charts';

const Dashboard = ({ result, setResult }) => {
  if (!result) return null;

  const getRiskClass = () => {
    if (result.risk === "High") return "high";
    if (result.risk === "Medium") return "medium";
    return "low";
  };

  return (
    <div className="result-box">
      <h2>Prediction Result</h2>

      <p><strong>Probability:</strong> {result.probability}</p>

      <p className={getRiskClass()}>
        <strong>Risk:</strong> {result.risk}
      </p>

      <p><strong>Action:</strong> {result.action}</p>

      <Charts result={result} />

      <button onClick={() => setResult(null)}>
        🔄 New Prediction
      </button>

      {result.reasons && result.reasons.length > 0 && (
  <div style={{ marginTop: "15px" }}>
    <h4>Why this risk?</h4>
    <ul>
      {result.reasons.map((r, i) => (
        <li key={i}>{r}</li>
      ))}
    </ul>
  </div>
)}
    </div>

    
  );
};

export default Dashboard;