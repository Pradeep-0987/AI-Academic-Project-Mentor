
import { useEffect, useState } from "react";
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
  MessageCircle,
  Send,
  Plus,
  CalendarDays,
  ShieldCheck,
  Sparkles,
  Users,
  Download,
  GraduationCap,
  RefreshCw,
} from "lucide-react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const sections = [
  { id: "overview", label: "Overview", icon: Gauge },
  { id: "generator", label: "Project Generator", icon: Sparkles },
  { id: "blueprints", label: "Blueprint Results", icon: FileText },
  { id: "mentor", label: "AI Mentor & Progress", icon: MessageCircle },
  { id: "documents", label: "Project Documents", icon: FileText },
  { id: "faculty", label: "Faculty Dashboard", icon: GraduationCap },
];

function App() {
  const [activeSection, setActiveSection] = useState("overview");
  const [projectIdea, setProjectIdea] = useState("");
  const [duration, setDuration] = useState(8);
  const [teamSize, setTeamSize] = useState(6);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [mentorProjects, setMentorProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [mentorProjectName, setMentorProjectName] = useState("");
  const [mentorProjectIdea, setMentorProjectIdea] = useState("");
  const [mentorMessages, setMentorMessages] = useState([
    { role: "assistant", content: "Hi! I'm your AI academic project mentor. Create or select a project, then ask me about your next task, blockers, milestones, or viva preparation." },
  ]);
  const [mentorInput, setMentorInput] = useState("");
  const [mentorLoading, setMentorLoading] = useState(false);
  const [mentorError, setMentorError] = useState("");
  const [milestoneTitle, setMilestoneTitle] = useState("");
  const [milestoneDueDate, setMilestoneDueDate] = useState("");
  const [documentType, setDocumentType] = useState("synopsis");
  const [documents, setDocuments] = useState([]);
  const [documentProjectId, setDocumentProjectId] = useState("");
  const [documentResult, setDocumentResult] = useState(null);
  const [documentLoading, setDocumentLoading] = useState(false);
  const [documentError, setDocumentError] = useState("");
  const [facultyToken, setFacultyToken] = useState("");
  const [facultyData, setFacultyData] = useState(null);
  const [facultyLoading, setFacultyLoading] = useState(false);
  const [facultyError, setFacultyError] = useState("");

  async function loadMentorProjects() {
    try {
      const response = await fetch(`${API_URL}/api/mentor/projects`);
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Unable to load projects.");
      setMentorProjects(data.projects || []);
      if (selectedProjectId) {
        const selected = (data.projects || []).find((p) => String(p.id) === String(selectedProjectId));
        if (selected) await loadMentorProject(selected.id);
      }
    } catch (err) { setMentorError(err.message); }
  }

  async function loadMentorProject(id) {
    if (!id) return;
    try {
      const response = await fetch(`${API_URL}/api/mentor/projects/${id}`);
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Unable to load project.");
      setSelectedProjectId(String(id));
      setMentorMessages(data.project.messages?.length ? data.project.messages : [
        { role: "assistant", content: `I'm ready to help with ${data.project.name}. Tell me your current progress or what is blocking you.` },
      ]);
    } catch (err) { setMentorError(err.message); }
  }

  async function createMentorProject(event) {
    event.preventDefault();
    setMentorError("");
    try {
      const response = await fetch(`${API_URL}/api/mentor/projects`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: mentorProjectName, idea: mentorProjectIdea }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Project creation failed.");
      setMentorProjectName(""); setMentorProjectIdea("");
      await loadMentorProjects();
      await loadMentorProject(data.project.id);
    } catch (err) { setMentorError(err.message); }
  }

  async function sendMentorMessage(event) {
    event.preventDefault();
    const message = mentorInput.trim();
    if (!message || mentorLoading) return;
    const nextMessages = [...mentorMessages, { role: "user", content: message }];
    setMentorMessages(nextMessages); setMentorInput(""); setMentorLoading(true); setMentorError("");
    try {
      const response = await fetch(`${API_URL}/api/mentor/chat`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, project_id: selectedProjectId ? Number(selectedProjectId) : null, history: nextMessages.slice(-12) }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Mentor request failed.");
      setMentorMessages((current) => [...current, { role: "assistant", content: data.reply }]);
      if (selectedProjectId) await loadMentorProjects();
    } catch (err) { setMentorError(err.message); }
    finally { setMentorLoading(false); }
  }

  async function addMentorMilestone(event) {
    event.preventDefault();
    if (!selectedProjectId || !milestoneTitle.trim()) return;
    try {
      const response = await fetch(`${API_URL}/api/mentor/projects/${selectedProjectId}/milestones`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: milestoneTitle, due_date: milestoneDueDate || null }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Could not add milestone.");
      setMilestoneTitle(""); setMilestoneDueDate(""); await loadMentorProjects();
      await loadMentorProject(selectedProjectId);
      setMentorError("");
    } catch (err) { setMentorError(err.message); }
  }

  async function changeMilestoneStatus(milestoneId, status) {
    try {
      const response = await fetch(`${API_URL}/api/mentor/milestones/${milestoneId}`, {
        method: "PATCH", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Could not update milestone.");
      await loadMentorProjects(); await loadMentorProject(selectedProjectId); setMentorError("");
    } catch (err) { setMentorError(err.message); }
  }

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

  useEffect(() => { loadMentorProjects(); }, []);

  const blueprint = result?.blueprint;
  const quality = result?.quality_report;


  async function loadDocuments(projectId = documentProjectId) {
    if (!projectId) {
      setDocumentError("Select a tracked project first.");
      return;
    }
    setDocumentError("");
    try {
      const response = await fetch(`${API_URL}/api/documents/projects/${projectId}`);
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Could not load documents.");
      setDocuments(data.documents || []);
    } catch (err) {
      setDocumentError(err.message);
    }
  }

  async function generateDocument(event) {
    event.preventDefault();
    if (!documentProjectId) {
      setDocumentError("Create or select a tracked project in AI Mentor & Progress first.");
      return;
    }
    setDocumentLoading(true);
    setDocumentError("");
    setDocumentResult(null);
    try {
      const response = await fetch(`${API_URL}/api/documents/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_id: Number(documentProjectId),
          document_type: documentType,
        }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Document generation failed.");
      setDocumentResult(data.document);
      await loadDocuments(documentProjectId);
    } catch (err) {
      setDocumentError(err.message);
    } finally {
      setDocumentLoading(false);
    }
  }

  async function loadFacultyDashboard(event) {
    if (event) event.preventDefault();
    setFacultyLoading(true);
    setFacultyError("");
    try {
      const response = await fetch(`${API_URL}/api/faculty/dashboard`, {
        headers: { "X-Faculty-Token": facultyToken },
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Could not load faculty dashboard.");
      setFacultyData(data);
    } catch (err) {
      setFacultyError(err.message);
      setFacultyData(null);
    } finally {
      setFacultyLoading(false);
    }
  }

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
                <Stat icon={BrainCircuit} label="AI agents" value="10" detail="Specialized roles" />
                <Stat icon={Layers3} label="Analysis stages" value="10" detail="One unified workflow" />
                <Stat icon={ShieldCheck} label="Quality checks" value={quality ? String(quality.checks?.length ?? 0).padStart(2, "0") : "04"} detail="Blueprint validation" />
                <Stat icon={Activity} label="Blueprints created" value={result ? "01" : "00"} detail="This session" />
              </div>

              <section className="section-heading">
                <div><h2>How it works</h2><p>Ten agents collaborate to prepare your blueprint</p></div>
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
                  {loading ? <><LoaderCircle className="spin" size={18} /> Generating with ten agents...</> : <><Sparkles size={18} /> Generate project blueprint <ArrowRight size={17} /></>}
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
                    <div><span className="summary-label">PROJECT IDEA</span><h2>{blueprint?.project_idea}</h2><p>Generated by ten AI agents</p></div>
                    <div className="quality-pill"><ShieldCheck size={17} /> {quality?.warning_count ?? 0} quality warning(s)</div>
                  </div>

                  <div className="result-grid">
                    <ResultCard title="Feasibility analysis" icon={Gauge} data={blueprint?.feasibility} />
                    <ResultCard title="Project scope" icon={Layers3} data={blueprint?.scope} />
                    <ResultCard title="Technology recommendations" icon={Code2} data={blueprint?.technology} />
                    <ResultCard title="Project plan" icon={Clock3} data={blueprint?.planning} />
                    <ResultCard title="Risk assessment" icon={ShieldCheck} data={blueprint?.risk_assessment} />
                    <ResultCard title="Research & literature plan" icon={BookOpen} data={blueprint?.research} />
                    <ResultCard title="Dataset & data quality plan" icon={Layers3} data={blueprint?.dataset} />
                    <ResultCard title="System architecture" icon={Cpu} data={blueprint?.architecture} />
                    <ResultCard title="Testing & evaluation plan" icon={Activity} data={blueprint?.testing} />
                    <ResultCard title="Documentation & viva plan" icon={FileText} data={blueprint?.documentation} />
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

          {activeSection === "mentor" && (
            <section className="results-page mentor-page">
              <div className="eyebrow"><MessageCircle size={15} /> CONTINUOUS PROJECT GUIDANCE</div>
              <h1>AI mentor <span>& progress</span></h1>
              <p className="page-description">Talk through blockers, plan your next task, and keep milestone status in one place. Projects and messages are stored in your local SQLite database.</p>
              {mentorError && <div className="error-box"><AlertTriangle size={18} />{mentorError}</div>}
              <div className="mentor-layout">
                <aside className="mentor-projects-panel">
                  <div className="quality-title"><Layers3 size={20} /><div><h2>Your projects</h2><p>Persistent local tracking</p></div></div>
                  <button className="secondary-button mentor-refresh" onClick={loadMentorProjects}>Refresh projects</button>
                  <div className="mentor-project-list">
                    {mentorProjects.map((project) => (
                      <button key={project.id} className={`mentor-project-option ${String(project.id) === String(selectedProjectId) ? "selected" : ""}`} onClick={() => loadMentorProject(project.id)}>
                        <strong>{project.name}</strong><span>{project.completed_count || 0}/{project.milestone_count || 0} milestones complete</span>
                      </button>
                    ))}
                    {!mentorProjects.length && <p className="muted-copy">Create your first project below.</p>}
                  </div>
                  <form className="mentor-create-form" onSubmit={createMentorProject}>
                    <h3><Plus size={16} /> New tracked project</h3>
                    <label htmlFor="mentorProjectName">Project name</label>
                    <input id="mentorProjectName" required minLength={2} maxLength={160} value={mentorProjectName} onChange={(e) => setMentorProjectName(e.target.value)} placeholder="Retail demand forecasting" />
                    <label htmlFor="mentorProjectIdea">Project idea</label>
                    <textarea id="mentorProjectIdea" required minLength={3} maxLength={2000} rows={3} value={mentorProjectIdea} onChange={(e) => setMentorProjectIdea(e.target.value)} placeholder="What are you building?" />
                    <button className="primary-button" type="submit">Create project <ArrowRight size={15} /></button>
                  </form>
                </aside>
                <div className="mentor-main-column">
                  <div className="quality-card mentor-chat-card">
                    <div className="quality-title"><div className="form-icon"><BrainCircuit size={22} /></div><div><h2>Conversational mentor</h2><p>{selectedProjectId ? "Project-aware guidance enabled" : "General academic guidance — select a project for tracking context"}</p></div></div>
                    <div className="mentor-messages" aria-live="polite">
                      {mentorMessages.map((item, index) => <div key={`${index}-${item.role}`} className={`mentor-message ${item.role}`}><span>{item.role === "assistant" ? "MENTOR" : "YOU"}</span><p>{item.content}</p></div>)}
                      {mentorLoading && <div className="mentor-message assistant"><span>MENTOR</span><p><LoaderCircle className="spin" size={15} /> Thinking through your next step…</p></div>}
                    </div>
                    <form className="mentor-chat-form" onSubmit={sendMentorMessage}>
                      <textarea value={mentorInput} onChange={(e) => setMentorInput(e.target.value)} rows={2} maxLength={4000} placeholder="Ask about your next task, blockers, progress, or viva…" />
                      <button className="primary-button" type="submit" disabled={mentorLoading || !mentorInput.trim()}><Send size={16} /> Send</button>
                    </form>
                  </div>
                  <div className="quality-card">
                    <div className="quality-title"><CalendarDays size={21} /><div><h2>Milestone tracker</h2><p>Update status as your work progresses</p></div></div>
                    {selectedProjectId ? <>
                      <form className="milestone-add-form" onSubmit={addMentorMilestone}>
                        <input required value={milestoneTitle} onChange={(e) => setMilestoneTitle(e.target.value)} maxLength={200} placeholder="New milestone (e.g. complete data cleaning)" />
                        <input type="date" value={milestoneDueDate} onChange={(e) => setMilestoneDueDate(e.target.value)} aria-label="Milestone due date" />
                        <button className="secondary-button" type="submit"><Plus size={15} /> Add</button>
                      </form>
                      {mentorProjects.find((p) => String(p.id) === String(selectedProjectId)) ? null : null}
                      <MentorMilestones projectId={selectedProjectId} onError={setMentorError} onStatusChange={changeMilestoneStatus} />
                    </> : <p className="muted-copy">Create or select a project to add and track milestones.</p>}
                  </div>
                </div>
              </div>
            </section>
          )}

          {activeSection === "documents" && (
            <section className="results-page">
              <div className="eyebrow"><FileText size={15} /> ACADEMIC DOCUMENT STUDIO</div>
              <h1>Project <span>documents</span></h1>
              <p className="page-description">Generate a synopsis, methodology, or progress report from a tracked project's saved idea, blueprint, and milestone records.</p>
              {documentError && <div className="error-box"><AlertTriangle size={18} />{documentError}</div>}
              <form className="generator-card" onSubmit={generateDocument}>
                <label htmlFor="documentProject">Tracked project</label>
                <select id="documentProject" value={documentProjectId} onChange={(e) => { setDocumentProjectId(e.target.value); setDocumentResult(null); }}>
                  <option value="">Select a project</option>
                  {mentorProjects.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
                </select>
                <label htmlFor="documentType" style={{ marginTop: 16 }}>Document type</label>
                <select id="documentType" value={documentType} onChange={(e) => setDocumentType(e.target.value)}>
                  <option value="synopsis">Project synopsis</option>
                  <option value="methodology">Methodology</option>
                  <option value="progress_report">Progress report</option>
                </select>
                <button className="primary-button submit-button" type="submit" disabled={documentLoading}>
                  {documentLoading ? <><LoaderCircle className="spin" size={17} /> Generating document…</> : <><Sparkles size={17} /> Generate document <ArrowRight size={16} /></>}
                </button>
                <button className="secondary-button" type="button" onClick={() => loadDocuments()}><RefreshCw size={15} /> Refresh saved documents</button>
              </form>
              {documentResult && <article className="result-card" style={{ marginTop: 18 }}>
                <div className="quality-title"><FileText size={21} /><div><h2>{documentResult.title}</h2><p>Saved document · {new Date(documentResult.created_at).toLocaleString()}</p></div></div>
                <a className="secondary-button" href={`${API_URL}/api/documents/${documentResult.id}/download`}><Download size={15} /> Download Markdown</a>
                <pre className="document-preview">{documentResult.content}</pre>
              </article>}
              <section className="quality-card" style={{ marginTop: 18 }}>
                <div className="quality-title"><BookOpen size={21} /><div><h2>Saved documents</h2><p>Previously generated files for the selected project</p></div></div>
                {documents.map((doc) => <div className="check-row" key={doc.id}><FileText size={16} /><span>{doc.title}</span><a href={`${API_URL}/api/documents/${doc.id}/download`}><Download size={15} /> Download</a></div>)}
                {!documents.length && <p className="muted-copy">Select a project and refresh to see saved documents.</p>}
              </section>
            </section>
          )}

          {activeSection === "faculty" && (
            <section className="results-page">
              <div className="eyebrow"><GraduationCap size={15} /> FACULTY WORKSPACE</div>
              <h1>Faculty <span>dashboard</span></h1>
              <p className="page-description">Monitor project health from recorded milestone statuses and deadlines. Access requires the faculty token configured by the project administrator.</p>
              <form className="generator-card" onSubmit={loadFacultyDashboard}>
                <label htmlFor="facultyToken">Faculty access token</label>
                <input id="facultyToken" type="password" autoComplete="current-password" value={facultyToken} onChange={(e) => setFacultyToken(e.target.value)} placeholder="Enter FACULTY_DASHBOARD_TOKEN" required />
                <button className="primary-button submit-button" type="submit" disabled={facultyLoading}>
                  {facultyLoading ? <><LoaderCircle className="spin" size={17} /> Loading dashboard…</> : <><RefreshCw size={17} /> Load faculty dashboard</>}
                </button>
              </form>
              {facultyError && <div className="error-box"><AlertTriangle size={18} />{facultyError}</div>}
              {facultyData && <>
                <div className="stats-grid" style={{ marginTop: 18 }}>
                  <Stat icon={Layers3} label="Projects" value={String(facultyData.total_projects)} detail="Tracked projects" />
                  <Stat icon={AlertTriangle} label="Needs attention" value={String(facultyData.needs_attention)} detail="Blocked or overdue" />
                  <Stat icon={CheckCircle2} label="Completed" value={String(facultyData.completed_projects)} detail="All milestones complete" />
                  <Stat icon={Activity} label="Average progress" value={`${facultyData.average_progress_percent}%`} detail="Across tracked projects" />
                </div>
                <section className="quality-card" style={{ marginTop: 18 }}>
                  <div className="quality-title"><Users size={21} /><div><h2>Student project health</h2><p>Generated {new Date(facultyData.generated_at).toLocaleString()}</p></div></div>
                  {facultyData.projects.map((p) => <article className="faculty-project" key={p.id}>
                    <div className="faculty-project-head"><div><h3>{p.name}</h3><p>{p.idea}</p></div><span className={`health-pill ${p.health}`}>{p.health.replaceAll("_", " ")}</span></div>
                    <div className="progress-track"><div className="progress-fill" style={{ width: `${p.progress_percent}%` }} /></div>
                    <div className="faculty-metrics"><span>{p.progress_percent}% complete</span><span>{p.completed_count}/{p.milestone_count} milestones</span><span>{p.blocked_count} blocked</span><span>{p.overdue_count} overdue</span></div>
                    <p className="faculty-summary">{p.summary}</p>
                  </article>)}
                  {!facultyData.projects.length && <p className="muted-copy">No tracked projects are available yet.</p>}
                  <p className="disclaimer">{facultyData.note}</p>
                </section>
              </>}
            </section>
          )}
        </div>
      </main>
    </div>
  );
}


function MentorMilestones({ projectId, onError, onStatusChange }) {
  const [milestones, setMilestones] = useState([]);
  useEffect(() => {
    let active = true;
    fetch(`${API_URL}/api/mentor/projects/${projectId}`)
      .then(async (response) => { const data = await response.json(); if (!response.ok) throw new Error(data.detail || "Unable to load milestones."); return data.project; })
      .then((project) => { if (active) setMilestones(project.milestones || []); })
      .catch((error) => { if (active) onError(error.message); });
    return () => { active = false; };
  }, [projectId, onError]);
  if (!milestones.length) return <p className="muted-copy">No milestones yet. Add the first milestone above.</p>;
  const completed = milestones.filter((m) => m.status === "completed").length;
  return <div className="milestone-list"><div className="milestone-progress"><span>{completed} of {milestones.length} completed</span><strong>{Math.round(completed / milestones.length * 100)}%</strong></div><div className="progress-track"><span style={{ width: `${completed / milestones.length * 100}%` }} /></div>{milestones.map((milestone) => <div className="milestone-row" key={milestone.id}><div className="milestone-copy"><strong>{milestone.title}</strong><span>{milestone.due_date ? `Due ${milestone.due_date}` : "No due date"}</span></div><select aria-label={`Status for ${milestone.title}`} value={milestone.status} onChange={(event) => onStatusChange(milestone.id, event.target.value)}><option value="pending">Pending</option><option value="in_progress">In progress</option><option value="blocked">Blocked</option><option value="completed">Completed</option></select></div>)}</div>;
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
