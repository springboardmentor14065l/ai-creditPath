import Plot from "react-plotly.js";

const actionLabel = (item) => {
  if (item?.action?.includes("Immediate")) {
    return "Immediate outreach";
  }
  if (item?.action?.includes("Call")) {
    return "Pending follow-up";
  }
  return "Reminder sent";
};

function Charts({ batchResult, history, workflowSource }) {
  const localSummary = history.reduce(
    (acc, item) => {
      if (item.risk === "Low") acc.low += 1;
      if (item.risk === "Medium") acc.medium += 1;
      if (item.risk === "High") acc.high += 1;
      return acc;
    },
    { low: 0, medium: 0, high: 0 }
  );

  const summary = batchResult?.summary
    ? {
        low: batchResult.summary.low_risk,
        medium: batchResult.summary.medium_risk,
        high: batchResult.summary.high_risk
      }
    : localSummary;

  const workflowCounts = workflowSource.reduce(
    (acc, item) => {
      const label = actionLabel(item);
      acc[label] = (acc[label] || 0) + 1;
      return acc;
    },
    { "Reminder sent": 0, "Pending follow-up": 0, "Immediate outreach": 0 }
  );

  const chartMax = Math.max(1, summary.low, summary.medium, summary.high);

  return (
    <section className="panel-card chart-stack">
      <div className="section-header">
        <div>
          <h2>Borrower Risk Distribution</h2>
          <p>Live Low, Medium, High borrower counts from API responses.</p>
        </div>
      </div>

      <div className="chart-block">
        <Plot
          data={[
            {
              x: [summary.low, summary.medium, summary.high],
              y: ["Low", "Medium", "High"],
              type: "bar",
              orientation: "h",
              marker: {
                color: ["#0f7f7a", "#77a8b6", "#d7b058"],
                line: { color: "#0c3f49", width: 1 }
              },
              text: [summary.low, summary.medium, summary.high],
              textposition: "outside",
              hovertemplate: "%{y}: %{x}<extra></extra>",
              cliponaxis: false
            }
          ]}
          layout={{
            paper_bgcolor: "transparent",
            plot_bgcolor: "transparent",
            margin: { l: 72, r: 24, t: 12, b: 36 },
            font: { color: "#18364d", family: "Segoe UI, sans-serif" },
            xaxis: {
              title: "Count",
              range: [0, chartMax + 1],
              gridcolor: "#d7dee8",
              zeroline: false,
              fixedrange: true
            },
            yaxis: {
              title: "",
              fixedrange: true
            },
            dragmode: false
          }}
          config={{ displayModeBar: false, responsive: true, staticPlot: true }}
          style={{ width: "100%", height: "220px" }}
        />
      </div>

      <div className="chart-divider" />

      <div className="section-header nested-header">
        <div>
          <h3>Workflow Distribution</h3>
          <p>Operational mix of borrower actions after scoring.</p>
        </div>
      </div>

      <div className="chart-block chart-block-pie">
        <Plot
          data={[
            {
              values: [
                workflowCounts["Reminder sent"],
                workflowCounts["Pending follow-up"],
                workflowCounts["Immediate outreach"]
              ],
              labels: ["Reminder sent", "Pending follow-up", "Immediate outreach"],
              type: "pie",
              hole: 0.25,
              textinfo: "none",
              marker: {
                colors: ["#0f7f7a", "#3d8ca5", "#d0a341"],
                line: { color: "#ffffff", width: 2 }
              },
              hovertemplate: "%{label}: %{value}<extra></extra>"
            }
          ]}
          layout={{
            paper_bgcolor: "transparent",
            plot_bgcolor: "transparent",
            margin: { l: 0, r: 0, t: 0, b: 0 },
            font: { color: "#18364d", family: "Segoe UI, sans-serif" },
            showlegend: true,
            legend: {
              orientation: "v",
              x: 1,
              xanchor: "left",
              y: 0.5
            }
          }}
          config={{ displayModeBar: false, responsive: true, staticPlot: true }}
          style={{ width: "100%", height: "220px" }}
        />
      </div>
    </section>
  );
}

export default Charts;
