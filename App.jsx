import React, { useState } from 'react';
import Form from './components/Form.jsx';
import ResultCard from './components/ResultCard.jsx';
import Charts from './components/Charts.jsx';
import HistoryTable from './components/HistoryTable.jsx';
import { predictRisk } from './services/api';
import { LayoutDashboard, TrendingUp, AlertTriangle, Users, Target, CheckCircle2, AlertOctagon } from 'lucide-react';

function App() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // History state array (max 5)
  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem('predictionHistory');
    if (saved) {
      try { return JSON.parse(saved); } catch (e) { return []; }
    }
    return [];
  });

  // Save history to localStorage whenever it changes
  React.useEffect(() => {
    localStorage.setItem('predictionHistory', JSON.stringify(history));
  }, [history]);

  const handlePredict = async (data) => {
    setLoading(true);
    setError(null);
    try {
      const result = await predictRisk(data);
      setPrediction(result);
      
      // Update history
      const newEntry = {
        age: data.age,
        income: data.income,
        risk: result.risk,
        probability: result.probability
      };
      
      setHistory(prevHistory => {
        const updated = [newEntry, ...prevHistory];
        if (updated.length > 5) return updated.slice(0, 5);
        return updated;
      });
      
    } catch (err) {
      setError("Failed to fetch prediction. Is the backend running at http://127.0.0.1:8000?");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // KPI Calculations
  const totalPredictions = history.length;
  const highRiskCount = history.filter(item => item.risk === 'High Risk').length;
  const mediumRiskCount = history.filter(item => item.risk === 'Medium Risk').length;
  const lowRiskCount = history.filter(item => item.risk === 'Low Risk').length;

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      {/* Header */}
      <header className="bg-indigo-950 text-white py-5 px-8 shadow-xl flex items-center justify-between sticky top-0 z-50">
        <div className="flex items-center space-x-3">
          <div className="bg-gradient-to-br from-indigo-500 to-indigo-700 p-2 rounded-xl shadow-inner">
            <TrendingUp className="text-white w-8 h-8" />
          </div>
          <h1 className="text-2xl font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-indigo-200">
            CreditPathAI
          </h1>
        </div>
        <div className="hidden md:flex items-center space-x-6">
          <span className="text-indigo-300 text-sm font-semibold tracking-wide flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div> Live API Connection
          </span>
          <div className="h-6 w-px bg-indigo-800"></div>
          <span className="bg-indigo-800/50 border border-indigo-700 px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-widest text-indigo-200 shadow-inner">
            XGBoost v1.4
          </span>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 p-6 md:p-8 max-w-[1600px] mx-auto w-full">
        {/* KPI Section */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex items-center transition-transform hover:scale-[1.02]">
            <div className="p-3 bg-blue-50 text-blue-600 rounded-lg mr-4"><Users size={24} /></div>
            <div>
              <p className="text-sm font-bold text-gray-500 uppercase tracking-wider">Total Predictions</p>
              <h3 className="text-2xl font-black text-gray-800">{totalPredictions}</h3>
            </div>
          </div>
          <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex items-center transition-transform hover:scale-[1.02]">
            <div className="p-3 bg-red-50 text-red-600 rounded-lg mr-4"><AlertOctagon size={24} /></div>
            <div>
              <p className="text-sm font-bold text-gray-500 uppercase tracking-wider">High Risk</p>
              <h3 className="text-2xl font-black text-gray-800">{highRiskCount}</h3>
            </div>
          </div>
          <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex items-center transition-transform hover:scale-[1.02]">
            <div className="p-3 bg-amber-50 text-amber-600 rounded-lg mr-4"><Target size={24} /></div>
            <div>
              <p className="text-sm font-bold text-gray-500 uppercase tracking-wider">Medium Risk</p>
              <h3 className="text-2xl font-black text-gray-800">{mediumRiskCount}</h3>
            </div>
          </div>
          <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex items-center transition-transform hover:scale-[1.02]">
            <div className="p-3 bg-green-50 text-green-600 rounded-lg mr-4"><CheckCircle2 size={24} /></div>
            <div>
              <p className="text-sm font-bold text-gray-500 uppercase tracking-wider">Low Risk</p>
              <h3 className="text-2xl font-black text-gray-800">{lowRiskCount}</h3>
            </div>
          </div>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-500 text-red-800 p-4 rounded-r-lg shadow-md flex items-center animate-in slide-in-from-top-2" role="alert">
            <AlertTriangle className="mr-3 w-6 h-6 shrink-0" />
            <p className="font-semibold">{error}</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column: Form */}
          <div className="lg:col-span-4 h-full">
            <Form onPredict={handlePredict} loading={loading} />
          </div>

          {/* Center Column: Result */}
          <div className="lg:col-span-4 h-full">
            {!prediction && !loading && (
              <div className="h-full flex flex-col items-center justify-center p-10 bg-white rounded-2xl border-2 border-dashed border-gray-200 text-gray-400">
                <LayoutDashboard className="w-20 h-20 mb-6 opacity-20" />
                <h3 className="text-2xl font-bold text-gray-600">Awaiting Data</h3>
                <p className="text-center mt-3 text-sm max-w-[250px] leading-relaxed">
                  Fill out the borrower profile and run the analysis to generate AI-driven insights.
                </p>
              </div>
            )}

            {loading && (
              <div className="h-full flex flex-col items-center justify-center p-12 bg-white rounded-2xl border border-indigo-100 shadow-lg">
                <div className="relative">
                  <div className="w-20 h-20 border-4 border-indigo-100 border-t-indigo-600 rounded-full animate-spin"></div>
                  <div className="absolute inset-0 flex items-center justify-center">
                     <TrendingUp className="text-indigo-400 w-8 h-8 animate-pulse" />
                  </div>
                </div>
                <div className="mt-6 text-indigo-700 font-bold animate-pulse text-xl">Analyzing Risk Patterns...</div>
              </div>
            )}

            {prediction && !loading && (
              <ResultCard result={prediction} />
            )}
          </div>

          {/* Right Column: Charts */}
          <div className="lg:col-span-4 h-full">
            {!prediction && !loading ? (
              <div className="h-full flex flex-col items-center justify-center p-10 bg-white rounded-2xl border-2 border-dashed border-gray-200 text-gray-400">
                <Target className="w-20 h-20 mb-6 opacity-20" />
                <h3 className="text-2xl font-bold text-gray-600">No Analytics Yet</h3>
              </div>
            ) : (loading ? (
               <div className="h-[750px] bg-slate-100 rounded-2xl border border-gray-100 animate-pulse"></div>
            ) : (
               <Charts probability={prediction?.probability || 0} />
            ))}
          </div>
        </div>

        {/* Prediction History Table */}
        <HistoryTable history={history} />
        
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-6 text-center text-gray-500 text-sm mt-auto">
        &copy; 2026 CreditPathAI Systems. Secure AI Processing Engine. All rights reserved.
      </footer>
    </div>
  );
}

export default App;
