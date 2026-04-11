import React from 'react';

const Form = ({ formData, onChange, onSubmit, loading }) => {
  const handleFormSubmit = (e) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <div className="card">
      <h2 style={{ marginBottom: '1.5rem', fontSize: '1.25rem' }}>Applicant Details</h2>
      <form onSubmit={handleFormSubmit} className="form-grid">
        <div className="form-group">
          <label>Age</label>
          <input type="number" name="age" value={formData.age} onChange={onChange} />
        </div>
        <div className="form-group">
          <label>Income ($)</label>
          <input type="number" name="income" value={formData.income} onChange={onChange} />
        </div>
        <div className="form-group">
          <label>Loan Amount ($)</label>
          <input type="number" name="loan_amount" value={formData.loan_amount} onChange={onChange} />
        </div>
        <div className="form-group">
          <label>Credit Score</label>
          <input type="number" name="credit_score" value={formData.credit_score} onChange={onChange} />
        </div>
        <div className="form-group">
          <label>Months Employed</label>
          <input type="number" name="months_employed" value={formData.months_employed} onChange={onChange} />
        </div>
        <div className="form-group">
          <label>Interest Rate (%)</label>
          <input type="number" step="0.1" name="interest_rate" value={formData.interest_rate} onChange={onChange} />
        </div>
        <div className="form-group">
          <label>Loan Term (Months)</label>
          <input type="number" name="loan_term" value={formData.loan_term} onChange={onChange} />
        </div>
        <div className="form-group">
          <label>DTI Ratio (0-1)</label>
          <input type="number" step="0.01" name="dti_ratio" value={formData.dti_ratio} onChange={onChange} />
        </div>
        <div className="form-group">
          <label>Education</label>
          <select name="education" value={formData.education} onChange={onChange}>
            <option value="High School">High School</option>
            <option value="Bachelor's">Bachelor's</option>
            <option value="Master's">Master's</option>
            <option value="PhD">PhD</option>
          </select>
        </div>
        <div className="form-group">
          <label>Employment</label>
          <select name="employment_type" value={formData.employment_type} onChange={onChange}>
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
  );
};

export default Form;
