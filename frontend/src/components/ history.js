import React, { useState } from 'react';

const History = ({ history, setHistory }) => {
  const [filter, setFilter] = useState("All");

  const filteredData = filter === "All"
    ? history
    : history.filter(item => item.risk === filter);

  return (
    <div className="history-box">
      <h3>📜 Prediction History</h3>

      {/* Filter */}
      <select onChange={(e) => setFilter(e.target.value)}>
        <option>All</option>
        <option>Low</option>
        <option>Medium</option>
        <option>High</option>
      </select>

      {/* Table */}
      <table>
        <thead>
          <tr>
            <th>Probability</th>
            <th>Risk</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {filteredData.map((item, index) => (
            <tr key={index}>
              <td>{(item.probability * 100).toFixed(0)}%</td>
              <td>{item.risk}</td>
              <td>{item.action}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Clear Button */}
      <button onClick={() => setHistory([])}>
        🗑 Clear History
      </button>
    </div>
  );
};

export default History;
