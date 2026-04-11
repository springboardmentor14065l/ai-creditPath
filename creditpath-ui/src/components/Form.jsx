import React, { useState } from 'react';
import './Form.css';

const Form = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    age: '',
    income: '',
    loanamount: '',
    monthly_debt: '',
    creditscore: '',
    interestrate: '',
    monthsemployed: '',
    hascosigner: 'no',
    employmenttype: 'other',
    maritalstatus: 'single'
  });
  
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formData.age || formData.age < 18) newErrors.age = 'Valid age is required';
    if (!formData.income || formData.income < 0) newErrors.income = 'Valid income is required';
    if (!formData.loanamount || formData.loanamount <= 0) newErrors.loanamount = 'Valid loan amount is required';
    if (!formData.monthly_debt || formData.monthly_debt < 0) newErrors.monthly_debt = 'Valid monthly debt is required';
    if (!formData.creditscore || formData.creditscore < 300 || formData.creditscore > 850) newErrors.creditscore = 'Credit score must be between 300 and 850';
    if (!formData.interestrate || formData.interestrate < 0) newErrors.interestrate = 'Valid interest rate is required';
    if (!formData.monthsemployed || formData.monthsemployed < 0) newErrors.monthsemployed = 'Valid months employed is required';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      // Convert numbers appropriately where needed, but let's keep strings in state until submit for simpler rendering
      [name]: value
    }));
    // clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      // Cast types correctly for the API
      const payload = {
        age: parseInt(formData.age, 10),
        income: parseFloat(formData.income),
        loanamount: parseFloat(formData.loanamount),
        monthly_debt: parseFloat(formData.monthly_debt),
        creditscore: parseInt(formData.creditscore, 10),
        interestrate: parseFloat(formData.interestrate),
        monthsemployed: parseInt(formData.monthsemployed, 10),
        hascosigner: formData.hascosigner,
        employmenttype: formData.employmenttype,
        maritalstatus: formData.maritalstatus
      };
      onSubmit(payload);
    }
  };

  return (
    <form className="loan-form" onSubmit={handleSubmit}>
      <h2>Applicant Details</h2>
      
      <div className="form-grid">
        <div className="form-group">
          <label>Age</label>
          <input type="number" name="age" value={formData.age} onChange={handleChange} required />
          {errors.age && <span className="error">{errors.age}</span>}
        </div>
        
        <div className="form-group">
          <label>Annual Income ($)</label>
          <input type="number" name="income" value={formData.income} onChange={handleChange} required />
          {errors.income && <span className="error">{errors.income}</span>}
        </div>
        
        <div className="form-group">
          <label>Loan Amount ($)</label>
          <input type="number" name="loanamount" value={formData.loanamount} onChange={handleChange} required />
          {errors.loanamount && <span className="error">{errors.loanamount}</span>}
        </div>
        
        <div className="form-group">
          <label>Monthly Debt ($)</label>
          <input type="number" name="monthly_debt" value={formData.monthly_debt} onChange={handleChange} required />
          {errors.monthly_debt && <span className="error">{errors.monthly_debt}</span>}
        </div>
        
        <div className="form-group">
          <label>Credit Score (300-850)</label>
          <input type="number" name="creditscore" value={formData.creditscore} onChange={handleChange} required />
          {errors.creditscore && <span className="error">{errors.creditscore}</span>}
        </div>

        <div className="form-group">
          <label>Interest Rate (%)</label>
          <input type="number" step="0.01" name="interestrate" value={formData.interestrate} onChange={handleChange} required />
          {errors.interestrate && <span className="error">{errors.interestrate}</span>}
        </div>
        
        <div className="form-group">
          <label>Months Employed</label>
          <input type="number" name="monthsemployed" value={formData.monthsemployed} onChange={handleChange} required />
          {errors.monthsemployed && <span className="error">{errors.monthsemployed}</span>}
        </div>

        <div className="form-group">
          <label>Has Co-Signer?</label>
          <select name="hascosigner" value={formData.hascosigner} onChange={handleChange}>
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </div>

        <div className="form-group">
          <label>Employment Type</label>
          <select name="employmenttype" value={formData.employmenttype} onChange={handleChange}>
            <option value="unemployed">Unemployed</option>
            <option value="self-employed">Self-employed</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div className="form-group">
          <label>Marital Status</label>
          <select name="maritalstatus" value={formData.maritalstatus} onChange={handleChange}>
            <option value="single">Single</option>
            <option value="married">Married</option>
            <option value="divorced">Divorced</option>
          </select>
        </div>
      </div>
      
      <button className="submit-btn" type="submit" disabled={isLoading}>
        {isLoading ? <span className="spinner"></span> : 'Analyze Risk'}
      </button>
    </form>
  );
};

export default Form;
