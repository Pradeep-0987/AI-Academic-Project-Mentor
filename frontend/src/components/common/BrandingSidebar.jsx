import React from 'react';
import {
  Sparkles,
  Compass,
  Cpu,
  Milestone,
  CheckCircle2
} from 'lucide-react';
import NextstepLogo from './NextstepLogo';

export default function BrandingSidebar({ className = '' }) {
  const highlights = [
    {
      icon: Compass,
      title: 'Smart Project Planning',
      description: 'Calibrate scope, curricular depth, and feasibility automatically.'
    },
    {
      icon: Cpu,
      title: 'Personalized Tech Stack',
      description: 'Tailor architecture, libraries, and tools to match your abilities.'
    },
    {
      icon: Milestone,
      title: 'AI-Guided Milestones',
      description: 'Structured sprint breakdowns with defense-ready deliverables.'
    }
  ];

  return (
    <aside className={`branding-sidebar ${className}`.trim()} aria-label="NEXTSTEP AI Overview">
      {/* Decorative ambient background mesh & glowing aura */}
      <div className="sidebar-aurora-glow" aria-hidden="true" />
      <div className="sidebar-grid-overlay" aria-hidden="true" />

      {/* Top Header / Logo */}
      <div className="sidebar-brand-header">
        <NextstepLogo />
      </div>

      {/* Headline & Value Proposition */}
      <div className="sidebar-main-intro">
        <h2 className="sidebar-headline">
          Turn your idea into a project that <span className="text-gradient-aurora">works.</span>
        </h2>
        <p className="sidebar-subtext">
          Plan smarter. Build confidently. Get AI-guided mentorship at every step.
        </p>

        {/* Abstract AI network orb illustration */}
        <div className="sidebar-network-card">
          <div className="network-orb-center">
            <div className="network-core-ring" />
            <Sparkles size={20} className="network-core-icon" />
          </div>
          <svg className="network-wires-svg" viewBox="0 0 240 70" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M 20 35 Q 70 10 120 35 T 220 35" stroke="rgba(139, 92, 246, 0.4)" strokeWidth="1.5" strokeDasharray="3 3" />
            <path d="M 30 50 Q 80 60 120 35 T 210 20" stroke="rgba(96, 165, 250, 0.35)" strokeWidth="1.2" />
            <circle cx="30" cy="50" r="3" fill="#60A5FA" />
            <circle cx="210" cy="20" r="3" fill="#8B5CF6" />
            <circle cx="65" cy="22" r="2.5" fill="#C4B5FD" />
            <circle cx="175" cy="45" r="2.5" fill="#93C5FD" />
          </svg>
          <div className="network-stat-label">
            <span className="live-dot" />
            <span>Curriculum Model v4.2 Active</span>
          </div>
        </div>
      </div>

      {/* Three Compact Feature Highlights */}
      <div className="sidebar-features-list">
        {highlights.map((feat, idx) => {
          const Icon = feat.icon;
          return (
            <div key={idx} className="sidebar-feature-item">
              <div className="feature-icon-wrapper">
                <Icon size={16} strokeWidth={2.2} />
              </div>
              <div className="feature-content">
                <h4 className="feature-title">{feat.title}</h4>
                <p className="feature-description">{feat.description}</p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Sidebar Footer */}
      <div className="sidebar-footer-region">
        <div className="footer-student-badge">
          <CheckCircle2 size={13} className="text-emerald" />
          <span>Built for student innovators.</span>
        </div>
      </div>
    </aside>
  );
}
