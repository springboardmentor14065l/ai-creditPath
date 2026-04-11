import React from "react";

const Recommendation = ({ result, goBack }) => {
    return (
        <div style={{
            height: "100vh",
            background: "#0f172a",
            color: "white",
            display: "flex",
            justifyContent: "center",
            alignItems: "center"
        }}>
            <div style={{
                background: "#1e293b",
                padding: "30px",
                borderRadius: "15px",
                textAlign: "center"
            }}>
                <h2>💡 Recommendation</h2>

                <p>
                    {result.risk === "High"
                        ? "⚠️ High risk detected. Avoid approving loan immediately."
                        : result.risk === "Medium"
                        ? "⚡ Moderate risk. Monitor repayment closely."
                        : "✅ Safe applicant. Loan can be approved."}
                </p>

                <button onClick={goBack}>Back</button>
            </div>
        </div>
    );
};

export default Recommendation;