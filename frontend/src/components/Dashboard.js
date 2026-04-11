import React, { useState } from "react";
import Form from "./Form";
import Gauge from "./Gauge";
import Recommendation from "./Recommendation"; // ✅ added

const Dashboard = () => {
    const [result, setResult] = useState(null);
    const [showReco, setShowReco] = useState(false); // ✅ added

    // ✅ Navigation logic
    if (showReco) {
        return (
            <Recommendation 
                result={result} 
                goBack={() => setShowReco(false)} 
            />
        );
    }

    return (
        <div style={{
            background: "#0f172a",
            minHeight: "100vh",
            color: "white",
            padding: "30px"
        }}>
            <h1 style={{ textAlign: "center", color: "#3b82f6" }}>
                CreditPath AI
            </h1>

            <p style={{ textAlign: "center", marginBottom: "30px" }}>
                Advanced Credit Risk Assessment & Automated Recovery
            </p>

            <div style={{
                display: "flex",
                justifyContent: "center",
                gap: "50px"
            }}>
                
                {/* LEFT CARD */}
                <div style={{
                    background: "#1e293b",
                    padding: "25px",
                    borderRadius: "15px",
                    boxShadow: "0 0 15px rgba(0,0,0,0.5)"
                }}>
                    <Form setResult={setResult} />
                </div>

                {/* RIGHT CARD */}
                {result && (
                    <div style={{
                        background: "#1e293b",
                        padding: "25px",
                        borderRadius: "15px",
                        width: "250px",
                        textAlign: "center"
                    }}>
                        <Gauge value={result.risk_score} />

                        <h2 style={{
                            marginTop: "15px",
                            color:
                                result.risk === "High" ? "#ef4444" :
                                result.risk === "Medium" ? "#f59e0b" : "#22c55e"
                        }}>
                            {result.risk} Risk
                        </h2>

                        <p style={{ marginTop: "10px" }}>
                            {result.action}
                        </p>

                        {/* ✅ NEW BUTTON */}
                        <button
                            onClick={() => setShowReco(true)}
                            style={{
                                marginTop: "10px",
                                padding: "8px",
                                background: "#f59e0b",
                                border: "none",
                                borderRadius: "5px",
                                cursor: "pointer"
                            }}
                        >
                            Get Recommendation
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;