
import { useState } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  BookOpen,
  BrainCircuit,
  CheckCircle2,
  ChevronRight,
  Clock3,
  Code2,
  Cpu,
  FileText,
  Gauge,
  Layers3,
  LoaderCircle,
  ShieldCheck,
  Sparkles,
  Users,
} from "lucide-react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const sections = [
  { id: "overview", label: "Overview", icon: Gauge },
  { id: "generator", label: "Project Generator", icon: Sparkles },
  { id: "blueprints", label: "Blueprint Results", icon: FileText },
];

function App() {
  const [activeSection, setActiveSection] = useState("overview");
  const [projectIdea, setProjectIdea] = useState("");
  const [duration, setDuration] = useState(8);
  const [teamSize, setTeamSize] = useState(6);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  async function generateBlueprint(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `${API_URL}/api/ai/generate-blueprint`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            project_idea: projectIdea,
            duration_weeks: Number(duration),
            team_size: Number(teamSize),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Blueprint generation failed. Check the backend terminal."
        );
      }

      setResult(data);
      setActiveSection("blueprints");
    } catch (err) {
      setError(
        err.message.includes("Failed to fetch")
          ? "Cannot reach the backend. Make sure FastAPI is running on port 8000."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  const blueprint = result?.blueprint;
  const quality = result?.quality_report;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><BrainCircuit size={25} /></div>
          <div>
            <h2>ProjectMentor</h2>
            <p>AI ACADEMIC STUDIO</p>
          </div>
        </div>

        <div className="workspace-label">WORKSPACE</div>

        <nav className="navigation">
          {sections.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              className={`nav-item ${activeSection === id ? "active" : ""}`}
              onClick={() => setActiveSection(id)}
            >
              <Icon size={19} />
              <span>{label}</span>
              {activeSection === id && <ChevronRight size={16} />}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-tip">
            <Sparkles size={20} />
            <h3>Build smarter projects</h3>
            <p>Turn your academic idea into a structured implementation plan.</p>
            <button onClick={() => setActiveSection("generator")}>
              Get started <ArrowRight size={15} />
            </button>
          </div>
          <div className="profile">
            <div className="avatar">AI</div>
            <div><strong>Student Workspace</strong><span>Academic project lab</span></div>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="breadcrumb">Workspace</span>
            <ChevronRight size={14} />
            <strong>
              {sections.find((item) => item.id === activeSection)?.label}
            </strong>
          </div>
          <div className="api-status">
            <span className="status-dot" /> AI ENGINE
            <span className="model-name">Gemini API</span>
          </div>
        </header>

        <div className="page-content">
          {activeSection === "overview" && (
            <>
              <section className="welcome">
                <div>
                  <div className="eyebrow"><Sparkles size={15} /> YOUR AI PROJECT PARTNER</div>
                  <h1>From idea to <span>blueprint.</span></h1>
                  <p>Plan your next academic project with AI-powered feasibility analysis, technology recommendations, timelines, and risk assessment.</p>
                  <button className="primary-button" onClick={() => setActiveSection("generator")}>
                    Generate a blueprint <ArrowRight size={17} />
                  </button>
                </div>
                <div className="hero-art">
                  <div className="orbit orbit-one" />
                  <div className="orbit orbit-two" />
                  <div className="hero-core"><BrainCircuit size={55} /></div>
                  <div className="floating-chip chip-one"><Cpu size={17} /> AI analysis</div>
                  <div className="floating-chip chip-two"><Layers3 size={17} /> Smart planning</div>
                  <div className="floating-chip chip-three"><ShieldCheck size={17} /> Risk checks</div>
                </div>
              </section>

              <section className="section-heading">
                <div><h2>Your project workspace</h2><p>Everything you need to get started</p></div>
              </section>

              <div className="stats-grid">
                <Stat icon={BrainCircuit} label="AI agents" value="05" detail="Specialized roles" />
                <Stat icon={Layers3} label="Analysis stages" value="05" detail="One unified workflow" />
                <Stat icon={ShieldCheck} label="Quality checks" value={quality ? String(quality.checks?.length ?? 0).padStart(2, "0") : "04"} detail="Blueprint validation" />
                <Stat icon={Activity} label="Blueprints created" value={result ? "01" : "00"} detail="This session" />
              </div>

              <section className="section-heading">
                <div><h2>How it works</h2><p>Five agents collaborate to prepare your blueprint</p></div>
              </section>

              <div className="agent-grid">
                <Agent icon={Gauge} number="01" title="Feasibility" description="Evaluate project practicality and resources." />
                <Agent icon={Layers3} number="02" title="Scope definition" description="Identify deliverables and project boundaries." />
                <Agent icon={Code2} number="03" title="Technology stack" description="Recommend suitable tools and frameworks." />
                <Agent icon={Clock3} number="04" title="Project planning" description="Build a phased implementation timeline." />
                <Agent icon={ShieldCheck} number="05" title="Risk assessment" description="Identify risks and mitigation strategies." />
              </div>

              <div className="bottom-banner">
                <div className="banner-icon"><BookOpen size={23} /></div>
                <div><h3>Have a project idea?</h3><p>Start with a simple description. Your AI agents will do the initial analysis.</p></div>
                <button className="secondary-button" onClick={() => setActiveSection("generator")}>Start a project <ArrowRight size={16} /></button>
              </div>
            </>
          )}

          {activeSection === "generator" && (
            <section className="generator-page">
              <div className="eyebrow"><Sparkles size={15} /> AI-POWERED WORKFLOW</div>
              <h1>Project <span>generator</span></h1>
              <p className="page-description">Describe your idea. Our five-agent workflow will prepare a structured project blueprint.</p>

              <form className="generator-card" onSubmit={generateBlueprint}>
                <div className="form-title"><div className="form-icon"><BrainCircuit size={22} /></div><div><h2>Tell us about your project</h2><p>Provide enough detail for a useful initial assessment.</p></div></div>

                <label htmlFor="projectIdea">Project idea <span>*</span></label>
                <textarea
                  id="projectIdea"
                  required
                  minLength={3}
                  maxLength={2000}
                  value={projectIdea}
                  onChange={(e) => setProjectIdea(e.target.value)}
                  placeholder="Example: AI-powered demand forecasting for Indian retail sales..."
                  rows={5}
                />
                <div className="character-count">{projectIdea.length}/2000 characters</div>

                <div className="form-grid">
                  <div>
                    <label htmlFor="duration">Project duration</label>
                    <select id="duration" value={duration} onChange={(e) => setDuration(e.target.value)}>
                      {[2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 52].map((week) => (
                        <option key={week} value={week}>{week} weeks</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label htmlFor="teamSize">Team size</label>
                    <select id="teamSize" value={teamSize} onChange={(e) => setTeamSize(e.target.value)}>
                      {[1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20].map((size) => (
                        <option key={size} value={size}>{size} {size === 1 ? "member" : "members"}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {error && <div className="error-box"><AlertTriangle size={18} />{error}</div>}

                <button className="primary-button submit-button" type="submit" disabled={loading}>
                  {loading ? <><LoaderCircle className="spin" size={18} /> Generating with five agents...</> : <><Sparkles size={18} /> Generate project blueprint <ArrowRight size={17} /></>}
                </button>
                <p className="privacy-note"><ShieldCheck size={15} /> Your request is sent to your local API and Gemini. Don't enter passwords or private information.</p>
              </form>
            </section>
          )}

          {activeSection === "blueprints" && (
            <section className="results-page">
              <div className="eyebrow"><CheckCircle2 size={15} /> GENERATED BLUEPRINT</div>
              <h1>Blueprint <span>results</span></h1>
              {!result ? (
                <div className="empty-state">
                  <div className="empty-icon"><FileText size={35} /></div>
                  <h2>No blueprint yet</h2>
                  <p>Generate a project blueprint to see the five agent results here.</p>
                  <button className="primary-button" onClick={() => setActiveSection("generator")}>Create blueprint <ArrowRight size={16} /></button>
                </div>
              ) : (
                <>
                  <div className="result-summary">
                    <div><span className="summary-label">PROJECT IDEA</span><h2>{blueprint?.project_idea}</h2><p>Generated by five AI agents</p></div>
                    <div className="quality-pill"><ShieldCheck size={17} /> {quality?.warning_count ?? 0} quality warning(s)</div>
                  </div>

                  <div className="result-grid">
                    <ResultCard title="Feasibility analysis" icon={Gauge} data={blueprint?.feasibility} />
                    <ResultCard title="Project scope" icon={Layers3} data={blueprint?.scope} />
                    <ResultCard title="Technology recommendations" icon={Code2} data={blueprint?.technology} />
                    <ResultCard title="Project plan" icon={Clock3} data={blueprint?.planning} />
                    <ResultCard title="Risk assessment" icon={ShieldCheck} data={blueprint?.risk_assessment} />
                  </div>

                  <section className="quality-card">
                    <div className="quality-title"><ShieldCheck size={21} /><div><h2>Quality report</h2><p>Automated checks on this generated blueprint</p></div></div>
                    {quality?.checks?.map((check, index) => (
                      <div className="check-row" key={`${check.name}-${index}`}>
                        {check.passed ? <CheckCircle2 size={17} className="check-ok" /> : <AlertTriangle size={17} className="check-warning" />}
                        <span>{String(check.name).replaceAll("_", " ")}</span>
                        <strong>{check.passed ? "Passed" : "Review"}</strong>
                      </div>
                    ))}
                    {quality?.warnings?.length > 0 ? quality.warnings.map((warning, index) => (
                      <div className="warning-message" key={index}><AlertTriangle size={17} />{warning}</div>
                    )) : <p className="all-clear"><CheckCircle2 size={17} /> No warnings from the implemented checks.</p>}
                    <p className="disclaimer">{quality?.note}</p>
                  </section>

                  <button className="secondary-button" onClick={() => { setProjectIdea(blueprint?.project_idea || projectIdea); setActiveSection("generator"); }}>
                    Generate another blueprint <ArrowRight size={16} />
                  </button>
                </>
              )}
            </section>
          )}
        </div>
      </main>
    </div>
  );
}

function Stat({ icon: Icon, label, value, detail }) {
  return <div className="stat-card"><div className="stat-top"><span>{label}</span><Icon size={19} /></div><strong>{value}</strong><p>{detail}</p></div>;
}

function Agent({ icon: Icon, number, title, description }) {
  return <div className="agent-card"><div className="agent-top"><div className="agent-icon"><Icon size={20} /></div><span>{number}</span></div><h3>{title}</h3><p>{description}</p></div>;
}

function ResultCard({ title, icon: Icon, data }) {
  return (
    <article className="result-card">
      <div className="result-card-title"><div className="agent-icon"><Icon size={19} /></div><h3>{title}</h3></div>
      {data ? <DataView data={data} /> : <p>No data returned for this section.</p>}
    </article>
  );
}

function DataView({ data }) {
  if (typeof data === "string" || typeof data === "number" || typeof data === "boolean") {
    return <p>{String(data)}</p>;
  }
  if (Array.isArray(data)) {
    return <ul className="data-list">{data.map((item, index) => <li key={index}><DataView data={item} /></li>)}</ul>;
  }
  if (data && typeof data === "object") {
    return (
      <div className="data-fields">
        {Object.entries(data).map(([key, value]) => (
          <div className="data-field" key={key}>
            <span>{key.replaceAll("_", " ")}</span>
            <div><DataView data={value} /></div>
          </div>
        ))}
      </div>
    );
  }
  return <p>—</p>;
}

export default App;
