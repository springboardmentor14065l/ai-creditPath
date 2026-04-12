import React, { useState } from 'react';
import { predict } from '../services/api';

const Form = ({ setResult }) => {
  const [formData, setFormData] = useState({
    age: '',
    loanamount: '',
    creditscore: '',
    monthsemployed: '',
    numcreditlines: '',
    interestrate: '',
    loanterm: '',
    dtiratio: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const validate = () => {
    for (let key in formData) {
      if (formData[key] === "") return "All fields are required";
    }
    return "";
  };

  const handleSubmit = async () => {
    const err = validate();
    if (err) {
      setError(err);
      return;
    }

    try {
      setLoading(true);
      setError("");

      const formattedData = {};
      for (let key in formData) {
        formattedData[key] = Number(formData[key]);
      }

      const res = await predict(formattedData);
      setResult(res.data);

    } catch (e) {
      setError("Backend connection failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-grid">

      {Object.keys(formData).map((field) => (
        <div key={field}>
          <label>{field}</label>
          <input name={field} onChange={handleChange} />
        </div>
      ))}

      {error && <p className="error">{error}</p>}

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Predicting..." : "Predict"}
      </button>
    </div>
  );
};

export default Form;