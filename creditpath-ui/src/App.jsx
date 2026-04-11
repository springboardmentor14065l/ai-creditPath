import React, { useState, useEffect } from 'react';
import Form from './components/Form';
import Dashboard from './components/Dashboard';
import { submitLoanApplication } from './services/api';
import './App.css';

function App() {
  const [resultData, setResultData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [theme, setTheme] = useState('light');

  // Ensure body follows theme logic if needed, but app-container wraps it.
  useEffect(() => {
    document.body.className = theme === 'dark' ? 'dark-theme' : '';
  }, [theme]);

  const toggleTheme = () => {
    setTheme(t => t === 'light' ? 'dark' : 'light');
  };

  const handleFormSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await submitLoanApplication(formData);
      setResultData(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`app-container ${theme === 'dark' ? 'dark-theme' : ''}`}>
      <header className="app-header">
        <button onClick={toggleTheme} className="theme-toggle">
          {theme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode'}
        </button>
        <div className="logo-container">
          <div className="logo-icon"></div>
          <h1>CreditPath</h1>
        </div>
        <p className="subtitle">Real-time Machine Learning Risk Assessment</p>
      </header>

      <main className="main-content">
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}
        
        <div className="layout-grid">
          <div className="form-section">
            <Form onSubmit={handleFormSubmit} isLoading={isLoading} />
          </div>
          
          <div className="dashboard-section">
            <Dashboard data={resultData} theme={theme} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
