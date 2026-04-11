import React, { useState } from "react";

const Login = ({ setIsLoggedIn }) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = () => {
        if (username && password) {
            setIsLoggedIn(true);
        } else {
            alert("Please enter username and password");
        }
    };

    return (
        <div style={{
            height: "100vh",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            background: "linear-gradient(to right, #0f172a, #1e293b)",
            color: "white"
        }}>
            <div style={{
                background: "#1e293b",
                padding: "40px",
                borderRadius: "15px",
                width: "300px",
                boxShadow: "0 0 20px rgba(0,0,0,0.6)",
                textAlign: "center"
            }}>
                <h2 style={{ color: "#3b82f6" }}>Welcome to CreditPath AI</h2>
                <p style={{ fontSize: "14px", marginBottom: "20px" }}>
                    Smart Credit Risk Assessment System
                </p>

                <input
                    placeholder="Username"
                    onChange={(e) => setUsername(e.target.value)}
                    style={inputStyle}
                />

                <input
                    type="password"
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)}
                    style={inputStyle}
                />

                <button onClick={handleLogin} style={buttonStyle}>
                    Login
                </button>
            </div>
        </div>
    );
};

const inputStyle = {
    width: "100%",
    padding: "10px",
    margin: "10px 0",
    borderRadius: "5px",
    border: "none"
};

const buttonStyle = {
    width: "100%",
    padding: "10px",
    background: "#3b82f6",
    color: "white",
    border: "none",
    borderRadius: "5px",
    marginTop: "10px",
    cursor: "pointer"
};

export default Login;