import React from 'react';
import Plot from 'react-plotly.js';

function Charts({ history }) {
  if (!history || history.length === 0) return null;

  const low    = history.filter(h => h.risk === 'Low').length;
  const medium = history.filter(h => h.risk === 'Medium').length;
  const high   = history.filter(h => h.risk === 'High').length;

  const probs  = history.map((h, i) => ({ x: `Case ${i + 1}`, y: h.probability }));

  const riskColors = {
    Low:    '#27AE60',
    Medium: '#F39C12',
    High:   '#E74C3C',
  };

  const barData = [{
    x: ['Low Risk', 'Medium Risk', 'High Risk'],
    y: [low, medium, high],
    type: 'bar',
    marker: { color: ['#27AE60', '#F39C12', '#E74C3C'], line: { color: '#fff', width: 1.5 } },
    text: [low, medium, high],
    textposition: 'outside',
  }];

  const lineData = [{
    x: probs.map(p => p.x),
    y: probs.map(p => p.y),
    type: 'scatter',
    mode: 'lines+markers',
    line:   { color: '#2980B9', width: 2.5 },
    marker: { color: probs.map(p => riskColors[history[probs.indexOf(p)]?.risk] || '#2980B9'), size: 9 },
  }];

  const pieData = [{
    labels: ['Low Risk', 'Medium Risk', 'High Risk'],
    values: [low, medium, high],
    type: 'pie',
    marker: { colors: ['#27AE60', '#F39C12', '#E74C3C'] },
    hole: 0.45,
    textinfo: 'label+percent',
  }];

  const layout = {
    paper_bgcolor: 'transparent',
    plot_bgcolor:  'transparent',
    font: { family: 'DM Sans, sans-serif', color: '#1a1a2e' },
    margin: { t: 40, b: 40, l: 40, r: 20 },
    showlegend: false,
  };

  const config = { displayModeBar: false, responsive: true };

  return (
    <div className="charts-section">
      <h2 className="charts-title">Analytics Dashboard</h2>
      <p className="charts-sub">Based on {history.length} prediction{history.length > 1 ? 's' : ''}</p>

      <div className="charts-grid">
        <div className="chart-box">
          <h3>Risk Distribution</h3>
          <Plot data={barData} layout={{ ...layout, yaxis: { title: 'Count' } }} config={config} style={{ width: '100%', height: 280 }} />
        </div>

        <div className="chart-box">
          <h3>Risk Breakdown</h3>
          <Plot data={pieData} layout={{ ...layout, showlegend: true, legend: { orientation: 'h', y: -0.2 } }} config={config} style={{ width: '100%', height: 280 }} />
        </div>

        <div className="chart-box chart-full">
          <h3>Default Probability Trend</h3>
          <Plot
            data={lineData}
            layout={{
              ...layout,
              shapes: [
                { type: 'line', x0: 0, x1: 1, xref: 'paper', y0: 0.3, y1: 0.3, line: { color: '#F39C12', dash: 'dot', width: 1.5 } },
                { type: 'line', x0: 0, x1: 1, xref: 'paper', y0: 0.6, y1: 0.6, line: { color: '#E74C3C', dash: 'dot', width: 1.5 } },
              ],
              yaxis: { title: 'Probability', range: [0, 1] },
              annotations: [
                { x: 1, xref: 'paper', y: 0.3, text: 'Medium threshold', showarrow: false, font: { color: '#F39C12', size: 11 } },
                { x: 1, xref: 'paper', y: 0.6, text: 'High threshold',   showarrow: false, font: { color: '#E74C3C', size: 11 } },
              ]
            }}
            config={config}
            style={{ width: '100%', height: 280 }}
          />
        </div>
      </div>
    </div>
  );
}

export default Charts;
