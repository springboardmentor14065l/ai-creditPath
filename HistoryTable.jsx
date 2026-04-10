import React from 'react';
import { User, DollarSign, Activity, Percent } from 'lucide-react';

const HistoryTable = ({ history }) => {
  if (!history || history.length === 0) return null;

  return (
    <div className="mt-8 bg-white p-6 rounded-xl shadow-lg border border-gray-100">
      <h3 className="text-xl font-bold mb-4 text-gray-800">Recent Predictions</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm whitespace-nowrap">
          <thead className="uppercase tracking-wider border-b-2 border-gray-200 bg-gray-50 text-gray-600">
            <tr>
              <th scope="col" className="px-6 py-4 font-semibold flex items-center gap-2">
                <User size={16} /> Age
              </th>
              <th scope="col" className="px-6 py-4 font-semibold">
                <div className="flex items-center gap-2"><DollarSign size={16} /> Income</div>
              </th>
              <th scope="col" className="px-6 py-4 font-semibold">
                <div className="flex items-center gap-2"><Activity size={16} /> Risk Level</div>
              </th>
              <th scope="col" className="px-6 py-4 font-semibold">
                <div className="flex items-center gap-2"><Percent size={16} /> Probability</div>
              </th>
            </tr>
          </thead>
          <tbody>
            {history.map((entry, index) => {
              const { age, income, risk, probability } = entry;
              let riskColor = "bg-gray-100 text-gray-800";
              if (risk === "High Risk") riskColor = "bg-red-100 text-red-800";
              if (risk === "Medium Risk") riskColor = "bg-orange-100 text-orange-800";
              if (risk === "Low Risk") riskColor = "bg-green-100 text-green-800";

              return (
                <tr key={index} className="border-b border-gray-200 hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4">{age} yrs</td>
                  <td className="px-6 py-4 font-mono">${income.toLocaleString()}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded text-xs font-bold ${riskColor}`}>
                      {risk}
                    </span>
                  </td>
                  <td className="px-6 py-4 font-mono font-medium">
                    {(probability * 100).toFixed(2)}%
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HistoryTable;
