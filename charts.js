import React from 'react';
import Plot from 'react-plotly.js';

const Charts = ({ result }) => {
  if (!result) return null;

  const probability = result.probability * 100;

  return (
    <div className="chart-box">

      {/* GAUGE CHART */}
      <Plot
        data={[
          {
            type: "indicator",
            mode: "gauge+number",
            value: probability,
            title: { text: "Risk Score (%)" },
            gauge: {
              axis: { range: [0, 100] },
              steps: [
                { range: [0, 40], color: "#22c55e" },   // green
                { range: [40, 70], color: "#f59e0b" }, // yellow
                { range: [70, 100], color: "#ef4444" } // red
              ],
              bar: { color: "#2563eb" }
            }
          }
        ]}
        layout={{ width: 350, height: 250 }}
      />

      {/* BAR CHART */}
      <Plot
        data={[
          {
            x: ["Low", "Medium", "High"],
            y: [
              probability < 40 ? probability : 10,
              probability >= 40 && probability < 70 ? probability : 10,
              probability >= 70 ? probability : 10
            ],
            type: "bar"
          }
        ]}
        layout={{
          title: "Risk Category Distribution",
          width: 400,
          height: 250
        }}
      />

    </div>
  );
};

export default Charts;