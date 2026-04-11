import React, { useState } from 'react';
import { predict } from '../services/api';
import Form from './Form';
import Charts from './Charts';

const Dashboard = () => {
  const [formData, setFormData] = useState({
    age: 30, income: 50000, loan_amount: 20000, credit_score: 650,
    months_employed: 24, num_credit_lines: 5, interest_rate: 12.5,
    loan_term: 36, dti_ratio: 0.35, education: "Bachelor's",
    employment_type: "Full-time", marital_status: "Single",
    has_mortgage: "No", has_dependents: "No", loan_purpose: "Other", has_cosigner: "No"
  });

  const [result, setResult] = useState(null);
  const [history, setHistory] = useState({ low: 0, med: 0, high: 0 });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    // UX Fix: Allow empty strings during typing to prevent persistent zeros
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    try {
      // Data Integrity: Convert numeric fields back to Numbers only right before submission
      const numericFields = ["age", "income", "loan_amount", "credit_score", "months_employed", "num_credit_lines", "interest_rate", "loan_term", "dti_ratio"];
      const submissionData = { ...formData };
      
      numericFields.forEach(field => {
        submissionData[field] = submissionData[field] === "" ? 0 : Number(submissionData[field]);
      });

      const res = await predict(submissionData);
      const data = res.data;
      setResult(data);
      setHistory(prev => ({
        ...prev,
        low: data.risk === 'Low' ? prev.low + 1 : prev.low,
        med: data.risk === 'Medium' ? prev.med + 1 : prev.med,
        high: data.risk === 'High' ? prev.high + 1 : prev.high
      }));
    } catch (e) {
      // UX Goal: Graceful Error Handling
      console.error("API Call Failed:", e);
      setError("System Unavailable: Could not reach the Risk Assessment Engine. Please try again later.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const getRiskClass = (risk) => risk ? risk.toLowerCase() : '';
  const getRiskColor = (risk) => {
    if (risk === 'Low') return '#10b981';
    if (risk === 'Medium') return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="container">
      <header className="header">
        <h1>CreditPath AI <span style={{fontSize: '1rem', color: 'var(--text-secondary)', verticalAlign: 'middle', marginLeft: '1rem'}}>v1.4.1</span></h1>
        <p style={{color: 'var(--text-secondary)', fontWeight: 500}}>Predictive Credit Risk Engine & Recovery Action Center</p>
      </header>

      <main className="dashboard-grid">
        <Form formData={formData} onChange={handleInputChange} onSubmit={handleSubmit} loading={loading} />

        <div className="card">
          {/* Display Error Message if API fails */}
          {error && (
            <div style={{
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
              border: '1px solid var(--danger)',
              color: 'var(--danger)',
              padding: '1rem',
              borderRadius: '0.5rem',
              marginBottom: '2rem',
              textAlign: 'center',
              fontWeight: 600
            }}>
              ⚠️ {error}
            </div>
          )}

          {result ? (
            <div className="action-center">
              <div className={`risk-alert-box ${getRiskClass(result.risk)}`}>
                <div className="risk-badge-large" style={{ backgroundColor: getRiskColor(result.risk), color: 'white' }}>
                  {result.risk} Risk Detected
                </div>
                <h2 className="huge-action-text">{result.action}</h2>
                <p className="probability-subtext">
                  Model confidence: <strong>{(result.probability * 100).toFixed(0)}%</strong> default probability
                </p>
              </div>
              <Charts probability={result.probability} risk={result.risk} history={history} />
            </div>
          ) : !error && (
            <div style={{color: 'var(--text-secondary)', textAlign: 'center', padding: '10rem 2rem'}}>
              <div style={{fontSize: '5rem', marginBottom: '2rem'}}>📈</div>
              <h2 style={{color: 'white', marginBottom: '1rem'}}>Awaiting Applicant Data</h2>
              <p>Enter loan details on the left to activate the risk assessment engine.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
