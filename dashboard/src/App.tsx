import React, { useState } from 'react';

interface PredictionResponse {
  probability: number;
  risk: string;
  action: string;
}

interface LoanInput {
  age: number;
  income: number;
  loan_amount: number;
  credit_score: number;
  months_employed: number;
  num_credit_lines: number;
  interest_rate: number;
  loan_term: number;
  dti_ratio: number;
  education: string;
  employment_type: string;
  marital_status: string;
}

const App: React.FC = () => {
  const [formData, setFormData] = useState<LoanInput>({
    age: 30,
    income: 50000,
    loan_amount: 20000,
    credit_score: 650,
    months_employed: 24,
    num_credit_lines: 5,
    interest_rate: 12.5,
    loan_term: 36,
    dti_ratio: 0.35,
    education: "Bachelor's",
    employment_type: "Full-time",
    marital_status: "Single"
  });

  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: ["education", "employment_type", "marital_status"].includes(name) ? value : Number(value)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error fetching prediction:", error);
      alert("Failed to connect to API server. Ensure it's running!");
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'Low': return 'var(--success)';
      case 'Medium': return 'var(--warning)';
      case 'High': return 'var(--danger)';
      default: return 'var(--accent)';
    }
  };

  const radius = 90;
  const circumference = 2 * Math.PI * radius;
  const offset = result ? circumference - (result.probability * circumference) : circumference;

  return (
    <div className="container">
      <header className="header">
        <h1>CreditPath AI</h1>
        <p style={{color: 'var(--text-secondary)'}}>Advanced Credit Risk Assessment & Automated Recovery Action</p>
      </header>

      <main className="dashboard-grid">
        {/* INPUT FORM */}
        <div className="card">
          <form onSubmit={handleSubmit} className="form-grid">
            <div className="form-group">
              <label>Age</label>
              <input type="number" name="age" value={formData.age} onChange={handleInputChange} />
            </div>
            <div className="form-group">
              <label>Income ($)</label>
              <input type="number" name="income" value={formData.income} onChange={handleInputChange} />
            </div>
            <div className="form-group">
              <label>Loan Amount ($)</label>
              <input type="number" name="loan_amount" value={formData.loan_amount} onChange={handleInputChange} />
            </div>
            <div className="form-group">
              <label>Credit Score</label>
              <input type="number" name="credit_score" value={formData.credit_score} onChange={handleInputChange} />
            </div>
            <div className="form-group">
              <label>Months Employed</label>
              <input type="number" name="months_employed" value={formData.months_employed} onChange={handleInputChange} />
            </div>
            <div className="form-group">
              <label>Interest Rate (%)</label>
              <input type="number" step="0.1" name="interest_rate" value={formData.interest_rate} onChange={handleInputChange} />
            </div>
            <div className="form-group">
              <label>Loan Term (Months)</label>
              <input type="number" name="loan_term" value={formData.loan_term} onChange={handleInputChange} />
            </div>
            <div className="form-group">
              <label>DTI Ratio (0-1)</label>
              <input type="number" step="0.01" name="dti_ratio" value={formData.dti_ratio} onChange={handleInputChange} />
            </div>
            <div className="form-group">
              <label>Education</label>
              <select name="education" value={formData.education} onChange={handleInputChange}>
                <option value="High School">High School</option>
                <option value="Bachelor's">Bachelor's</option>
                <option value="Master's">Master's</option>
                <option value="PhD">PhD</option>
              </select>
            </div>
            <div className="form-group">
              <label>Employment</label>
              <select name="employment_type" value={formData.employment_type} onChange={handleInputChange}>
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Self-employed">Self-employed</option>
                <option value="Unemployed">Unemployed</option>
              </select>
            </div>
            
            <button type="submit" className="btn-predict" disabled={loading}>
              {loading ? "Calculating Risk..." : "Run Risk Assessment"}
            </button>
          </form>
        </div>

        {/* RESULTS DISPLAY */}
        <div className="card risk-display">
          {result ? (
            <>
              <div className="gauge-container">
                <svg className="gauge-svg">
                  <circle className="gauge-bg" cx="100" cy="100" r={radius} />
                  <circle 
                    className="gauge-fill" 
                    cx="100" cy="100" r={radius}
                    stroke={getRiskColor(result.risk)}
                    style={{
                      strokeDasharray: circumference,
                      strokeDashoffset: offset,
                      transform: 'rotate(-90deg)',
                      transformOrigin: '50% 50%'
                    }}
                  />
                </svg>
                <div className="probability-text">
                  {(result.probability * 100).toFixed(0)}%
                </div>
              </div>

              <div className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk) }}>
                {result.risk} Risk
              </div>

              <div className="action-card" style={{ borderLeftColor: getRiskColor(result.risk) }}>
                <div className="action-label">Automated Recommendation</div>
                <div className="action-text">{result.action}</div>
                <div className="logic-text">
                  The XGBoost engine has flagged this profile based on historical default patterns.
                </div>
              </div>
            </>
          ) : (
            <div style={{color: 'var(--text-secondary)', textAlign: 'center'}}>
              <div style={{fontSize: '4rem', marginBottom: '1rem'}}>📊</div>
              <p>Enter applicant details to generate a real-time risk score and actionable decision.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default App;
