import React from 'react';
import Charts from './Charts';
import './Dashboard.css';

const Dashboard = ({ data, theme }) => {
  if (!data) {
    return (
      <div className="dashboard empty">
        <div className="empty-state">
          <h3>No Data Yet</h3>
          <p>Fill out the application form to generate a risk analysis.</p>
        </div>
      </div>
    );
  }

  const { probability, risk, action } = data;

  const isHighRisk = risk === "High";
  const isMediumRisk = risk === "Medium";
  const isLowRisk = risk === "Low";

  let statusClass = "status-low";
  if (isMediumRisk) statusClass = "status-medium";
  if (isHighRisk) statusClass = "status-high";

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Credit Risk Analysis Results</h2>
      </div>

      <div className="metrics-grid">
        <div className={`metric-card ${statusClass}`}>
          <span className="metric-title">Risk Level</span>
          <span className="metric-value">{risk}</span>
        </div>
        
        <div className="metric-card normal">
          <span className="metric-title">Default Probability</span>
          <span className="metric-value">{(probability * 100).toFixed(1)}%</span>
        </div>
      </div>

      <div className={`action-card ${statusClass}`}>
        <div className="action-header">
          <h3>Recommended Action</h3>
        </div>
        <p className="action-text">{action}</p>
      </div>

      <div className="chart-container">
        <Charts probability={probability} theme={theme} />
      </div>
    </div>
  );
};

export default Dashboard;
