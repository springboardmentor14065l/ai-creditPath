import { useEffect, useMemo, useRef, useState } from "react";
import BatchDashboard from "./BatchDashboard";
import Charts from "./Charts";
import Form from "./Form";
import HeroScene from "./HeroScene";
import { defaultFormData, portfolioTemplates } from "../data/presets";
import { pingApi, predict, predictBatch } from "../services/api";

const tabs = [
  { id: "overview", label: "Overview", sectionId: "overview", icon: "⊞" },
  { id: "input", label: "New Input", sectionId: "input", icon: "✏" },
  { id: "chart", label: "Risk Chart", sectionId: "chart", icon: "◉" },
  { id: "queue", label: "Agent Queue", sectionId: "queue", icon: "≡" }
];

const formatPercent = (value) => {
  if (value === null || value === undefined) {
    return "--";
  }
  return `${(value * 100).toFixed(2)}%`;
};

const parseApiError = (apiError, fallback) => {
  const detail = apiError?.response?.data?.detail;
  if (typeof detail === "string") {
    return detail;
  }
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || item.message || JSON.stringify(item)).join(" | ");
  }
  if (detail && typeof detail === "object") {
    return JSON.stringify(detail);
  }
  return fallback;
};

const buildDriverSummary = (drivers = []) =>
  drivers
    .slice(0, 3)
    .map((driver) => `${driver.label} ${driver.direction}`)
    .join(" | ");

/* ── Modal overlay component ── */
function Modal({ title, onClose, children }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-panel" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">{title}</h2>
          <button type="button" className="modal-close" onClick={onClose}>✕</button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
}

