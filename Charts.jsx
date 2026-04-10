import React from 'react';
import PlotlyPlot from 'react-plotly.js';

const Plot = PlotlyPlot.default || PlotlyPlot;

const Charts = ({ probability }) => {
  // Hardcoded top features from feature_importance.csv for the visualization
  const featureData = {
    x: ['Age', 'L/I Ratio', 'Int. Rate', 'Int. Burden', 'Mos. Emp.', 'Cosigner', 'Dependents'],
    y: [0.145, 0.106, 0.069, 0.064, 0.059, 0.053, 0.051],
  };

  const riskColor = probability > 0.6 ? '#ef4444' : (probability > 0.3 ? '#f97316' : '#22c55e');

  return (
    <div className="grid grid-cols-1 gap-6">
      {/* Risk Gauge Chart */}
      <div className="bg-white p-4 rounded-xl shadow-lg border border-gray-100 h-[380px]">
        <h3 className="text-lg font-bold mb-2 text-gray-700">Risk Probability Gauge</h3>
        <Plot
          data={[
            {
              type: "indicator",
              mode: "gauge+number",
              value: probability * 100,
              number: { suffix: "%", font: { size: 40 } },
              gauge: {
                axis: { range: [null, 100], tickwidth: 1, tickcolor: "darkblue" },
                bar: { color: riskColor },
                bgcolor: "white",
                borderwidth: 2,
                bordercolor: "#e5e7eb",
                steps: [
                  { range: [0, 30], color: "#dcfce7" },
                  { range: [30, 60], color: "#ffedd5" },
                  { range: [60, 100], color: "#fee2e2" },
                ],
              },
            },
          ]}
          layout={{
            autosize: true,
            margin: { t: 50, r: 50, l: 50, b: 0 },
            height: 300,
          }}
          useResizeHandler={true}
          className="w-full h-full"
        />
      </div>

      {/* Feature Importance Chart */}
      <div className="bg-white p-4 rounded-xl shadow-lg border border-gray-100 h-[430px]">
        <h3 className="text-lg font-bold mb-2 text-gray-700">Top Risk Drivers</h3>
        <Plot
          data={[
            {
              x: featureData.x,
              y: featureData.y,
              type: 'bar',
              marker: {
                color: '#6366f1',
                opacity: 0.8,
              },
            },
          ]}
          layout={{
            autosize: true,
            margin: { t: 10, r: 10, l: 40, b: 60 },
            xaxis: { title: { text: 'Feature', font: { size: 10 } }, tickangle: -45 },
            yaxis: { title: 'Importance' },
            font: { size: 11 },
            height: 350,
          }}
          useResizeHandler={true}
          className="w-full h-full"
        />
      </div>
    </div>
  );
};

export default Charts;
