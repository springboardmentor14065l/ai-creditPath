import React from 'react';
import PlotComponent from 'react-plotly.js';

const Plot = PlotComponent.default || PlotComponent;

const Charts = ({ probability, theme }) => {
  const value = probability * 100;

  // React mapping for dynamic Plotly styling
  const isDark = theme === 'dark';
  const fontColor = isDark ? "#f8fafc" : "#1e293b";
  const tickColor = isDark ? "#94a3b8" : "#64748b";
  const barColor = isDark ? "#f8fafc" : "#0f172a";
  const bgColor = isDark ? "#1e293b" : "#f1f5f9";
  const paperColor = "transparent";

  return (
    <div style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
      <Plot
        data={[
          {
            type: "indicator",
            mode: "gauge+number",
            value: value,
            title: { text: "Default Probability (%)", font: { size: 18, color: fontColor } },
            gauge: {
              axis: { range: [0, 100], tickwidth: 1, tickcolor: tickColor, tickfont: { color: tickColor } },
              bar: { color: barColor },
              bgcolor: bgColor,
              borderwidth: 0,
              steps: [
                { range: [0, 30], color: isDark ? "rgba(34,197,94,0.4)" : "#bbf7d0" },
                { range: [30, 60], color: isDark ? "rgba(234,179,8,0.4)" : "#fef08a" },
                { range: [60, 100], color: isDark ? "rgba(239,68,68,0.4)" : "#fecaca" }
              ],
            }
          }
        ]}
        layout={{ 
          width: 400, 
          height: 300, 
          margin: { t: 50, b: 30, l: 30, r: 30 },
          paper_bgcolor: paperColor,
          font: { family: "Inter, sans-serif", color: fontColor }
        }}
        config={{ responsive: true, displayModeBar: false }}
      />
    </div>
  );
};

export default Charts;
