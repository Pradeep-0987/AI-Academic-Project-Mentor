import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowDownRight,
  ArrowLeft,
  ArrowRight,
  Bell,
  BookOpen,
  Bot,
  CalendarDays,
  Check,
  CheckCircle2,
  ChevronDown,
  CircleHelp,
  ClipboardList,
  Clock3,
  Cpu,
  FileText,
  FolderKanban,
  Gauge,
  GraduationCap,
  Layers3,
  LayoutDashboard,
  LoaderCircle,
  LogOut,
  MessageCircle,
  PanelLeftClose,
  PanelLeftOpen,
  Plus,
  Send,
  Settings,
  ShieldAlert,
  Sparkles,
  UserRound,
  UsersRound,
  X,
} from 'lucide-react';
import { NextstepMark } from '../components/common/NextstepLogo';
import { useOnboarding } from '../context/OnboardingContext';
import {
  createProject,
  generateProjectBlueprint,
  getProjectBlueprint,
  listProjects,
  saveStudentProfile,
  sendProjectMentorMessage,
  updateMilestoneStatus,
  DEPARTMENTS,
  SEMESTERS,
  GRADUATION_YEARS,
} from '../services/api';
import './Workspace.css';

const PROJECT_SECTIONS = [
  ['overview', 'Overview', LayoutDashboard],
  ['feasibility', 'Feasibility', Gauge],
  ['scope', 'Scope', ClipboardList],
  ['technology', 'Technology', Cpu],
  ['risk', 'Risk analysis', ShieldAlert],
  ['milestones', 'Weekly milestones', CalendarDays],
  ['monitor', 'NEXTSTEP AI Assistant', Bot],
];

const SUGGESTED_QUESTIONS = [
  'What should I complete this week?',
  'Which milestones are delayed?',
  'What are the major risks in my project?',
  'Help me prepare for my next project review.',
];

function routeInfo(path) {
  const projectMatch = path.match(/^\/projects\/([^/]+)(?:\/([^/]+))?/);
  if (path === '/projects/new') return { page: 'new-project' };
  if (projectMatch) return { page: projectMatch[2] || 'overview', projectId: projectMatch[1] };
  if (path === '/ai-monitor') return { page: 'monitor' };
  if (path === '/profile') return { page: 'profile' };
  if (path === '/settings') return { page: 'settings' };
  return { page: 'dashboard' };
}

function displayDate(value) {
  if (!value) return 'Not scheduled';
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime())
    ? 'Not scheduled'
    : parsed.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
}

function projectProgress(project) {
  return project?.progress || 0;
}

function listValue(value) {
  if (Array.isArray(value)) return value.filter(Boolean);
  if (typeof value === 'string' && value.trim()) return [value.trim()];
  return [];
}

function EmptyState({ title, text, action }) {
  return (
    <div className="ws-empty">
      <div className="ws-empty-icon"><FolderKanban size={22} /></div>
      <h2>{title}</h2>
      <p>{text}</p>
      {action}
    </div>
  );
}

function StatCard({ label, value, note, icon: Icon, tone = 'green' }) {
  return (
    <article className="ws-stat-card">
      <div className={`ws-stat-icon ${tone}`}><Icon size={19} /></div>
      <div className="ws-stat-label">{label}</div>
      <div className="ws-stat-value">{value}</div>
      <div className="ws-stat-note">{note}</div>
    </article>
  );
}

function SectionCard({ title, eyebrow, children, className = '' }) {
  return (
    <section className={`ws-card ${className}`}>
      <div className="ws-card-heading">
        <div>
          {eyebrow && <span className="ws-eyebrow">{eyebrow}</span>}
          <h2>{title}</h2>
        </div>
      </div>
      {children}
    </section>
  );
}

