import React, { useState, useEffect } from 'react';
import Form from './components/form';
import Dashboard from './components/dashboard';
import History from './components/history';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  // Load history
  useEffect(() => {
    const saved = localStorage.getItem("history");
    if (saved) setHistory(JSON.parse(saved));
  }, []);

  // Save history
  useEffect(() => {
    localStorage.setItem("history", JSON.stringify(history));
  }, [history]);

  return (
    <>
      {/* ✅ NAVBAR */}
      <div className="navbar">🏦 CreditAI  Dashboard</div>

      <div className="container">
        <div className="card">

          <h2 className="title">Loan Risk Analysis</h2>

          {!result ? (
            <Form setResult={(res) => {
              setResult(res);
              setHistory([res, ...history]);
            }} />
          ) : (
            <Dashboard result={result} setResult={setResult} />
          )}

          {/* History always visible */}
          <History history={history} setHistory={setHistory} />

        </div>
      </div>
    </>
  );
}

export default App;