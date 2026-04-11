import React, { useState } from "react";
import { predict } from "../services/api";

const Form = ({ setResult }) => {
    const [formData, setFormData] = useState({
        loan_amnt: "",
        int_rate: "",
        dti: ""
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async () => {
        try {
            const res = await predict(formData);
            setResult(res);
        } catch (error) {
            console.error(error);
            alert("Error connecting to backend");
        }
    };

    return (
        <div>
            <h3>Enter Loan Details</h3>

            {/* ✅ Grid Layout */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>

                <input name="loan_amnt" placeholder="Loan Amount (₹)" onChange={handleChange} style={input}/>
                <input name="int_rate" placeholder="Interest Rate (%)" onChange={handleChange} style={input}/>
                <input name="dti" placeholder="Monthly Expenses Ratio" onChange={handleChange} style={input}/>
                
                {/* These are UI-only for now (not sent to backend) */}
                <input placeholder="Monthly Income (₹)" style={input}/>
                <input placeholder="Employment Years" style={input}/>
                <input placeholder="Loan Term (months)" style={input}/>

            </div>

            <button onClick={handleSubmit} style={btn}>
                Run Risk Assessment
            </button>
        </div>
    );
};

/* ✅ Styles (ADD HERE — inside same file, BELOW component) */

const input = {
    padding: "10px",
    borderRadius: "5px",
    border: "none"
};

const btn = {
    marginTop: "15px",
    padding: "10px",
    background: "#3b82f6",
    color: "white",
    border: "none",
    borderRadius: "5px",
    width: "100%"
};

export default Form;