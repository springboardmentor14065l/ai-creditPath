import React from 'react';
import Plot from 'react-plotly.js';

interface RiskChartProps {
  probability: number;
  risk: string;
}

const RiskChart: React.FC<RiskChartProps> = ({ probability, risk }) => {
  const getRiskColor = (riskLabel: string) => {
    switch (riskLabel) {
      case 'Low': return '#10b981';
      case 'Medium': return '#f59e0b';
      case 'High': return '#ef4444';
      default: return '#3b82f6';
    }
  };

  const data: any = [
    {
      type: "indicator",
      mode: "gauge+number",
      value: probability * 100,
      title: { text: "Default Probability", font: { size: 24, color: "#f8fafc" } },
      number: { suffix: "%", font: { color: "#f8fafc" } },
      gauge: {
        axis: { range: [0, 100], tickwidth: 1, tickcolor: "#94a3b8" },
        bar: { color: getRiskColor(risk) },
        bgcolor: "#1e293b",
        borderwidth: 2,
        bordercolor: "#334155",
        steps: [
          { range: [0, 30], color: "rgba(16, 185, 129, 0.1)" },
          { range: [30, 60], color: "rgba(245, 158, 11, 0.1)" },
          { range: [60, 100], color: "rgba(239, 68, 68, 0.1)" }
        ],
        threshold: {
          line: { color: "#f8fafc", width: 4 },
          thickness: 0.75,
          value: probability * 100
        }
      }
    }
  ];

  const layout = {
    width: 450,
    height: 350,
    margin: { t: 25, r: 25, l: 25, b: 25 },
    paper_bgcolor: "rgba(0,0,0,0)",
    font: { color: "#f8fafc", family: "Inter" }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center' }}>
      <Plot
        data={data}
        layout={layout}
        config={{ displayModeBar: false, responsive: true }}
      />
    </div>
  );
};

export default RiskChart;
