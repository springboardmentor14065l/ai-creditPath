import { useState } from "react";

function InterventionSimulator({ baselineResult, onSimulate, loading, simulation }) {
  const [creditBoost, setCreditBoost] = useState(20);
  const [dtiDrop, setDtiDrop] = useState(4);
  const [rateCut, setRateCut] = useState(0.01);

  const uplift =
    baselineResult && simulation
      ? Math.max(0, (baselineResult.probability - simulation.probability) * 100)
      : 0;

  return (
    <section className="glass-card simulator-card">
      <div className="section-heading">
        <div>
          <span className="eyebrow">Scenario Planning</span>
          <h2>What happens if the offer improves?</h2>
        </div>
        <p>
          Try a better credit profile, lower DTI, or a reduced rate and compare the likely outcome
          before the agent reaches out.
        </p>
      </div>

      <div className="slider-grid">
        <label className="slider-field">
          <span>Credit score boost</span>
          <strong>+{creditBoost}</strong>
          <input
            type="range"
            min="0"
            max="120"
            step="5"
            value={creditBoost}
            onChange={(event) => setCreditBoost(Number(event.target.value))}
          />
        </label>

        <label className="slider-field">
          <span>DTI reduction</span>
          <strong>-{dtiDrop}</strong>
          <input
            type="range"
            min="0"
            max="15"
            step="1"
            value={dtiDrop}
            onChange={(event) => setDtiDrop(Number(event.target.value))}
          />
        </label>

        <label className="slider-field">
          <span>Rate concession</span>
          <strong>-{rateCut.toFixed(3)}</strong>
          <input
            type="range"
            min="0"
            max="0.04"
            step="0.002"
            value={rateCut}
            onChange={(event) => setRateCut(Number(event.target.value))}
          />
        </label>
      </div>

      <div className="simulator-actions">
        <button
          type="button"
          className="primary-btn"
          onClick={() => onSimulate({ creditBoost, dtiDrop, rateCut })}
          disabled={!baselineResult || loading}
        >
          {loading ? "Simulating..." : "Run What-If Scenario"}
        </button>
        <div className="uplift-badge">
          <span>Potential Risk Drop</span>
          <strong>{simulation ? `${uplift.toFixed(2)} pts` : "--"}</strong>
        </div>
      </div>

      <div className="simulation-panels">
        <div className="mini-panel">
          <span>Baseline</span>
          <strong>{baselineResult ? `${(baselineResult.probability * 100).toFixed(2)}%` : "--"}</strong>
          <small>{baselineResult ? baselineResult.action : "Run a prediction first"}</small>
        </div>
        <div className="mini-panel accent">
          <span>Simulated</span>
          <strong>{simulation ? `${(simulation.probability * 100).toFixed(2)}%` : "--"}</strong>
          <small>{simulation ? simulation.action : "No scenario run yet"}</small>
        </div>
      </div>
    </section>
  );
}

export default InterventionSimulator;
