import React, { useState, useEffect } from 'react';
import Form      from './components/Form';
import Dashboard from './components/Dashboard';
import Charts    from './components/Charts';
import './App.css';

function App() {
  const [result,  setResult]  = useState(null);
  const [input,   setInput]   = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [apiOk,   setApiOk]   = useState(null);
  const [tab,     setTab]     = useState('predict');

  useEffect(() => {
    const check = async () => {
      try {
        const { healthCheck } = await import('./services/api');
        await healthCheck();
        setApiOk(true);
      } catch {
        setApiOk(false);
      }
    };
    check();
  }, []);

  const handleResult = (res, inp) => {
    setResult(res);
    setInput(inp);
    if (res && !res.error && inp) {
      setHistory(prev => [...prev, { ...res, input: inp }]);
    }
  };

  return (
    <div className="app">

      <header className="app-header">
        <div className="header-inner">
          <div className="brand">
            <span className="brand-icon">⚡</span>
            <div>
              <h1>CreditPath<span>AI</span></h1>
              <p>Loan Default Prediction & Recovery Engine</p>
            </div>
          </div>
          <div className="header-right">
            <div className={`api-status ${apiOk === true ? 'online' : apiOk === false ? 'offline' : 'checking'}`}>
              <span className="status-dot" />
              {apiOk === true ? 'API Online' : apiOk === false ? 'API Offline' : 'Checking...'}
            </div>
            <div className="stats-pill">{history.length} Predictions</div>
          </div>
        </div>

        <nav className="tabs">
          <button className={tab === 'predict'   ? 'tab active' : 'tab'} onClick={() => setTab('predict')}>Predict</button>
          <button className={tab === 'analytics' ? 'tab active' : 'tab'} onClick={() => setTab('analytics')}>Analytics</button>
          <button className={tab === 'history'   ? 'tab active' : 'tab'} onClick={() => setTab('history')}>History ({history.length})</button>
        </nav>
      </header>

      <main className="app-main">

        {tab === 'predict' && (
          <div className="predict-layout">
            <div className="left-col">
              <Form onResult={handleResult} onLoading={setLoading} />
            </div>
            <div className="right-col">
              {loading ? (
                <div className="loading-card">
                  <div className="spinner" />
                  <p>Analysing borrower profile...</p>
                </div>
              ) : result ? (
                <Dashboard result={result} inputData={input} />
              ) : (
                <div className="empty-card">
                  <span>🔍</span>
                  <p>Fill in the borrower details and click <b>Predict Risk</b> to see the result.</p>
                </div>
              )}
            </div>
          </div>
        )}

        {tab === 'analytics' && (
          history.length === 0
            ? <div className="empty-card center"><span>📊</span><p>Make at least one prediction to see analytics.</p></div>
            : <Charts history={history} />
        )}

        {tab === 'history' && (
          <div className="history-section">
            <h2>Prediction History</h2>
            {history.length === 0
              ? <div className="empty-card center"><span>📋</span><p>No predictions yet.</p></div>
              : (
                <div className="history-table-wrap">
                  <table className="history-table">
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>Age</th>
                        <th>Income</th>
                        <th>Loan Amount</th>
                        <th>Credit Score</th>
                        <th>Probability</th>
                        <th>Risk</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {history.map((h, i) => (
                        <tr key={i}>
                          <td>{i + 1}</td>
                          <td>{h.input.age}</td>
                          <td>₹{parseInt(h.input.income).toLocaleString()}</td>
                          <td>₹{parseInt(h.input.loan_amount).toLocaleString()}</td>
                          <td>{h.input.credit_score}</td>
                          <td>{Math.round(h.probability * 100)}%</td>
                          <td>
                            <span className={`risk-badge risk-${h.risk.toLowerCase()}`}>{h.risk}</span>
                          </td>
                          <td>{h.action}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )
            }
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>CreditPathAI — Infosys Springboard Internship 6.0 &nbsp;|&nbsp; Akhil Babu Gujjaralapudi &nbsp;|&nbsp; Milestone 6</p>
      </footer>
    </div>
  );
}

export default App;
