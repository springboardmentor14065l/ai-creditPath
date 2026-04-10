import React from 'react';
import { ShieldCheck, ShieldAlert, AlertCircle, Info } from 'lucide-react';

const ResultCard = ({ result }) => {
  if (!result) return null;

  const { probability, risk, action } = result;

  const getRiskStyles = () => {
    switch (risk) {
      case 'Low Risk':
        return {
          bg: 'bg-green-50 border-green-300',
          text: 'text-green-700',
          accent: 'bg-green-600',
          icon: <ShieldCheck className="text-green-600 w-16 h-16" />,
          insight: 'Borrower profile suggests strong financial stability and high repayment likelihood.'
        };
      case 'Medium Risk':
        return {
          bg: 'bg-amber-50 border-amber-300',
          text: 'text-amber-700',
          accent: 'bg-amber-500',
          icon: <AlertCircle className="text-amber-600 w-16 h-16" />,
          insight: 'Borrower shows potential risk factors. Close monitoring recommended.'
        };
      case 'High Risk':
        return {
          bg: 'bg-red-50 border-red-300',
          text: 'text-red-700',
          accent: 'bg-red-600',
          icon: <ShieldAlert className="text-red-600 w-16 h-16" />,
          insight: 'High default probability detected based on historical data patterns. Urgent action required.'
        };
      default:
        return {
          bg: 'bg-gray-50 border-gray-200',
          text: 'text-gray-700',
          accent: 'bg-gray-600',
          icon: null,
          insight: ''
        };
    }
  };

  const styles = getRiskStyles();

  return (
    <div className={`p-8 rounded-2xl shadow-xl border-2 transition-all transform hover:-translate-y-1 duration-300 ease-out animate-in fade-in zoom-in-95 h-full flex flex-col justify-between ${styles.bg}`}>
      <div className="flex flex-col items-center text-center">
        <div className="mb-4 bg-white p-4 rounded-full shadow-lg border border-gray-100 animate-bounce-short">
          {styles.icon}
        </div>
        
        <h2 className="text-xl font-bold text-gray-500 uppercase tracking-widest mb-2">Prediction Status</h2>
        <div className={`text-5xl font-black mb-8 drop-shadow-sm ${styles.text}`}>
          {risk}
        </div>

        <div className="w-full h-px bg-black/10 mb-8 rounded-full"></div>

        <div className="grid grid-cols-1 gap-6 w-full text-left">
          <div className="bg-white/60 p-5 rounded-xl shadow-sm border border-black/5">
            <span className="text-xs uppercase tracking-wider text-gray-500 font-bold block mb-2">Default Probability</span>
            <span className="text-4xl font-mono font-black text-gray-800">
              {(probability * 100).toFixed(1)}<span className="text-2xl text-gray-400">%</span>
            </span>
          </div>
          
          <div className="bg-white/60 p-5 rounded-xl shadow-sm border border-black/5">
            <span className="text-xs uppercase tracking-wider text-gray-500 font-bold block mb-2">Recommended Action</span>
            <p className="text-lg font-bold text-gray-800 flex items-center">
              <span className={`w-4 h-4 rounded-full mr-3 shadow-inner ${styles.accent}`}></span>
              {action}
            </p>
          </div>
        </div>
      </div>
      
      <div className="mt-6 flex items-start p-4 bg-white/40 rounded-lg text-sm text-gray-700 font-medium">
        <Info className="w-5 h-5 mr-3 text-gray-500 flex-shrink-0 mt-0.5" />
        <p>{styles.insight}</p>
      </div>
    </div>
  );
};

export default ResultCard;
