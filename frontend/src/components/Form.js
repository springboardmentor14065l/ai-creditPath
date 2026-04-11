import React, { useState } from 'react';
import '../styles/Form.css';

const Form = ({ onSubmit, loading }) => {
    const [formData, setFormData] = useState({
        income: '',
        loan_amount: '',
        credit_score: '',
        months_employed: '',
    });

    const [errors, setErrors] = useState({});

    /**
     * Validate form inputs
     * @returns {boolean} - true if valid, false otherwise
     */
    const validateForm = () => {
        const newErrors = {};

        if (!formData.income || formData.income <= 0) {
            newErrors.income = 'Income must be greater than 0';
        }
        if (!formData.loan_amount || formData.loan_amount <= 0) {
            newErrors.loan_amount = 'Loan amount must be greater than 0';
        }
        if (!formData.credit_score || formData.credit_score < 300 || formData.credit_score > 850) {
            newErrors.credit_score = 'Credit score must be between 300 and 850';
        }
        if (!formData.months_employed || formData.months_employed < 0) {
            newErrors.months_employed = 'Months employed must be 0 or greater';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    /**
     * Handle input change
     */
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value === '' ? '' : parseFloat(value),
        });
        // Clear error for this field when user starts typing
        if (errors[name]) {
            setErrors({
                ...errors,
                [name]: '',
            });
        }
    };

    /**
     * Handle form submission
     */
    const handleSubmit = (e) => {
        e.preventDefault();

        if (validateForm()) {
            onSubmit({
                income: parseFloat(formData.income),
                loan_amount: parseFloat(formData.loan_amount),
                credit_score: parseFloat(formData.credit_score),
                months_employed: parseFloat(formData.months_employed),
            });
        }
    };

    /**
     * Reset form
     */
    const handleReset = () => {
        setFormData({
            income: '',
            loan_amount: '',
            credit_score: '',
            months_employed: '',
        });
        setErrors({});
    };

    return (
        <div className="form-container">
            <h2>Loan Application Form</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="income">Annual Income ($)</label>
                    <input
                        type="number"
                        id="income"
                        name="income"
                        value={formData.income}
                        onChange={handleChange}
                        placeholder="Enter annual income"
                        disabled={loading}
                        required
                    />
                    {errors.income && <span className="error-message">{errors.income}</span>}
                </div>

                <div className="form-group">
                    <label htmlFor="loan_amount">Loan Amount ($)</label>
                    <input
                        type="number"
                        id="loan_amount"
                        name="loan_amount"
                        value={formData.loan_amount}
                        onChange={handleChange}
                        placeholder="Enter loan amount"
                        disabled={loading}
                        required
                    />
                    {errors.loan_amount && <span className="error-message">{errors.loan_amount}</span>}
                </div>

                <div className="form-group">
                    <label htmlFor="credit_score">Credit Score</label>
                    <input
                        type="number"
                        id="credit_score"
                        name="credit_score"
                        value={formData.credit_score}
                        onChange={handleChange}
                        placeholder="Enter credit score (300-850)"
                        disabled={loading}
                        required
                    />
                    {errors.credit_score && <span className="error-message">{errors.credit_score}</span>}
                </div>

                <div className="form-group">
                    <label htmlFor="months_employed">Months Employed</label>
                    <input
                        type="number"
                        id="months_employed"
                        name="months_employed"
                        value={formData.months_employed}
                        onChange={handleChange}
                        placeholder="Enter months employed"
                        disabled={loading}
                        required
                    />
                    {errors.months_employed && <span className="error-message">{errors.months_employed}</span>}
                </div>

                <div className="form-actions">
                    <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={loading}
                    >
                        {loading ? 'Analyzing...' : 'Get Risk Assessment'}
                    </button>
                    <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={handleReset}
                        disabled={loading}
                    >
                        Reset
                    </button>
                </div>
            </form>
        </div>
    );
};

export default Form;
