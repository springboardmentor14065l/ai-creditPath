import React from "react";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

const Gauge = ({ value }) => {
    let color = "#22c55e";

    if (value > 60) color = "#ef4444";
    else if (value > 30) color = "#f59e0b";

    return (
        <div style={{ width: 90, height: 90, margin: "auto" }}>
            <CircularProgressbar
                value={value}
                text={`${value}%`}
                strokeWidth={8}   // ✅ FIXED (use JS comment, not JSX comment)
                styles={buildStyles({
                    pathColor: color,
                    textColor: "#fff",
                    trailColor: "#1e293b"
                })}
            />
        </div>
    );
};

export default Gauge;