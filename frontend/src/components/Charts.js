import React from 'react';
import Plot from 'react-plotly.js';
import '../styles/Charts.css';

const Charts = ({ result }) => {
    if (!result) {
        return (
            <div className="charts-container">
                <div className="no-chart">
                    <p>Charts will appear here after analysis</p>
                </div>
            </div>
        );
    }

    const { probability, risk } = result;

    // Prepare risk distribution data
    // Simulate realistic distribution based on the predicted risk
    let riskDistribution = {
        low: 30,
        medium: 40,
        high: 30,
    };

    // Adjust distribution based on current prediction
    if (risk.toLowerCase() === 'low') {
        riskDistribution = {
            low: 60,
            medium: 25,
            high: 15,
        };
    } else if (risk.toLowerCase() === 'medium') {
        riskDistribution = {
            low: 25,
            medium: 60,
            high: 15,
        };
    } else if (risk.toLowerCase() === 'high') {
        riskDistribution = {
            low: 15,
            medium: 25,
            high: 60,
        };
    }

    // Risk distribution bar chart
    const riskDistributionData = [
        {
            x: ['Low Risk', 'Medium Risk', 'High Risk'],
            y: [riskDistribution.low, riskDistribution.medium, riskDistribution.high],
            type: 'bar',
            marker: {
                color: ['#10b981', '#f59e0b', '#ef4444'],
            },
        },
    ];

    const riskDistributionLayout = {
        title: 'Risk Distribution in Portfolio',
        xaxis: { title: 'Risk Category' },
        yaxis: { title: 'Percentage (%)' },
        margin: { l: 50, r: 50, t: 50, b: 50 },
        paper_bgcolor: '#f9fafb',
        plot_bgcolor: '#f3f4f6',
        font: { family: 'Arial, sans-serif', size: 12 },
    };

    // Probability gauge chart
    const probabilityData = [
        {
            type: 'bar',
            x: ['Default Probability', 'No Default Probability'],
            y: [probability * 100, (1 - probability) * 100],
            marker: {
                color: ['#ef4444', '#10b981'],
            },
        },
    ];

    const probabilityLayout = {
        title: 'Default Probability Breakdown',
        xaxis: { title: 'Outcome' },
        yaxis: { title: 'Probability (%)' },
        barmode: 'stack',
        margin: { l: 50, r: 50, t: 50, b: 50 },
        paper_bgcolor: '#f9fafb',
        plot_bgcolor: '#f3f4f6',
        font: { family: 'Arial, sans-serif', size: 12 },
    };

    return (
        <div className="charts-container">
            <h2>Analytics & Insights</h2>
            
            <div className="charts-grid">
                <div className="chart-card">
                    <Plot
                        data={riskDistributionData}
                        layout={riskDistributionLayout}
                        config={{ responsive: true, displayModeBar: false }}
                        style={{ width: '100%', height: '100%' }}
                    />
                </div>

                <div className="chart-card">
                    <Plot
                        data={probabilityData}
                        layout={probabilityLayout}
                        config={{ responsive: true, displayModeBar: false }}
                        style={{ width: '100%', height: '100%' }}
                    />
                </div>
            </div>

            {/* Statistics Summary */}
            <div className="statistics-summary">
                <div className="stat-item">
                    <span className="stat-label">Portfolio Risk Distribution</span>
                    <span className="stat-value">
                        <span style={{ color: '#10b981' }}>📈 {riskDistribution.low}% Low</span>
                        <span style={{ color: '#f59e0b' }}>📊 {riskDistribution.medium}% Medium</span>
                        <span style={{ color: '#ef4444' }}>📉 {riskDistribution.high}% High</span>
                    </span>
                </div>

                <div className="stat-item">
                    <span className="stat-label">Current Application Risk</span>
                    <span className="stat-value">
                        {risk === 'Low' && '✅ Low Risk'}
                        {risk === 'Medium' && '⚠️ Medium Risk'}
                        {risk === 'High' && '❌ High Risk'}
                    </span>
                </div>

                <div className="stat-item">
                    <span className="stat-label">Default Probability</span>
                    <span className="stat-value">{(probability * 100).toFixed(2)}%</span>
                </div>
            </div>
        </div>
    );
};

export default Charts;
