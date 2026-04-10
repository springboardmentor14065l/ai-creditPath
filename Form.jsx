import React, { useState } from 'react';

const Form = ({ onPredict, loading }) => {
  const [formData, setFormData] = useState({
    age: 35,
    income: 50000,
    loan_amount: 10000,
    credit_score: 700,
    months_employed: 24,
    num_credit_lines: 2,
    interest_rate: 10.5,
    loan_term: 36,
    dti_ratio: 0.3,
    education: 1,
    employment_type: 0,
    marital_status: 1,
    has_mortgage: 0,
    has_dependents: 0,
    loan_purpose: 4,
    has_cosigner: 0,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name.includes('has_') || ['education', 'employment_type', 'marital_status', 'loan_purpose', 'age', 'credit_score', 'months_employed', 'num_credit_lines', 'loan_term'].includes(name) 
        ? parseInt(value) 
        : parseFloat(value),
    });
  };



  const handleSubmit = (e) => {
    e.preventDefault();
    onPredict(formData);
  };

  const inputClass = "w-full p-2 border border-gray-300 rounded focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all shadow-sm hover:border-indigo-400";
  const labelClass = "block text-sm font-semibold text-gray-700 mb-1";

  return (
    <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100 flex flex-col h-full">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-gray-800">Borrower Details</h2>
      </div>

      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1">
        <div title="Age of the borrower inside years.">
          <label className={labelClass}>Age</label>
          <input type="number" name="age" value={formData.age} onChange={handleChange} className={inputClass} required />
        </div>
        <div title="Total annual salary / income.">
          <label className={labelClass}>Annual Income ($)</label>
          <input type="number" name="income" value={formData.income} onChange={handleChange} className={inputClass} required />
        </div>
        <div title="The requested loan amount in dollars.">
          <label className={labelClass}>Loan Amount ($)</label>
          <input type="number" name="loan_amount" value={formData.loan_amount} onChange={handleChange} className={inputClass} required />
        </div>
        <div title="FICO equivalent credit score. Between 300 - 850.">
          <label className={labelClass}>Credit Score (300-850)</label>
          <input type="number" name="credit_score" value={formData.credit_score} onChange={handleChange} className={inputClass} min="300" max="850" required />
        </div>
        <div title="Total months continuously employed in current job.">
          <label className={labelClass}>Months Employed</label>
          <input type="number" name="months_employed" value={formData.months_employed} onChange={handleChange} className={inputClass} required />
        </div>
        <div title="Total number of active credit cards and loans.">
          <label className={labelClass}>Credit Lines</label>
          <input type="number" name="num_credit_lines" value={formData.num_credit_lines} onChange={handleChange} className={inputClass} required />
        </div>
        <div title="The target interest rate for the loan.">
          <label className={labelClass}>Interest Rate (%)</label>
          <input type="number" step="0.01" name="interest_rate" value={formData.interest_rate} onChange={handleChange} className={inputClass} required />
        </div>
        <div title="The duration of the loan in months (e.g. 36 or 60).">
          <label className={labelClass}>Loan Term (Months)</label>
          <input type="number" name="loan_term" value={formData.loan_term} onChange={handleChange} className={inputClass} required />
        </div>
        <div title="Debt-to-Income Ratio (e.g. 0.3 for 30%).">
          <label className={labelClass}>DTI Ratio</label>
          <input type="number" step="0.01" name="dti_ratio" value={formData.dti_ratio} onChange={handleChange} className={inputClass} required />
        </div>
        <div>
          <label className={labelClass}>Education Level</label>
          <select name="education" value={formData.education} onChange={handleChange} className={inputClass}>
            <option value="0">High School</option>
            <option value="1">Bachelor's</option>
            <option value="2">Master's</option>
            <option value="3">PhD</option>
          </select>
        </div>
        <div>
          <label className={labelClass}>Employment Type</label>
          <select name="employment_type" value={formData.employment_type} onChange={handleChange} className={inputClass}>
            <option value="0">Full-time</option>
            <option value="1">Part-time</option>
            <option value="2">Self-employed</option>
            <option value="3">Unemployed</option>
          </select>
        </div>
        <div>
          <label className={labelClass}>Marital Status</label>
          <select name="marital_status" value={formData.marital_status} onChange={handleChange} className={inputClass}>
            <option value="0">Divorced</option>
            <option value="1">Married</option>
            <option value="2">Single</option>
          </select>
        </div>
        <div>
          <label className={labelClass}>Has Mortgage?</label>
          <select name="has_mortgage" value={formData.has_mortgage} onChange={handleChange} className={inputClass}>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>
        <div>
          <label className={labelClass}>Has Dependents?</label>
          <select name="has_dependents" value={formData.has_dependents} onChange={handleChange} className={inputClass}>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>
        <div>
          <label className={labelClass}>Loan Purpose</label>
          <select name="loan_purpose" value={formData.loan_purpose} onChange={handleChange} className={inputClass}>
            <option value="0">Auto</option>
            <option value="1">Business</option>
            <option value="2">Education</option>
            <option value="3">Home</option>
            <option value="4">Other</option>
          </select>
        </div>
        <div>
          <label className={labelClass}>Has Cosigner?</label>
          <select name="has_cosigner" value={formData.has_cosigner} onChange={handleChange} className={inputClass}>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>
        <div className="md:col-span-2 mt-4 content-end">
          <button 
            type="submit" 
            disabled={loading}
            className={`w-full py-4 rounded-xl font-bold text-lg text-white transition-all shadow-lg flex items-center justify-center ${loading ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 hover:shadow-indigo-500/30 active:transform active:scale-[0.98]'}`}
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Predicting Risk...
              </>
            ) : 'Run Risk Analysis'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default Form;
