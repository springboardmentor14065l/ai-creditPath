import React from 'react';
import Plot from 'react-plotly.js';

const Charts = ({ probability, risk, history }) => {
  const getRiskColor = (riskLabel) => {
    switch (riskLabel) {
      case 'Low': return '#10b981';
      case 'Medium': return '#f59e0b';
      case 'High': return '#ef4444';
      default: return '#3b82f6';
    }
  };

  const layoutBase = {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: "#f8fafc", family: "Inter", size: 10 },
    margin: { t: 30, r: 10, l: 30, b: 30 },
    height: 250,
    autosize: true
  };

  return (
    <div className="charts-container">
      <div style={{ flex: '1 1 300px', minWidth: '250px' }}>
        <Plot
          data={[{
            type: "indicator",
            mode: "gauge+number",
            value: probability * 100,
            number: { suffix: "%", font: { size: 20 } },
            gauge: {
              axis: { range: [0, 100] },
              bar: { color: getRiskColor(risk) },
              bgcolor: "#1e293b",
              steps: [
                { range: [0, 30], color: "rgba(16, 185, 129, 0.1)" },
                { range: [30, 60], color: "rgba(245, 158, 11, 0.1)" },
                { range: [60, 100], color: "rgba(239, 68, 68, 0.1)" }
              ]
            }
          }]}
          layout={{ ...layoutBase, title: 'Risk Probability' }}
          config={{ displayModeBar: false, responsive: true }}
          style={{ width: '100%' }}
          useResizeHandler={true}
        />
      </div>
      
      <div style={{ flex: '1 1 300px', minWidth: '250px' }}>
        <Plot
          data={[{
            x: ['Low', 'Medium', 'High'],
            y: [history.low, history.med, history.high],
            type: 'bar',
            marker: { color: ['#10b981', '#f59e0b', '#ef4444'] }
          }]}
          layout={{ ...layoutBase, title: 'Risk Distribution' }}
          config={{ displayModeBar: false, responsive: true }}
          style={{ width: '100%' }}
          useResizeHandler={true}
        />
      </div>
    </div>
  );
};

export default Charts;