export default function Workspace() {
  const {
    currentUser,
    profile,
    updateProfileField,
    handleLogout,
  } = useOnboarding();
  const [route, setRoute] = useState(() => window.location.pathname);
  const [projects, setProjects] = useState([]);
  const [blueprint, setBlueprint] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [pageError, setPageError] = useState('');
  const [notice, setNotice] = useState('');
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('acad_theme') === 'dark');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => window.innerWidth <= 760);
  const [savingProfile, setSavingProfile] = useState(false);
  const info = routeInfo(route);
  const activeProject = useMemo(
    () => projects.find((project) => project.id === info.projectId) || null,
    [projects, info.projectId]
  );
  const selectedProjectId = info.projectId || projects[0]?.id;
  const selectedProject = projects.find((project) => project.id === selectedProjectId) || activeProject;

  const navigate = (path) => {
    if (window.location.pathname !== path) window.history.pushState(null, '', path);
    setRoute(path);
    setPageError('');
    setNotice('');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  useEffect(() => {
    const handlePopState = () => setRoute(window.location.pathname);
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  useEffect(() => {
    document.documentElement.dataset.theme = darkMode ? 'dark' : 'light';
    localStorage.setItem('acad_theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);

  useEffect(() => {
    let active = true;
    async function loadWorkspace() {
      setIsLoading(true);
      setPageError('');
      try {
        const list = await listProjects();
        if (!active) return;
        setProjects(list);
        const current = routeInfo(route);
        if (current.projectId && current.page !== 'monitor') {
          const project = list.find((item) => item.id === current.projectId);
          if (!project) {
            setPageError('This project could not be found in your account.');
            setBlueprint(null);
          } else {
            setBlueprint(await getProjectBlueprint(current.projectId));
          }
        } else {
          setBlueprint(null);
        }
      } catch (error) {
        if (active) setPageError(error.message);
      } finally {
        if (active) setIsLoading(false);
      }
    }
    loadWorkspace();
    return () => { active = false; };
  }, [route]);

  const refreshProjects = async () => {
    const list = await listProjects();
    setProjects(list);
  };

  const handleCreateProject = async (event) => {
    event.preventDefault();
    setPageError('');
    setIsLoading(true);
    const form = new FormData(event.currentTarget);
    const payload = {
      title: String(form.get('title') || '').trim(),
      description: String(form.get('description') || '').trim(),
      domain: String(form.get('domain') || '').trim(),
      department: String(form.get('department') || '').trim(),
      technology_stack: String(form.get('technology_stack') || '').trim(),
      duration_weeks: Number(form.get('duration_weeks')),
      team_size: form.get('team_size') ? Number(form.get('team_size')) : null,
      guide_name: String(form.get('guide_name') || '').trim() || null,
    };
    try {
      const project = await createProject(payload);
      await refreshProjects();
      navigate(`/projects/${project.id}/overview`);
    } catch (error) {
      setPageError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const setMilestone = async (week, status) => {
    if (!selectedProjectId) return;
    setPageError('');
    try {
      const updated = await updateMilestoneStatus(selectedProjectId, week, status);
      setBlueprint(updated);
      await refreshProjects();
    } catch (error) {
      setPageError(error.message);
    }
  };

  const regenerateBlueprint = async () => {
    if (!selectedProjectId) return;
    setPageError('');
    setIsLoading(true);
    try {
      const generated = await generateProjectBlueprint(selectedProjectId);
      setBlueprint(generated);
      await refreshProjects();
    } catch (error) {
      setPageError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveProfile = async (event) => {
    event.preventDefault();
    setSavingProfile(true);
    setPageError('');
    try {
      await saveStudentProfile(profile);
      setNotice('Your academic profile has been saved.');
    } catch (error) {
      setPageError(error.message);
    } finally {
      setSavingProfile(false);
    }
  };

  const pageTitle = info.page === 'dashboard' ? 'Dashboard'
    : info.page === 'new-project' ? 'Create a project'
      : info.page === 'profile' ? 'Your profile'
        : info.page === 'settings' ? 'Settings'
          : info.page === 'monitor' ? 'NEXTSTEP AI Assistant'
            : PROJECT_SECTIONS.find(([id]) => id === info.page)?.[1] || 'Project';

  useEffect(() => {
    const title = info.projectId && activeProject
      ? `${pageTitle} · ${activeProject.title}`
      : pageTitle;
    document.title = `NEXTSTEP AI | ${title}`;
  }, [pageTitle, info.projectId, activeProject]);

  const activeProjects = projects.filter((project) => project.status !== 'completed');
  const completedProjects = projects.filter((project) => project.status === 'completed');
  const pendingMilestones = projects.reduce(
    (total, project) => total + Math.max((project.total_milestones || 0) - (project.milestones_completed || 0), 0),
    0
  );
  const delayedMilestones = projects.reduce((total, project) => total + (project.delayed_milestones || 0), 0);
  const totalProgress = projects.length
    ? Math.round(projects.reduce((sum, project) => sum + projectProgress(project), 0) / projects.length)
    : 0;

  return (
    <div className={`ws-shell${sidebarCollapsed ? ' sidebar-collapsed' : ''}`}>
      <aside className="ws-sidebar" id="workspace-sidebar" aria-label="Workspace navigation">
        <button className="ws-brand" onClick={() => navigate('/dashboard')} aria-label="Go to dashboard">
          <NextstepMark size={39} className="ws-brand-mark" />
          <span><strong>NEXTSTEP AI</strong><small>ACADEMIC PROJECT STUDIO</small></span>
        </button>
        <button className="ws-sidebar-inline-toggle" type="button" onClick={() => setSidebarCollapsed(true)} aria-label="Close navigation">
          <X size={18} />
        </button>
        <div className="ws-nav-label">Workspace</div>
        <nav className="ws-nav" aria-label="Main navigation">
          <button className={info.page === 'dashboard' ? 'active' : ''} onClick={() => navigate('/dashboard')} title="Dashboard" aria-label="Dashboard">
            <LayoutDashboard size={18} /> Dashboard
          </button>
          <button className={info.projectId ? 'active' : ''} onClick={() => navigate(projects[0] ? `/projects/${projects[0].id}/overview` : '/dashboard')} title="My projects">
            <BookOpen size={18} /> My projects
          </button>
          <button className={info.page === 'new-project' ? 'active' : ''} onClick={() => navigate('/projects/new')} title="Create project" aria-label="Create project">
            <FolderKanban size={18} /> Create project
          </button>
          <button
            className={info.projectId && info.page !== 'milestones' && info.page !== 'monitor' ? 'active' : ''}
            onClick={() => navigate(projects[0] ? `/projects/${selectedProjectId || projects[0].id}/overview` : '/projects/new')}
            title="Project blueprint"
            aria-label="Project blueprint"
          >
            <FileText size={18} /> Project blueprint
          </button>
          <button
            className={info.page === 'milestones' ? 'active' : ''}
            onClick={() => navigate(projects[0] ? `/projects/${selectedProjectId || projects[0].id}/milestones` : '/projects/new')}
            title="Weekly milestones"
            aria-label="Weekly milestones"
          >
            <CalendarDays size={18} /> Weekly milestones
          </button>
          <button className={info.page === 'monitor' ? 'active' : ''} onClick={() => navigate('/ai-monitor')} title="NEXTSTEP AI Assistant" aria-label="NEXTSTEP AI Assistant">
            <Bot size={18} /> NEXTSTEP AI Assistant <span className="ws-nav-new">AI</span>
          </button>
        </nav>
        {projects.length > 0 && (
          <>
            <div className="ws-nav-label ws-project-label">Your projects</div>
            <nav className="ws-nav ws-project-nav" aria-label="Your projects">
              {projects.slice(0, 5).map((project) => (
                <button
                  key={project.id}
                  className={info.projectId === project.id ? 'active' : ''}
                  onClick={() => navigate(`/projects/${project.id}/overview`)}
                  title={project.title}
                >
                  <span className="ws-project-dot" /> <span className="ws-nav-project-name">{project.title}</span>
                </button>
              ))}
            </nav>
          </>
        )}
        <div className="ws-sidebar-bottom">
          <button className={info.page === 'profile' ? 'active' : ''} onClick={() => navigate('/profile')} title="Profile" aria-label="Profile">
            <UserRound size={18} /> Profile
          </button>
          <button className={info.page === 'settings' ? 'active' : ''} onClick={() => navigate('/settings')} title="Settings" aria-label="Settings">
            <Settings size={18} /> Settings
          </button>
          <div className="ws-user-card">
            <span className="ws-user-avatar">{(currentUser?.name || 'S').slice(0, 1).toUpperCase()}</span>
            <span className="ws-user-text"><strong>{currentUser?.name || 'Student'}</strong><small>Student account</small></span>
            <button onClick={handleLogout} aria-label="Log out" title="Log out"><LogOut size={17} /></button>
          </div>
        </div>
      </aside>

      <main className="ws-main">
        <header className="ws-topbar">
          <div className="ws-topbar-leading">
            <button
              className="ws-sidebar-toggle"
              type="button"
              onClick={() => setSidebarCollapsed((value) => !value)}
              aria-expanded={!sidebarCollapsed}
              aria-controls="workspace-sidebar"
              aria-label={sidebarCollapsed ? 'Expand navigation' : 'Collapse navigation'}
              title={sidebarCollapsed ? 'Expand navigation' : 'Collapse navigation'}
            >
              {sidebarCollapsed ? <PanelLeftOpen size={18} /> : <PanelLeftClose size={18} />}
            </button>
            <div className="ws-breadcrumb">
            <span>Workspace</span><ArrowRight size={14} /><strong>{pageTitle}</strong>
            </div>
          </div>
          <div className="ws-top-actions">
            <span className="ws-icon-button" aria-hidden="true"><Bell size={18} /></span>
            <button className="ws-primary-button ws-top-create" onClick={() => navigate('/projects/new')}>
              <Plus size={17} /> New project
            </button>
          </div>
        </header>

        <div className="ws-content">
          {pageError && (
            <div className="ws-alert ws-alert-error" role="alert">
              <CircleHelp size={18} /> <span>{pageError}</span>
              <button onClick={() => setPageError('')} aria-label="Dismiss error"><X size={16} /></button>
            </div>
          )}
          {notice && <div className="ws-alert ws-alert-success"><CheckCircle2 size={18} />{notice}</div>}
          {isLoading && info.page !== 'new-project' && info.page !== 'profile' && info.page !== 'settings' ? (
            <div className="ws-loading"><LoaderCircle className="ws-spin" size={24} /> Loading your workspace…</div>
          ) : (
            <>
              {info.page === 'dashboard' && (
                <DashboardPage
                  projects={projects}
                  activeProjects={activeProjects}
                  completedProjects={completedProjects}
                  pendingMilestones={pendingMilestones}
                  delayedMilestones={delayedMilestones}
                  totalProgress={totalProgress}
                  navigate={navigate}
                  firstName={(currentUser?.name || 'Student').split(' ')[0]}
                />
              )}
              {info.page === 'new-project' && (
                <CreateProjectPage onSubmit={handleCreateProject} loading={isLoading} navigate={navigate} />
              )}
              {PROJECT_SECTIONS.some(([id]) => id === info.page && id !== 'monitor') && (
                selectedProject ? (
                  <ProjectPage
                    page={info.page}
                    project={selectedProject}
                    blueprint={blueprint}
                    navigate={navigate}
                    onMilestoneChange={setMilestone}
                    onGenerateBlueprint={regenerateBlueprint}
                    onError={setPageError}
                  />
                ) : (
                  <EmptyState
                    title="No project selected"
                    text="Create a project to generate your personalized blueprint and weekly plan."
                    action={<button className="ws-primary-button" onClick={() => navigate('/projects/new')}><Plus size={17} /> Create project</button>}
                  />
                )
              )}
              {info.page === 'monitor' && (
                <MonitorPage
                  key={selectedProject?.id || 'no-project'}
                  project={selectedProject}
                  projects={projects}
                  onSelect={(id) => navigate(`/projects/${id}/monitor`)}
                  onError={setPageError}
                />
              )}
              {info.page === 'profile' && (
                <ProfilePage
                  profile={profile}
                  updateProfileField={updateProfileField}
                  saving={savingProfile}
                  onSubmit={handleSaveProfile}
                />
              )}
              {info.page === 'settings' && (
                <SettingsPage darkMode={darkMode} onToggle={() => setDarkMode((value) => !value)} />
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}

function DashboardPage({
  projects,
  activeProjects,
  completedProjects,
  pendingMilestones,
  delayedMilestones,
  totalProgress,
  navigate,
  firstName,
}) {
  const recent = [...projects].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).slice(0, 4);
  const upcoming = [...projects]
    .filter((project) => project.next_deadline)
    .sort((a, b) => new Date(a.next_deadline) - new Date(b.next_deadline))
    .slice(0, 4);

  return (
    <>
      <section className="ws-dashboard-hero">
        <div className="ws-dashboard-hero-copy">
          <span className="ws-eyebrow">Every Step Builds Success.</span>
          <h1>Welcome to NEXTSTEP AI</h1>
          <p className="ws-dashboard-personal">Good to see you, {firstName}.</p>
          <p>Your ideas deserve a smarter path to success. Plan, build, and track your academic projects with AI-powered guidance.</p>
          <button className="ws-primary-button" onClick={() => navigate('/projects/new')}><Plus size={17} /> Create project</button>
        </div>
        <img src="/nextstep-hero.svg" alt="" aria-hidden="true" />
      </section>
      {projects.length === 0 ? (
        <EmptyState
          title="Start with your first project"
          text="Add your project details and duration. Your AI-assisted blueprint and week-by-week milestones will be generated from them."
          action={<button className="ws-primary-button" onClick={() => navigate('/projects/new')}><Plus size={17} /> Create your project</button>}
        />
      ) : (
        <>
          <div className="ws-stats-grid">
            <StatCard label="Total projects" value={projects.length} note="In your workspace" icon={FolderKanban} />
            <StatCard label="Active projects" value={activeProjects.length} note="Currently underway" icon={Layers3} tone="blue" />
            <StatCard label="Completed projects" value={completedProjects.length} note="Marked complete" icon={CheckCircle2} tone="violet" />
            <StatCard label="Pending milestones" value={pendingMilestones} note="Not yet completed" icon={Clock3} tone="blue" />
            <StatCard label="Delayed milestones" value={delayedMilestones} note="Past their target date" icon={CalendarDays} tone={delayedMilestones ? 'orange' : 'green'} />
            <StatCard label="Overall progress" value={`${totalProgress}%`} note="Across all your projects" icon={Gauge} tone="violet" />
          </div>
          <div className="ws-dashboard-grid">
            <SectionCard title="Project progress" eyebrow="OVERVIEW" className="ws-progress-card">
              <div className="ws-progress-summary">
                <span className="ws-progress-number">{totalProgress}%</span>
                <span className="ws-progress-caption">Average completion<br />based on completed milestones</span>
                <span className="ws-progress-change"><ArrowDownRight size={15} /> Live data</span>
              </div>
              <div className="ws-chart" role="img" aria-label="Project completion percentages">
                {projects.slice(0, 8).map((project) => (
                  <div className="ws-chart-column" key={project.id}>
                    <span className="ws-chart-value">{projectProgress(project)}%</span>
                    <div className="ws-chart-track"><div style={{ height: `${projectProgress(project)}%` }} /></div>
                    <span className="ws-chart-label" title={project.title}>{project.title}</span>
                  </div>
                ))}
              </div>
            </SectionCard>
            <SectionCard title="Upcoming deadlines" eyebrow="YOUR SCHEDULE">
              {upcoming.length ? (
                <div className="ws-deadline-list">
                  {upcoming.map((project) => (
                    <button className="ws-deadline-row" key={project.id} onClick={() => navigate(`/projects/${project.id}/milestones`)}>
                      <span className="ws-deadline-date">{displayDate(project.next_deadline).split(',')[0]}</span>
                      <span className="ws-deadline-copy"><strong>{project.next_milestone || project.title}</strong><small>{project.title}</small></span>
                      <ArrowRight size={16} />
                    </button>
                  ))}
                </div>
              ) : (
                <p className="ws-muted-copy">Upcoming milestone dates will appear here when your project plans are ready.</p>
              )}
            </SectionCard>
          </div>
          <SectionCard title="Recent activity" eyebrow="YOUR PROJECTS" className="ws-project-list-card">
            <div className="ws-project-table">
              <div className="ws-project-table-head"><span>Project</span><span>Duration</span><span>Progress</span><span>Status</span><span /></div>
              {recent.map((project) => (
                <button className="ws-project-row" key={project.id} onClick={() => navigate(`/projects/${project.id}/overview`)}>
                  <span className="ws-project-cell-title"><span className="ws-project-icon"><BookOpen size={17} /></span><span><strong>{project.title}</strong><small>{project.domain || project.department || 'Academic project'}</small></span></span>
                  <span>{project.duration_weeks} weeks</span>
                  <span className="ws-table-progress"><span className="ws-mini-track"><i style={{ width: `${projectProgress(project)}%` }} /></span>{projectProgress(project)}%</span>
                  <span><span className={`ws-status-pill ${project.status === 'completed' ? 'complete' : 'active'}`}>{project.status === 'completed' ? 'Completed' : 'Active'}</span></span>
                  <ArrowRight size={17} />
                </button>
              ))}
            </div>
          </SectionCard>
          <div className="ws-dashboard-bottom-grid">
            <SectionCard title="Weekly milestone timeline" eyebrow="NEXT UP" className="ws-timeline-card">
              {upcoming.length ? (
                <div className="ws-weekly-timeline">
                  {upcoming.slice(0, 4).map((project, index) => (
                    <button className="ws-timeline-item" key={project.id} onClick={() => navigate(`/projects/${project.id}/milestones`)}>
                      <span className="ws-timeline-marker">{index === 0 ? <span /> : null}</span>
                      <span className="ws-timeline-date">{displayDate(project.next_deadline)}</span>
                      <span className="ws-timeline-copy"><strong>{project.next_milestone || 'Next milestone'}</strong><small>{project.title}</small></span>
                      <ArrowRight size={16} />
                    </button>
                  ))}
                </div>
              ) : (
                <p className="ws-muted-copy">Milestones with upcoming dates will appear here as your project plans are generated.</p>
              )}
            </SectionCard>
            <section className="ws-ai-quick-card">
              <span className="ws-ai-quick-icon"><Bot size={21} /></span>
              <span className="ws-eyebrow">YOUR PROJECT COPILOT</span>
              <h2>Need a clear next step?</h2>
              <p>Ask NEXTSTEP AI about your milestones, project risks, or what to focus on next.</p>
              <button className="ws-ai-quick-action" onClick={() => navigate('/ai-monitor')}>Open AI Assistant <ArrowRight size={16} /></button>
              <span className="ws-ai-orbit orbit-one" />
              <span className="ws-ai-orbit orbit-two" />
            </section>
          </div>
        </>
      )}
    </>
  );
}

function CreateProjectPage({ onSubmit, loading, navigate }) {
  const formRef = useRef(null);
  const stepRefs = useRef([]);
  const [activeStep, setActiveStep] = useState(0);
  const [review, setReview] = useState({});
  const steps = [
    { title: 'Project Information', description: 'Give your project a clear title and explain the problem you want to solve.', icon: FileText },
    { title: 'Academic Information', description: 'Connect your project to your study area.', icon: GraduationCap },
    { title: 'Technology Stack', description: 'Choose the tools you plan to use; your blueprint can suggest alternatives.', icon: Cpu },
    { title: 'Duration & Team', description: 'Set the number of weeks so your milestones fit your schedule.', icon: CalendarDays },
    { title: 'Review & Generate', description: 'Check the details before generating your personalized blueprint.', icon: Sparkles },
  ];
  const expectedMilestones = Math.min(52, Math.max(0, Number(review.duration_weeks) || 0));
  const reviewItems = [
    ['Project title', review.title],
    ['Description', review.description],
    ['Domain', review.domain],
    ['Department', review.department],
    ['Technology stack', review.technology_stack],
    ['Duration', review.duration_weeks ? `${review.duration_weeks} weeks` : ''],
    ['Expected milestones', expectedMilestones ? `${expectedMilestones} weekly milestones` : ''],
    ['Team size', review.team_size ? `${review.team_size} members` : 'Not specified'],
    ['Guide / mentor', review.guide_name || 'Not specified'],
  ];

  const nextStep = () => {
    const invalidField = stepRefs.current[activeStep]?.querySelector(':invalid');
    if (invalidField) {
      invalidField.reportValidity();
      return;
    }
    if (activeStep === 3 && formRef.current) {
      setReview(Object.fromEntries(new FormData(formRef.current).entries()));
    }
    setActiveStep((step) => Math.min(step + 1, steps.length - 1));
  };

  const handleSubmit = (event) => {
    if (activeStep !== steps.length - 1) {
      event.preventDefault();
      nextStep();
      return;
    }
    onSubmit(event);
  };

  return (
    <>
      <button className="ws-back-link ws-create-back" type="button" onClick={() => navigate('/dashboard')}><ArrowLeft size={16} /> Back to workspace</button>
      <section className="ws-create-hero">
        <div className="ws-create-hero-copy">
          <span className="ws-create-eyebrow"><Sparkles size={14} /> PROJECT WORKSPACE</span>
          <h1>Bring Your Next Big Idea to Life.</h1>
          <p>Create your project, define your timeline, and let NEXTSTEP AI build your intelligent project blueprint.</p>
          <div className="ws-create-hero-points">
            <span><CheckCircle2 size={15} /> A plan shaped around your goals</span>
            <span><CalendarDays size={15} /> Weekly milestones that fit your timeline</span>
          </div>
        </div>
        <img src="/nextstep-hero.svg" alt="" aria-hidden="true" />
        <span className="ws-create-hero-glow" />
      </section>
      <form ref={formRef} className="ws-card ws-project-form ws-wizard" onSubmit={handleSubmit} noValidate>
        <ol className="ws-wizard-progress" aria-label="Project creation steps">
          {steps.map(({ title, icon: Icon }, index) => (
            <li key={title} className={index === activeStep ? 'current' : index < activeStep ? 'complete' : ''}>
              <button type="button" onClick={() => index < activeStep && setActiveStep(index)} disabled={loading || index >= activeStep} aria-current={index === activeStep ? 'step' : undefined}>
                <span className="ws-wizard-step-icon">{index < activeStep ? <Check size={16} /> : <Icon size={16} />}</span>
                <span className="ws-wizard-step-label"><small>STEP {index + 1}</small><strong>{title}</strong></span>
              </button>
            </li>
          ))}
        </ol>
        <div className="ws-wizard-progress-track"><span style={{ width: `${((activeStep + 1) / steps.length) * 100}%` }} /></div>
        {steps.slice(0, 4).map(({ title, description, icon: Icon }, index) => (
          <section
            className="ws-wizard-panel"
            hidden={activeStep !== index}
            key={title}
            ref={(element) => { stepRefs.current[index] = element; }}
            aria-labelledby={`ws-wizard-heading-${index}`}
          >
            <div className="ws-wizard-heading">
              <span className={`ws-form-section-icon ${index === 3 ? 'blue' : ''}`}><Icon size={20} /></span>
              <div><h2 id={`ws-wizard-heading-${index}`}>{title}</h2><p>{description}</p></div>
            </div>
            {index === 0 && (
              <>
                <label className="ws-field"><span>Project title <b>*</b></span><input name="title" required minLength="2" maxLength="200" placeholder="e.g. Smart Campus Energy Monitor" /></label>
                <label className="ws-field"><span>Description <b>*</b></span><textarea name="description" required minLength="20" maxLength="5000" rows="4" placeholder="Describe the problem, who it affects, and what you plan to create." /></label>
              </>
            )}
            {index === 1 && (
              <div className="ws-form-two">
                <label className="ws-field"><span>Domain <b>*</b></span><input name="domain" required maxLength="1000" placeholder="e.g. Healthcare, Education, Agriculture" /></label>
                <label className="ws-field"><span>Department <b>*</b></span><select name="department" required defaultValue=""><option value="" disabled>Select department</option>{DEPARTMENTS.map((department) => <option key={department}>{department}</option>)}</select></label>
              </div>
            )}
            {index === 2 && (
              <label className="ws-field"><span>Technology stack <b>*</b></span><input name="technology_stack" required maxLength="1000" placeholder="e.g. React, FastAPI, PostgreSQL, PyTorch" /><small>Separate technologies with commas. Your AI blueprint can also suggest alternatives.</small></label>
            )}
            {index === 3 && (
              <>
                <label className="ws-field ws-duration-field"><span>Project duration (weeks) <b>*</b></span><input name="duration_weeks" type="number" required min="1" max="52" step="1" placeholder="e.g. 10" /><small>Choose between 1 and 52 weeks. Your plan will include one milestone per week.</small></label>
                <div className="ws-form-subheading"><UsersRound size={17} /><div><h3>Team information</h3><p>These details are optional and can be added later.</p></div></div>
                <div className="ws-form-two">
                  <label className="ws-field"><span>Team size <em>Optional</em></span><input name="team_size" type="number" min="1" max="20" step="1" placeholder="Leave blank if not decided" /></label>
                  <label className="ws-field"><span>Guide / mentor name <em>Optional</em></span><input name="guide_name" maxLength="255" placeholder="Add your project guide, if assigned" /></label>
                </div>
              </>
            )}
          </section>
        ))}
        <section className="ws-wizard-panel ws-review-panel" hidden={activeStep !== 4} aria-labelledby="ws-wizard-heading-review">
          <div className="ws-wizard-heading">
            <span className="ws-form-section-icon"><Sparkles size={20} /></span>
            <div><h2 id="ws-wizard-heading-review">Review your project</h2><p>Make sure everything looks right before you generate your blueprint.</p></div>
          </div>
          <dl className="ws-review-grid">
            {reviewItems.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value || 'Not provided'}</dd></div>)}
          </dl>
          <p className="ws-review-note"><Sparkles size={16} /> NEXTSTEP AI will use these details to create a tailored blueprint and weekly milestone plan.</p>
        </section>
        <div className="ws-form-footer ws-wizard-footer">
          <span>{activeStep === 4 ? <><Sparkles size={16} /> {expectedMilestones} milestone{expectedMilestones === 1 ? '' : 's'} will be planned.</> : <>Step {activeStep + 1} of {steps.length}</>}</span>
          <div>
            {activeStep > 0 && <button className="ws-secondary-button" type="button" onClick={() => setActiveStep((step) => step - 1)} disabled={loading}><ArrowLeft size={16} /> Back</button>}
            {activeStep < steps.length - 1 ? (
              <button className="ws-primary-button" type="button" onClick={nextStep}>Continue <ArrowRight size={16} /></button>
            ) : (
              <button className="ws-primary-button ws-generate-button" type="submit" disabled={loading}>{loading ? <LoaderCircle className="ws-spin" size={17} /> : <Sparkles size={17} />}{loading ? 'Generating your AI blueprint…' : 'Generate My AI Blueprint'}</button>
            )}
          </div>
        </div>
      </form>
    </>
  );
}

function ProjectPage({ page, project, blueprint, navigate, onMilestoneChange, onGenerateBlueprint }) {
  const sectionName = PROJECT_SECTIONS.find(([id]) => id === page)?.[1] || 'Project overview';
  const milestones = blueprint?.planning?.weekly_milestones || [];
  const progress = project.progress || 0;

  return (
    <>
      <div className="ws-page-heading ws-project-heading">
        <div>
          <span className="ws-eyebrow">{sectionName.toUpperCase()}</span>
          <h1>{page === 'overview' ? project.title : sectionName}</h1>
          <p>{page === 'overview' ? project.description : project.title}</p>
        </div>
        <button className="ws-secondary-button" onClick={() => navigate(`/projects/${project.id}/monitor`)}><Bot size={17} /> Ask NEXTSTEP AI</button>
      </div>
      <nav className="ws-project-tabs" aria-label="Project blueprint pages">
        {PROJECT_SECTIONS.map(([id, label, Icon]) => (
          <button className={page === id ? 'selected' : ''} key={id} onClick={() => navigate(`/projects/${project.id}/${id}`)}><Icon size={16} />{label}</button>
        ))}
      </nav>
      {!blueprint && page !== 'overview' ? (
        <EmptyState
          title="Blueprint is not available"
          text="The AI blueprint could not be generated for this project. Try again to generate it from your project details."
          action={<button className="ws-primary-button" onClick={onGenerateBlueprint}><Sparkles size={16} /> Generate blueprint</button>}
        />
      ) : (
        <>
          {!blueprint && page === 'overview' && <div className="ws-alert ws-alert-error"><CircleHelp size={18} /><span>Project blueprint is unavailable.</span><button className="ws-primary-button" onClick={onGenerateBlueprint}><Sparkles size={15} /> Generate blueprint</button></div>}
          {page === 'overview' && <ProjectOverview project={project} blueprint={blueprint} milestones={milestones} progress={progress} navigate={navigate} />}
          {page === 'feasibility' && <FeasibilityPage data={blueprint?.feasibility} />}
          {page === 'scope' && <ScopePage data={blueprint?.scope} feasibility={blueprint?.feasibility} />}
          {page === 'technology' && <TechnologyPage data={blueprint?.technology} project={project} />}
          {page === 'risk' && <RiskPage data={blueprint?.risk} />}
          {page === 'milestones' && <MilestonesPage project={project} milestones={milestones} onMilestoneChange={onMilestoneChange} />}
        </>
      )}
    </>
  );
}

function ProjectOverview({ project, blueprint, milestones, progress, navigate }) {
  const due = milestones.find((milestone) => milestone.status !== 'completed');
  const scope = blueprint?.scope || {};
  return (
    <>
      <div className="ws-overview-grid">
        <SectionCard title="Project overview" eyebrow="PROJECT BRIEF" className="ws-overview-main">
          <p className="ws-description-copy">{project.description}</p>
          <div className="ws-info-grid">
            <InfoItem icon={Layers3} label="Domain" value={project.domain || 'Not specified'} />
            <InfoItem icon={GraduationCap} label="Department" value={project.department || 'Not specified'} />
            <InfoItem icon={CalendarDays} label="Duration" value={`${project.duration_weeks} weeks`} />
            <InfoItem icon={UsersRound} label="Team size" value={project.team_size ? `${project.team_size} members` : 'Not specified'} />
            <InfoItem icon={UserRound} label="Project guide" value={project.guide_name || 'Not assigned'} />
            <InfoItem icon={Cpu} label="Technologies" value={project.technology_stack || 'See recommended stack'} />
          </div>
        </SectionCard>
        <SectionCard title="Project health" eyebrow="LIVE PROGRESS">
          <div className="ws-health-number">{progress}<span>%</span></div>
          <div className="ws-progress-track"><i style={{ width: `${progress}%` }} /></div>
          <p className="ws-muted-copy">{project.milestones_completed} of {project.total_milestones} milestones completed.</p>
          <div className="ws-health-next"><span className="ws-next-icon"><Clock3 size={17} /></span><span><small>Next milestone</small><strong>{due?.milestone_title || (milestones.length ? 'All milestones complete' : 'Plan unavailable')}</strong></span></div>
          <button className="ws-inline-link" onClick={() => navigate(`/projects/${project.id}/milestones`)}>Open weekly plan <ArrowRight size={15} /></button>
        </SectionCard>
      </div>
      <SectionCard title="Project objectives" eyebrow="SCOPE PREVIEW">
        <ListItems items={listValue(scope.project_objective)} empty="Objectives will be available in the project scope." />
        <button className="ws-inline-link ws-card-link" onClick={() => navigate(`/projects/${project.id}/scope`)}>Explore full scope <ArrowRight size={15} /></button>
      </SectionCard>
    </>
  );
}

function InfoItem({ icon: Icon, label, value }) {
  return <div className="ws-info-item"><span><Icon size={16} /></span><div><small>{label}</small><strong>{value}</strong></div></div>;
}

function ListItems({ items, empty }) {
  return items.length ? (
    <ul className="ws-list-items">{items.map((item, index) => <li key={`${item}-${index}`}><Check size={16} />{item}</li>)}</ul>
  ) : <p className="ws-muted-copy">{empty}</p>;
}

function FeasibilityPage({ data = {} }) {
  const cards = [
    { title: 'Technical feasibility', score: data.feasibility || 'Not rated', detail: data.reasoning, tone: 'green' },
    { title: 'Economic feasibility', score: data.economic_feasibility || 'Review resources', detail: data.economic_reasoning || 'Consider hosting, software, hardware, and data costs within your project budget.', tone: 'blue' },
    { title: 'Operational feasibility', score: data.operational_feasibility || 'Review workflow', detail: data.operational_reasoning || 'Validate that intended users can adopt the solution in the planned environment.', tone: 'violet' },
  ];
  return (
    <>
      <div className="ws-triple-grid">{cards.map((card) => <section className="ws-card ws-feasibility-card" key={card.title}><span className={`ws-feasibility-badge ${card.tone}`}>{card.score}</span><h2>{card.title}</h2><p>{card.detail || 'No detailed assessment was returned in the blueprint.'}</p></section>)}</div>
      <SectionCard title="Required resources" eyebrow="WHAT YOU'LL NEED"><ListItems items={listValue(data.required_resources)} empty="No specific resources were listed in this feasibility assessment." /></SectionCard>
      <SectionCard title="Potential challenges" eyebrow="PLAN AHEAD"><ListItems items={listValue(data.potential_challenges)} empty="No challenges were listed in this assessment." /></SectionCard>
    </>
  );
}

function ScopePage({ data = {}, feasibility = {} }) {
  return (
    <>
      <SectionCard title="Problem statement" eyebrow="WHY THIS PROJECT">
        <p className="ws-prose">{feasibility.problem_statement || 'A problem statement was not provided in this blueprint.'}</p>
      </SectionCard>
      <SectionCard title="Proposed solution" eyebrow="HOW YOU'LL ADDRESS IT">
        <p className="ws-prose">{data.proposed_solution || 'A proposed solution was not provided in this blueprint.'}</p>
      </SectionCard>
      <SectionCard title="Project objectives" eyebrow="WHAT SUCCESS LOOKS LIKE"><ListItems items={listValue(data.project_objective)} empty="No project objectives were returned." /></SectionCard>
      <SectionCard title="In-scope features" eyebrow="DELIVERABLES"><ListItems items={[...listValue(data.mvp_features), ...listValue(data.functional_requirements)]} empty="No in-scope features were returned." /></SectionCard>
      <SectionCard title="Out of scope" eyebrow="BOUNDARIES"><ListItems items={listValue(data.out_of_scope)} empty="No out-of-scope items were returned." /></SectionCard>
      <SectionCard title="Expected outcomes" eyebrow="EVALUATION"><ListItems items={[...listValue(data.deliverables), ...listValue(data.success_criteria)]} empty="No expected outcomes were returned." /></SectionCard>
    </>
  );
}

function TechnologyPage({ data = {}, project }) {
  const groups = [
    ['Selected stack', listValue(project.technology_stack)],
    ['Frontend architecture', listValue(data.frontend)],
    ['Backend architecture', listValue(data.backend)],
    ['Database', listValue(data.database)],
    ['AI / ML technologies', listValue(data.ai_ml)],
    ['Deployment', listValue(data.deployment)],
    ['Development tools', listValue(data.development_tools)],
  ];
  const architecture = [
    ['Experience', listValue(data.frontend)],
    ['Application', listValue(data.backend)],
    ['Data', listValue(data.database)],
    ['Intelligence', listValue(data.ai_ml)],
  ].filter(([, technologies]) => technologies.length);
  return (
    <>
      <SectionCard title="Architecture rationale" eyebrow="SYSTEM DESIGN"><p className="ws-prose">{data.rationale || data.reasoning || 'No architecture rationale was provided.'}</p></SectionCard>
      {architecture.length > 0 && (
        <SectionCard title="Architecture at a glance" eyebrow="SYSTEM MAP">
          <div className="ws-architecture-flow" role="img" aria-label="Project technology layers">
            {architecture.map(([layer, technologies], index) => (
              <React.Fragment key={layer}>
                {index > 0 && <ArrowRight className="ws-architecture-arrow" size={18} />}
                <div className="ws-architecture-layer">
                  <small>{layer}</small>
                  <div>{technologies.map((technology) => <span className="ws-technology-badge" key={technology}>{technology}</span>)}</div>
                </div>
              </React.Fragment>
            ))}
          </div>
        </SectionCard>
      )}
      <div className="ws-tech-grid">{groups.map(([title, items]) => <section className="ws-card ws-tech-card" key={title}><span className="ws-tech-icon"><Cpu size={18} /></span><h2>{title}</h2><ListItems items={items} empty="No recommendations provided." /></section>)}</div>
      <SectionCard title="Alternatives &amp; limitations" eyebrow="TRADE-OFFS"><div className="ws-form-two"><div><h3>Alternatives</h3><ListItems items={listValue(data.alternatives)} empty="No alternatives listed." /></div><div><h3>Known limitations</h3><ListItems items={listValue(data.limitations)} empty="No limitations listed." /></div></div></SectionCard>
    </>
  );
}

function RiskPage({ data = {} }) {
  const risks = data.risks || [];
  return risks.length ? (
    <div className="ws-risk-list">{risks.map((risk, index) => (
      <article className="ws-card ws-risk-card" key={`${risk.risk}-${index}`}>
        <div className="ws-risk-title"><span className={`ws-severity ${String(risk.impact || risk.likelihood).toLowerCase()}`}><ShieldAlert size={16} />{risk.impact || risk.likelihood || 'Unrated'} impact</span><h2>{risk.risk}</h2></div>
        <div className="ws-form-two ws-risk-details"><div><h3>Mitigation strategy</h3><p>{risk.mitigation || 'No mitigation strategy was provided.'}</p></div><div><h3>Contingency plan</h3><p>{risk.contingency_plan || 'No contingency plan was provided.'}</p></div></div>
      </article>
    ))}</div>
  ) : <EmptyState title="No risk analysis found" text="The current project blueprint does not include any risk entries." />;
}

function MilestonesPage({ project, milestones, onMilestoneChange }) {
  if (!milestones.length) return <EmptyState title="Weekly plan unavailable" text="This project's blueprint has no weekly milestones yet." />;
  return (
    <>
      <div className="ws-milestone-summary"><div><strong>{milestones.length}</strong><span>planned weeks</span></div><div><strong>{project.milestones_completed || 0}</strong><span>completed</span></div><div><strong>{project.progress || 0}%</strong><span>overall progress</span></div></div>
      <div className="ws-milestone-list">
        {milestones.map((milestone) => (
          <article className={`ws-card ws-milestone-card status-${milestone.status || 'pending'}`} key={milestone.week_number}>
            <div className="ws-milestone-week"><span>WEEK</span><strong>{String(milestone.week_number).padStart(2, '0')}</strong></div>
            <div className="ws-milestone-content">
              <div className="ws-milestone-title"><div><h2>{milestone.milestone_title}</h2><p>{displayDate(milestone.expected_completion_date)}</p></div><select aria-label={`Week ${milestone.week_number} status`} value={milestone.status || 'pending'} onChange={(event) => onMilestoneChange(milestone.week_number, event.target.value)}><option value="pending">Not started</option><option value="in_progress">In progress</option><option value="completed">Completed</option></select></div>
              <div className="ws-form-two"><div><h3>Objectives</h3><ListItems items={listValue(milestone.objectives)} empty="No objectives provided." /></div><div><h3>Tasks &amp; deliverables</h3><ListItems items={[...listValue(milestone.tasks), ...listValue(milestone.deliverables)]} empty="No tasks provided." /></div></div>
            </div>
          </article>
        ))}
      </div>
    </>
  );
}

function MonitorPage({ project, projects, onSelect, onError }) {
  const [messages, setMessages] = useState(() => {
    if (!project?.id) return [];
    try {
      return JSON.parse(sessionStorage.getItem(`acad_monitor_${project.id}`) || '[]');
    } catch {
      return [];
    }
  });
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);

  useEffect(() => {
    if (project?.id) {
      sessionStorage.setItem(`acad_monitor_${project.id}`, JSON.stringify(messages));
    }
  }, [messages, project?.id]);

  const send = async (message) => {
    const content = message.trim();
    if (!content || !project || sending) return;
    const priorHistory = messages.slice(-12).map(({ role, content: text }) => ({ role, content: text }));
    setMessages((items) => [...items, { role: 'user', content, at: new Date().toISOString() }]);
    setInput('');
    setSending(true);
    onError('');
    try {
      const response = await sendProjectMentorMessage(project.id, content, priorHistory);
      setMessages((items) => [...items, {
        role: 'assistant',
        content: response.answer,
        actions: response.suggested_actions || [],
        followUp: response.follow_up_question,
        at: new Date().toISOString(),
      }]);
    } catch (error) {
      onError(error.message);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="ws-monitor-layout">
      <section className="ws-card ws-chat-card">
        <div className="ws-chat-header">
          <span className="ws-chat-avatar"><Bot size={20} /></span>
          <div><h2>NEXTSTEP AI Assistant</h2><p>{project ? `Project context: ${project.title}` : 'Project-aware academic guidance'}</p></div>
          {projects.length > 1 && <label className="ws-project-select"><span className="sr-only">Choose project</span><select value={project?.id || ''} onChange={(event) => onSelect(event.target.value)}>{projects.map((item) => <option value={item.id} key={item.id}>{item.title}</option>)}</select><ChevronDown size={14} /></label>}
        </div>
        {!project ? (
          <>
            <div className="ws-chat-welcome ws-chat-welcome-empty">
              <span><Sparkles size={20} /></span>
              <h2>Hello! Welcome to NEXTSTEP AI.</h2>
              <p>I&apos;m your intelligent project companion. I can help you plan milestones, monitor progress, understand your project blueprint, identify risks, and guide you towards successful project completion.</p>
            </div>
            <EmptyState title="Create a project to get started" text="NEXTSTEP AI uses your saved project blueprint and milestone data to provide specific guidance." />
          </>
        ) : (
          <>
            <div className="ws-chat-messages" aria-live="polite">
              {!messages.length && <div className="ws-chat-welcome"><span><Sparkles size={20} /></span><h2>Hello! Welcome to NEXTSTEP AI.</h2><p>I&apos;m your intelligent project companion. I can help you plan milestones, monitor progress, understand your project blueprint, identify risks, and guide you towards successful project completion.</p></div>}
              {messages.map((message, index) => (
                <div className={`ws-chat-message ${message.role}`} id={`ws-message-${index}`} key={`${message.at}-${index}`}>
                  {message.role === 'assistant' && <span className="ws-message-icon"><Bot size={16} /></span>}
                  <div className="ws-message-body"><p>{message.content}</p>{message.actions?.length > 0 && <ul>{message.actions.map((action) => <li key={action}>{action}</li>)}</ul>}{message.followUp && <p className="ws-chat-followup">{message.followUp}</p>}<time>{new Date(message.at).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })}</time></div>
                </div>
              ))}
              {sending && <div className="ws-chat-message assistant"><span className="ws-message-icon"><Bot size={16} /></span><div className="ws-typing"><i /><i /><i /><span>Reviewing your project…</span></div></div>}
            </div>
            {!messages.length && <div className="ws-suggestions">{SUGGESTED_QUESTIONS.map((question) => <button key={question} onClick={() => send(question)}>{question}<ArrowRight size={14} /></button>)}</div>}
            <form className="ws-chat-compose" onSubmit={(event) => { event.preventDefault(); send(input); }}>
              <input aria-label="Ask NEXTSTEP AI" value={input} onChange={(event) => setInput(event.target.value)} placeholder="Ask a question about this project…" maxLength={4000} disabled={sending} />
              <button className="ws-primary-button" type="submit" disabled={!input.trim() || sending} aria-label="Send message"><Send size={17} /></button>
            </form>
            <p className="ws-chat-disclaimer">AI guidance is based on available project data. Verify important academic and technical decisions with your project guide.</p>
          </>
        )}
      </section>
      <aside className="ws-monitor-aside">
        {messages.length > 0 && (
          <SectionCard title="Recent conversation" eyebrow="CHAT HISTORY">
            <div className="ws-history-list">
              {messages.slice(-4).reverse().map((message, index) => (
                <div className="ws-history-item" key={`${message.at}-${index}`}>
                  <span className={message.role}>{message.role === 'assistant' ? <Bot size={14} /> : <UserRound size={14} />}</span>
                  <div><small>{message.role === 'assistant' ? 'NEXTSTEP AI' : 'You'}</small><p>{message.content}</p></div>
                </div>
              ))}
            </div>
          </SectionCard>
        )}
        <SectionCard title="Project snapshot" eyebrow="CURRENT CONTEXT">
          {project ? <><div className="ws-snapshot-name">{project.title}</div><div className="ws-snapshot-row"><span>Duration</span><strong>{project.duration_weeks} weeks</strong></div><div className="ws-snapshot-row"><span>Progress</span><strong>{project.progress || 0}%</strong></div><div className="ws-snapshot-row"><span>Milestones</span><strong>{project.milestones_completed || 0} / {project.total_milestones || 0}</strong></div><button className="ws-inline-link" onClick={() => onSelect(project.id)}>Change project <ArrowRight size={15} /></button></> : <p className="ws-muted-copy">Your project snapshot will appear here.</p>}
        </SectionCard>
        <SectionCard title="Try asking" eyebrow="SUGGESTED PROMPTS">
          <div className="ws-prompt-list">{SUGGESTED_QUESTIONS.map((question) => <button key={question} onClick={() => send(question)} disabled={!project || sending}><MessageCircle size={15} />{question}</button>)}</div>
        </SectionCard>
      </aside>
    </div>
  );
}

function ProfilePage({ profile, updateProfileField, saving, onSubmit }) {
  return (
    <>
      <div className="ws-page-heading"><div><span className="ws-eyebrow">ACCOUNT</span><h1>Your academic profile</h1><p>Keep your student details up to date for more relevant project guidance.</p></div></div>
      <form className="ws-card ws-profile-form" onSubmit={onSubmit}>
        <div className="ws-form-section"><div className="ws-form-section-icon"><UserRound size={19} /></div><div className="ws-form-section-body"><h2>Academic details</h2><p>Profile information is saved to your authenticated student account.</p>
          <label className="ws-field"><span>Institution <b>*</b></span><input required minLength="2" maxLength="255" value={profile.institution || ''} onChange={(event) => updateProfileField('institution', event.target.value)} /></label>
          <div className="ws-form-two"><label className="ws-field"><span>Department <b>*</b></span><select required value={profile.department || ''} onChange={(event) => updateProfileField('department', event.target.value)}><option value="" disabled>Select department</option>{DEPARTMENTS.map((department) => <option key={department}>{department}</option>)}</select></label><label className="ws-field"><span>Current semester <b>*</b></span><select required value={profile.semester || ''} onChange={(event) => updateProfileField('semester', event.target.value)}><option value="" disabled>Select semester</option>{SEMESTERS.map((semester) => <option key={semester}>{semester}</option>)}</select></label></div>
          <label className="ws-field ws-profile-year"><span>Graduation year <b>*</b></span><select required value={profile.graduationYear || ''} onChange={(event) => updateProfileField('graduationYear', event.target.value)}><option value="" disabled>Select year</option>{GRADUATION_YEARS.map((year) => <option key={year}>{year}</option>)}</select></label>
        </div></div>
        <div className="ws-form-footer"><span>Changes are saved to your student profile.</span><button className="ws-primary-button" type="submit" disabled={saving}>{saving ? <LoaderCircle className="ws-spin" size={17} /> : <Check size={17} />}{saving ? 'Saving…' : 'Save profile'}</button></div>
      </form>
    </>
  );
}

function SettingsPage({ darkMode, onToggle }) {
  return (
    <>
      <div className="ws-page-heading"><div><span className="ws-eyebrow">PREFERENCES</span><h1>Settings</h1><p>Adjust your workspace appearance and preferences.</p></div></div>
      <SectionCard title="Appearance" eyebrow="WORKSPACE">
        <div className="ws-setting-row"><div className="ws-setting-icon"><Sparkles size={18} /></div><div className="ws-setting-copy"><strong>Dark theme</strong><span>Use a low-light color palette for your workspace.</span></div><button type="button" role="switch" aria-checked={darkMode} className={`ws-switch ${darkMode ? 'on' : ''}`} onClick={onToggle}><span /></button></div>
      </SectionCard>
      <SectionCard title="Account &amp; privacy" eyebrow="YOUR DATA">
        <p className="ws-prose">Your project records and NEXTSTEP AI conversations are scoped to your authenticated account. The assistant receives only the project details and blueprint needed to answer the current question.</p>
      </SectionCard>
    </>
  );
}
