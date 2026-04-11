import React from 'react';
import '../styles/Dashboard.css';

const Dashboard = ({ result }) => {
    if (!result) {
        return (
            <div className="dashboard-container">
                <div className="no-result">
                    <p>Submit the loan application form to see the risk assessment</p>
                </div>
            </div>
        );
    }

    const { probability, risk, action } = result;

    // Determine color based on risk level
    const getRiskColor = () => {
        switch (risk.toLowerCase()) {
            case 'low':
                return 'risk-low';
            case 'medium':
                return 'risk-medium';
            case 'high':
                return 'risk-high';
            default:
                return 'risk-medium';
        }
    };

    const probabilityPercentage = (probability * 100).toFixed(2);

    return (
        <div className="dashboard-container">
            <h2>Risk Assessment Results</h2>
            
            <div className="results-grid">
                {/* Risk Level Card */}
                <div className={`result-card ${getRiskColor()}`}>
                    <div className="card-label">Risk Level</div>
                    <div className="card-value">{risk}</div>
                    <div className="card-description">Overall loan default risk</div>
                </div>

                {/* Probability Card */}
                <div className="result-card result-card-info">
                    <div className="card-label">Default Probability</div>
                    <div className="card-value">{probabilityPercentage}%</div>
                    <div className="probability-bar">
                        <div 
                            className={`probability-fill ${getRiskColor()}`}
                            style={{ width: `${probability * 100}%` }}
                        ></div>
                    </div>
                </div>

                {/* Action Card */}
                <div className="result-card result-card-action">
                    <div className="card-label">Recommended Action</div>
                    <div className="card-action-text">{action}</div>
                </div>
            </div>

            {/* Risk Legend */}
            <div className="risk-legend">
                <h4>Risk Levels Guide:</h4>
                <div className="legend-items">
                    <div className="legend-item">
                        <span className="legend-color risk-low"></span>
                        <span>Low Risk: Safe to approve</span>
                    </div>
                    <div className="legend-item">
                        <span className="legend-color risk-medium"></span>
                        <span>Medium Risk: Review carefully</span>
                    </div>
                    <div className="legend-item">
                        <span className="legend-color risk-high"></span>
                        <span>High Risk: Recommendation to decline or require collateral</span>
                    </div>
                </div>
            </div>

            {/* Details Section */}
            <div className="details-section">
                <h4>Assessment Details</h4>
                <p>
                    The system has analyzed the applicant's loan details and determined 
                    a <strong>{risk.toLowerCase()}</strong> risk profile. The estimated 
                    probability of default is <strong>{probabilityPercentage}%</strong>.
                </p>
                <p className="action-details">
                    <strong>Action:</strong> {action}
                </p>
            </div>
        </div>
    );
};

export default Dashboard;