function Dashboard() {
  const [formData, setFormData] = useState(defaultFormData);
  const [apiStatus, setApiStatus] = useState("Checking...");
  const [result, setResult] = useState(null);
  const [batchResult, setBatchResult] = useState(null);
  const [queue, setQueue] = useState([]);
  const [history, setHistory] = useState([]);
  const [loadingSingle, setLoadingSingle] = useState(false);
  const [loadingBatch, setLoadingBatch] = useState(false);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("overview");
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [showAdminModal, setShowAdminModal] = useState(false);
  const [settingsValues, setSettingsValues] = useState({
    apiUrl: "http://127.0.0.1:8000",
    theme: "light",
    notifyOnHighRisk: true,
    autoAddToQueue: false
  });
  const [adminSaved, setAdminSaved] = useState(false);

  const sectionRefs = {
    overview: useRef(null),
    input: useRef(null),
    chart: useRef(null),
    queue: useRef(null)
  };

  useEffect(() => {
    const checkApi = async () => {
      try {
        await pingApi();
        setApiStatus("Online");
      } catch (apiError) {
        setApiStatus("Offline");
        setError(parseApiError(apiError, "Unable to connect to FastAPI. Start the backend and refresh the page."));
      }
    };

    checkApi();
  }, []);

  const normalizeValue = (name, value) => {
    if (name === "borrower_id") {
      return value;
    }

    const numericValue = Number(value);
    return Number.isNaN(numericValue) ? 0 : numericValue;
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((current) => ({
      ...current,
      [name]: normalizeValue(name, value)
    }));
  };

  const loadPreset = (template) => {
    setFormData(template);
    setError("");
    setResult(null);
  };

  const navigateToTab = (tabId) => {
    setActiveTab(tabId);
    const section = sectionRefs[tabId]?.current;
    if (section) {
      section.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  const submitSingle = async () => {
    setLoadingSingle(true);
    setError("");

    try {
      const response = await predict(formData);
      setResult(response);
      setActiveTab("overview");
      setHistory((current) => [
        ...current.slice(-7),
        {
          label: formData.borrower_id || `Case ${current.length + 1}`,
          probability: response.probability,
          risk: response.risk,
          action: response.action
        }
      ]);
    } catch (apiError) {
      setError(parseApiError(apiError, "Prediction failed. Verify the API URL and check backend validation."));
    } finally {
      setLoadingSingle(false);
    }
  };

  const handleAddToQueue = () => {
    setQueue((current) => {
      const borrowerId = formData.borrower_id || `queued-${current.length + 1}`;
      const deduped = current.filter((record) => record.borrower_id !== borrowerId);
      return [...deduped, { ...formData, borrower_id: borrowerId }];
    });
    setActiveTab("queue");
  };

  const runBatch = async (records) => {
    setLoadingBatch(true);
    setError("");

    try {
      const response = await predictBatch(records);
      setBatchResult(response);
      setActiveTab("queue");
    } catch (apiError) {
      setError(parseApiError(apiError, "Batch prediction failed. Make sure FastAPI is running and accepting records."));
    } finally {
      setLoadingBatch(false);
    }
  };

  const resetForm = () => {
    setFormData(defaultFormData);
    setResult(null);
    setError("");
    setActiveTab("input");
  };

  const borrowerCount = batchResult?.summary?.total_borrowers || queue.length || history.length || 0;
  const queueLength = queue.length;
  const driverSummary = buildDriverSummary(result?.top_risk_drivers);

  const workflowSummary = useMemo(() => {
    const source = batchResult?.predictions?.length
      ? batchResult.predictions
      : history.map((item, index) => ({
          borrower_id: item.label || `borrower-${index + 1}`,
          risk: item.risk,
          action: item.action || "Low Risk - Send Reminder",
          probability: item.probability,
          urgency_window_hours: item.risk === "High" ? 4 : item.risk === "Medium" ? 24 : 72
        }));

    return source;
  }, [batchResult, history]);

  const activeContentClass = `content-panel content-${activeTab}`;

  return (
    <main className="dashboard-shell">
      <aside className="sidebar">
        <div className="brand-lockup">
          <div className="brand-mark">CP</div>
          <div>
            <div className="brand-title">CreditPathAI</div>
            <div className="brand-subtitle">Recovery command center</div>
          </div>
        </div>

        <div className="sidebar-nav">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              type="button"
              className={`sidebar-tab ${activeTab === tab.id ? "is-active" : ""}`}
              onClick={() => navigateToTab(tab.id)}
            >
              <span className="sidebar-icon">{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        <div className="sidebar-footer">
          <button
            type="button"
            className="sidebar-meta"
            onClick={() => setShowSettingsModal(true)}
            title="Open Settings"
          >
            <span className="sidebar-icon">⚙</span>
            <span>Settings</span>
          </button>
          <button
            type="button"
            className="admin-card admin-card-btn"
            onClick={() => setShowAdminModal(true)}
            title="View Admin Profile"
          >
            <div className="admin-avatar">A</div>
            <div>
              <div className="admin-name">Admin</div>
              <div className="admin-role">Operations lead</div>
            </div>
            <span className="admin-arrow">›</span>
          </button>
        </div>
      </aside>

      <section className={activeContentClass}>
        <header ref={sectionRefs.overview} id="overview" className="page-header">
          <HeroScene
            apiStatus={apiStatus}
            latestResult={result}
            borrowerCount={borrowerCount}
            queueLength={queueLength}
          />
        </header>

        {error ? <div className="error-banner">{String(error)}</div> : null}

        <div className="layout-grid">
          <section ref={sectionRefs.input} id="input" className="input-panel">
            <Form
              formData={formData}
              onChange={handleChange}
              onSubmit={submitSingle}
              onReset={resetForm}
              onAddToQueue={handleAddToQueue}
              onLoadPreset={loadPreset}
              presets={{
                "Low Risk": portfolioTemplates[0],
                "Medium Risk": portfolioTemplates[1],
                "High Risk": portfolioTemplates[2]
              }}
              loading={loadingSingle}
              result={result}
              formatPercent={formatPercent}
              driverSummary={driverSummary}
            />
          </section>

          <section ref={sectionRefs.chart} id="chart" className="chart-panel">
            <Charts
              batchResult={batchResult}
              history={history}
              workflowSource={workflowSummary}
            />
          </section>
        </div>

        <section ref={sectionRefs.queue} id="queue" className="queue-panel">
          <BatchDashboard
            queue={queue}
            batchResult={batchResult}
            onRunTemplates={() => runBatch(portfolioTemplates)}
            onRunQueue={() => runBatch(queue)}
            loading={loadingBatch}
          />
        </section>
      </section>

      {/* ── Settings Modal ── */}
      {showSettingsModal && (
        <Modal title="⚙ Settings" onClose={() => setShowSettingsModal(false)}>
          <div className="modal-form">
            <div className="modal-field">
              <label className="modal-field-label">API Base URL</label>
              <input
                className="modal-field-input"
                type="text"
                value={settingsValues.apiUrl}
                onChange={(e) => setSettingsValues((s) => ({ ...s, apiUrl: e.target.value }))}
                placeholder="http://127.0.0.1:8000"
              />
              <span className="modal-field-hint">The base URL of your FastAPI backend.</span>
            </div>

            <div className="modal-field">
              <label className="modal-field-label">Theme</label>
              <select
                className="modal-field-input"
                value={settingsValues.theme}
                onChange={(e) => setSettingsValues((s) => ({ ...s, theme: e.target.value }))}
              >
                <option value="light">Light ☀</option>
                <option value="dark">Dark 🌙</option>
                <option value="auto">System default 💻</option>
              </select>
            </div>

            <div className="modal-toggle-row">
              <div>
                <div className="modal-field-label">Notify on High Risk</div>
                <span className="modal-field-hint">Show an alert banner when a high-risk borrower is scored.</span>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settingsValues.notifyOnHighRisk}
                  onChange={(e) => setSettingsValues((s) => ({ ...s, notifyOnHighRisk: e.target.checked }))}
                />
                <span className="toggle-track" />
              </label>
            </div>

            <div className="modal-toggle-row">
              <div>
                <div className="modal-field-label">Auto-add to Queue</div>
                <span className="modal-field-hint">Automatically add each prediction to the agent queue.</span>
              </div>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settingsValues.autoAddToQueue}
                  onChange={(e) => setSettingsValues((s) => ({ ...s, autoAddToQueue: e.target.checked }))}
                />
                <span className="toggle-track" />
              </label>
            </div>

            <div className="modal-actions">
              <button type="button" className="btn btn-ghost" onClick={() => setShowSettingsModal(false)}>Cancel</button>
              <button type="button" className="btn btn-primary" onClick={() => setShowSettingsModal(false)}>Save Settings</button>
            </div>
          </div>
        </Modal>
      )}

      {/* ── Admin Modal ── */}
      {showAdminModal && (
        <Modal title="👤 Admin Profile" onClose={() => setShowAdminModal(false)}>
          <div className="modal-form">
            <div className="admin-profile-header">
              <div className="admin-profile-avatar">A</div>
              <div>
                <div className="admin-profile-name">Admin User</div>
                <div className="admin-profile-role">Operations Lead · CreditPath AI</div>
              </div>
            </div>

            <div className="modal-section-title">Access & Permissions</div>
            <div className="admin-perm-list">
              {[
                { label: "Run Predictions", granted: true },
                { label: "Add to Agent Queue", granted: true },
                { label: "View Batch Results", granted: true },
                { label: "Export Reports", granted: true },
                { label: "Modify Model Config", granted: false },
                { label: "Manage Users", granted: false }
              ].map((perm) => (
                <div key={perm.label} className="admin-perm-row">
                  <span className={`perm-dot ${perm.granted ? "perm-granted" : "perm-denied"}`} />
                  <span className="perm-label">{perm.label}</span>
                  <span className={`perm-status ${perm.granted ? "perm-granted-text" : "perm-denied-text"}`}>
                    {perm.granted ? "Granted" : "Restricted"}
                  </span>
                </div>
              ))}
            </div>

            <div className="modal-section-title" style={{ marginTop: "20px" }}>Session Info</div>
            <div className="admin-session-grid">
              <div className="session-item">
                <span className="session-label">Environment</span>
                <span className="session-value">Development</span>
              </div>
              <div className="session-item">
                <span className="session-label">API Status</span>
                <span className={`session-value ${apiStatus === "Online" ? "text-success" : "text-danger"}`}>
                  {apiStatus}
                </span>
              </div>
              <div className="session-item">
                <span className="session-label">Borrowers Processed</span>
                <span className="session-value">{borrowerCount}</span>
              </div>
              <div className="session-item">
                <span className="session-label">Queue Length</span>
                <span className="session-value">{queueLength}</span>
              </div>
            </div>

            <div className="modal-actions">
              <button type="button" className="btn btn-ghost" onClick={() => setShowAdminModal(false)}>Close</button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => { setAdminSaved(true); setTimeout(() => setAdminSaved(false), 2000); }}
              >
                {adminSaved ? "✓ Saved!" : "Save Changes"}
              </button>
            </div>
          </div>
        </Modal>
      )}
    </main>
  );
}

export default Dashboard;
