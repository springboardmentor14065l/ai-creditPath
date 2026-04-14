import { useEffect, useMemo, useRef, useState } from "react";
import BatchDashboard from "./BatchDashboard";
import Charts from "./Charts";
import Form from "./Form";
import HeroScene from "./HeroScene";
import { defaultFormData, portfolioTemplates } from "../data/presets";
import { pingApi, predict, predictBatch } from "../services/api";

const tabs = [
  { id: "overview", label: "Overview", sectionId: "overview" },
  { id: "input", label: "New Input", sectionId: "input" },
  { id: "chart", label: "Risk Chart", sectionId: "chart" },
  { id: "queue", label: "Agent Queue", sectionId: "queue" }
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
              <span className="sidebar-icon">{tab.label.slice(0, 1)}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        <div className="sidebar-footer">
          <button type="button" className="sidebar-meta">
            <span className="sidebar-icon">S</span>
            <span>Settings</span>
          </button>
          <div className="admin-card">
            <div className="admin-avatar">A</div>
            <div>
              <div className="admin-name">Admin</div>
              <div className="admin-role">Operations lead</div>
            </div>
          </div>
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
    </main>
  );
}

export default Dashboard;
