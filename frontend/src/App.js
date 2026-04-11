import React, { useState } from 'react';
import Form from './components/Form';
import Dashboard from './components/Dashboard';
import Charts from './components/Charts';
import { predict } from './services/api';
import './styles/App.css';

const App = () => {
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    /**
     * Handle form submission and API call
     */
    const handleFormSubmit = async (formData) => {
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await predict(formData);
            setResult(response);
        } catch (err) {
            console.error('Error:', err);
            setError(err.message || 'An error occurred while processing your request. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    /**
     * Reset all state
     */
    const handleReset = () => {
        setResult(null);
        setError(null);
        setLoading(false);
    };

    return (
        <div className="app">
            <header className="app-header">
                <div className="header-content">
                    <h1>🏦 CreditPathAI</h1>
                    <p>AI-Powered Loan Risk Prediction System</p>
                </div>
            </header>

            <main className="app-main">
                <div className="container">
                    {/* Loading Spinner */}
                    {loading && (
                        <div className="loading-overlay">
                            <div className="spinner"></div>
                            <p>Analyzing loan application...</p>
                        </div>
                    )}

                    {/* Error Message */}
                    {error && (
                        <div className="error-banner">
                            <div className="error-content">
                                <span className="error-icon">⚠️</span>
                                <div className="error-message">
                                    <strong>Error:</strong> {error}
                                </div>
                                <button
                                    className="error-close"
                                    onClick={() => setError(null)}
                                >
                                    ✕
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Form Section */}
                    <section className="section form-section">
                        <Form onSubmit={handleFormSubmit} loading={loading} />
                    </section>

                    {/* Results Section */}
                    {result && (
                        <>
                            <section className="section dashboard-section">
                                <Dashboard result={result} />
                            </section>

                            <section className="section charts-section">
                                <Charts result={result} />
                            </section>

                            <section className="reset-section">
                                <button
                                    className="btn btn-reset"
                                    onClick={handleReset}
                                >
                                    Analyze Another Application
                                </button>
                            </section>
                        </>
                    )}
                </div>
            </main>

            <footer className="app-footer">
                <p>&copy; 2024 CreditPathAI - Intelligent Loan Risk Assessment</p>
                <p className="backend-status">
                    Backend API: <span className="status-indicator">●</span> http://127.0.0.1:8000
                </p>
            </footer>
        </div>
    );
};

export default App;
