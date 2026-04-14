import { useMemo, useState } from "react";

const formatPercent = (value) => `${(value * 100).toFixed(2)}%`;

const mapActionStatus = (action) => {
  if (action?.includes("Immediate")) {
    return "Immediate outreach";
  }
  if (action?.includes("Call")) {
    return "Pending follow-up";
  }
  return "Reminder sent";
};

const formatUrgency = (hours) => {
  if (hours <= 4) {
    return "Within 4 hours";
  }
  if (hours <= 24) {
    return "Next 24 hours";
  }
  return "Next 3 days";
};

const buildAvatar = (borrowerId = "U") => borrowerId.trim().slice(0, 1).toUpperCase();

function BatchDashboard({ queue, batchResult, onRunTemplates, onRunQueue, loading }) {
  const [borrowerFilter, setBorrowerFilter] = useState("");
  const [riskFilter, setRiskFilter] = useState("All");
  const [actionFilter, setActionFilter] = useState("All");

  const filteredRows = useMemo(
    () => {
      const predictions = batchResult?.predictions || [];
      return predictions.filter((item) => {
        const actionStatus = mapActionStatus(item.action);
        const borrowerMatches = item.borrower_id.toLowerCase().includes(borrowerFilter.toLowerCase());
        const riskMatches = riskFilter === "All" || item.risk === riskFilter;
        const actionMatches = actionFilter === "All" || actionStatus === actionFilter;
        return borrowerMatches && riskMatches && actionMatches;
      });
    },
    [actionFilter, batchResult, borrowerFilter, riskFilter]
  );

  return (
    <section className="panel-card queue-card">
      <div className="section-header">
        <div>
          <h2>Agent Recommendation Dashboard</h2>
          <p>Run batch scoring and prioritize borrowers by risk.</p>
        </div>
      </div>

      <div className="action-row">
        <button type="button" className="btn btn-secondary" onClick={onRunTemplates} disabled={loading}>
          Run Demo Batch
        </button>
        <button type="button" className="btn btn-primary" onClick={onRunQueue} disabled={loading || queue.length === 0}>
          {loading ? "Running Queue..." : `Run Queue (n) (${queue.length})`}
        </button>
      </div>

      <div className="table-wrap">
        <table className="queue-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Borrower</th>
              <th>Risk</th>
              <th>Probability</th>
              <th>Action</th>
              <th>Urgency</th>
            </tr>
            <tr className="filter-row">
              <th>
                <input value="" readOnly aria-label="Rank filter placeholder" />
              </th>
              <th>
                <input
                  value={borrowerFilter}
                  onChange={(event) => setBorrowerFilter(event.target.value)}
                  placeholder="Filter"
                  aria-label="Filter borrowers"
                />
              </th>
              <th>
                <select value={riskFilter} onChange={(event) => setRiskFilter(event.target.value)} aria-label="Filter risk">
                  <option value="All">Risk</option>
                  <option value="Low">Low</option>
                  <option value="Medium">Medium</option>
                  <option value="High">High</option>
                </select>
              </th>
              <th>
                <input value="" readOnly aria-label="Probability filter placeholder" />
              </th>
              <th>
                <select value={actionFilter} onChange={(event) => setActionFilter(event.target.value)} aria-label="Filter action">
                  <option value="All">Status</option>
                  <option value="Reminder sent">Reminder sent</option>
                  <option value="Pending follow-up">Pending follow-up</option>
                  <option value="Immediate outreach">Immediate outreach</option>
                </select>
              </th>
              <th>
                <input value="" readOnly aria-label="Urgency filter placeholder" />
              </th>
            </tr>
          </thead>
          <tbody>
            {filteredRows.length ? (
              filteredRows.map((item) => {
                const actionStatus = mapActionStatus(item.action);
                const probabilityWidth = `${Math.max(8, item.probability * 100)}%`;

                return (
                  <tr key={item.borrower_id}>
                    <td>{item.priority_rank}</td>
                    <td>
                      <div className="borrower-cell">
                        <span className="avatar-chip">{buildAvatar(item.borrower_id)}</span>
                        <span>{item.borrower_id}</span>
                      </div>
                    </td>
                    <td>
                      <span className={`risk-badge risk-${item.risk.toLowerCase()}`}>{item.risk}</span>
                    </td>
                    <td>
                      <div className="probability-cell">
                        <span>{formatPercent(item.probability)}</span>
                        <span className="probability-track">
                          <span className="probability-bar" style={{ width: probabilityWidth }} />
                        </span>
                      </div>
                    </td>
                    <td>
                      <span className={`action-badge action-${actionStatus.toLowerCase().replace(/\s+/g, "-")}`}>
                        {actionStatus}
                      </span>
                    </td>
                    <td>{formatUrgency(item.urgency_window_hours)}</td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={6} className="empty-state">
                  No batch results yet. Add borrowers and run queue.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default BatchDashboard;
