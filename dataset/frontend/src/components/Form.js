import React, { useState } from 'react';

const defaultForm = {
  age: '',
  income: '',
  loan_amount: '',
  credit_score: '',
  months_employed: '',
  num_credit_lines: '',
  interest_rate: '',
  loan_term: '',
  dti_ratio: '',
  education: 'Bachelor\'s',
  employment_type: 'Full-time',
  marital_status: 'Single',
  has_mortgage: 'No',
  has_dependents: 'No',
  loan_purpose: 'Personal',
  has_cosigner: 'No',
};

const fieldConfig = [
  { key: 'age',             label: 'Age',               type: 'number', placeholder: 'e.g. 35' },
  { key: 'income',          label: 'Annual Income (₹)', type: 'number', placeholder: 'e.g. 65000' },
  { key: 'loan_amount',     label: 'Loan Amount (₹)',   type: 'number', placeholder: 'e.g. 120000' },
  { key: 'credit_score',    label: 'Credit Score',      type: 'number', placeholder: '300 – 900' },
  { key: 'months_employed', label: 'Months Employed',   type: 'number', placeholder: 'e.g. 12' },
  { key: 'num_credit_lines',label: 'Credit Lines',      type: 'number', placeholder: 'e.g. 4' },
  { key: 'interest_rate',   label: 'Interest Rate (%)', type: 'number', placeholder: 'e.g. 14.5' },
  { key: 'loan_term',       label: 'Loan Term (months)',type: 'number', placeholder: 'e.g. 36' },
  { key: 'dti_ratio',       label: 'DTI Ratio',         type: 'number', placeholder: '0.01 – 0.99' },
];

const selectConfig = [
  { key: 'education',       label: 'Education',       options: ["High School", "Bachelor's", "Master's", "PhD"] },
  { key: 'employment_type', label: 'Employment Type', options: ["Full-time", "Part-time", "Self-employed", "Unemployed"] },
  { key: 'marital_status',  label: 'Marital Status',  options: ["Single", "Married", "Divorced"] },
  { key: 'loan_purpose',    label: 'Loan Purpose',    options: ["Personal", "Business", "Auto", "Home Improvement", "Education"] },
  { key: 'has_mortgage',    label: 'Has Mortgage',    options: ["Yes", "No"] },
  { key: 'has_dependents',  label: 'Has Dependents',  options: ["Yes", "No"] },
  { key: 'has_cosigner',    label: 'Has Co-Signer',   options: ["Yes", "No"] },
];

function Form({ onResult, onLoading }) {
  const [formData, setFormData] = useState(defaultForm);
  const [errors, setErrors]     = useState({});

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: '' });
  };

  const validate = () => {
    const errs = {};
    fieldConfig.forEach(({ key, label }) => {
      if (!formData[key]) errs[key] = `${label} is required`;
    });
    return errs;
  };

  const handleSubmit = async () => {
    const errs = validate();
    if (Object.keys(errs).length > 0) { setErrors(errs); return; }

    onLoading(true);
    try {
      const payload = {
        ...formData,
        age:              parseInt(formData.age),
        income:           parseFloat(formData.income),
        loan_amount:      parseFloat(formData.loan_amount),
        credit_score:     parseInt(formData.credit_score),
        months_employed:  parseInt(formData.months_employed),
        num_credit_lines: parseInt(formData.num_credit_lines),
        interest_rate:    parseFloat(formData.interest_rate),
        loan_term:        parseInt(formData.loan_term),
        dti_ratio:        parseFloat(formData.dti_ratio),
      };
      const { predict } = await import('../services/api');
      const res = await predict(payload);
      onResult(res.data, payload);
    } catch (err) {
      onResult({ error: 'API call failed. Make sure FastAPI is running.' }, null);
    } finally {
      onLoading(false);
    }
  };

  const handleReset = () => {
    setFormData(defaultForm);
    setErrors({});
    onResult(null, null);
  };

  return (
    <div className="form-card">
      <div className="form-header">
        <h2>Borrower Details</h2>
        <p>Enter the borrower's information to predict default risk</p>
      </div>

      <div className="form-grid">
        {fieldConfig.map(({ key, label, type, placeholder }) => (
          <div className="field-group" key={key}>
            <label>{label}</label>
            <input
              type={type}
              name={key}
              value={formData[key]}
              onChange={handleChange}
              placeholder={placeholder}
              className={errors[key] ? 'input-error' : ''}
            />
            {errors[key] && <span className="error-msg">{errors[key]}</span>}
          </div>
        ))}

        {selectConfig.map(({ key, label, options }) => (
          <div className="field-group" key={key}>
            <label>{label}</label>
            <select name={key} value={formData[key]} onChange={handleChange}>
              {options.map(o => <option key={o} value={o}>{o}</option>)}
            </select>
          </div>
        ))}
      </div>

      <div className="form-actions">
        <button className="btn-predict" onClick={handleSubmit}>Predict Risk</button>
        <button className="btn-reset"   onClick={handleReset}>Reset</button>
      </div>
    </div>
  );
}

export default Form;
