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

  // 1. Gauge Chart (Real-time single result)
  const gaugeData = [
    {
      type: "indicator",
      mode: "gauge+number",
      value: probability * 100,
      title: { text: "Current Risk", font: { size: 18, color: "#f8fafc" } },
      number: { suffix: "%", font: { color: "#f8fafc" } },
      gauge: {
        axis: { range: [0, 100], tickcolor: "#94a3b8" },
        bar: { color: getRiskColor(risk) },
        bgcolor: "#1e293b",
        steps: [
          { range: [0, 30], color: "rgba(16, 185, 129, 0.1)" },
          { range: [30, 60], color: "rgba(245, 158, 11, 0.1)" },
          { range: [60, 100], color: "rgba(239, 68, 68, 0.1)" }
        ]
      }
    }
  ];

  // 2. Bar Chart (Dynamic session history)
  const distributionData = [
    {
      x: ['Low', 'Medium', 'High'],
      y: [history.low, history.med, history.high],
      type: 'bar',
      marker: {
        color: ['#10b981', '#f59e0b', '#ef4444']
      }
    }
  ];

  const layoutBase = {
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: "#f8fafc", family: "Inter" },
    margin: { t: 40, r: 20, l: 40, b: 40 },
    height: 300,
    width: 350
  };

  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', justifyContent: 'center' }}>
      <Plot
        data={gaugeData}
        layout={{ ...layoutBase, title: 'Risk Probability' }}
        config={{ displayModeBar: false, responsive: true }}
      />
      
      <Plot
        data={distributionData}
        layout={{ ...layoutBase, title: 'Risk Distribution' }}
        config={{ displayModeBar: false, responsive: true }}
      />
    </div>
  );
};

export default Charts;
