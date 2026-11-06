import React from 'react';
import { Lightbulb, Users2, TrendingUp } from 'lucide-react';
import mentorIllustration from '../../assets/mentor-robot-illustration.png';

const FEATURES = [
  { icon: Lightbulb,  text: 'Get personalized project guidance' },
  { icon: Users2,      text: 'Find ideas for real-world projects' },
  { icon: TrendingUp, text: 'Build skills and track progress' },
];

export default function RightPanel({ currentStep }) {
  // Don't render on dashboard
  if (currentStep === 'dashboard') return null;

  return (
    <aside className="acad-right-panel" aria-label="Academic mentoring overview">
      {/* Eyebrow */}
      <p className="rp-eyebrow">ACADEMIC PROJECTS, REAL IMPACT</p>

      {/* Headline */}
      <h2 className="rp-heading">
        Turn your ideas into meaningful projects.
      </h2>

      {/* Feature list */}
      <ul className="rp-features-list" aria-label="Benefits">
        {FEATURES.map(({ icon: Icon, text }) => (
          <li key={text} className="rp-feature">
            <div className="rp-feat-icon" aria-hidden="true">
              <Icon size={14} strokeWidth={2} />
            </div>
            <span className="rp-feat-text">{text}</span>
          </li>
        ))}
      </ul>

      {/* Student & AI Robot Illustration */}
      <div className="rp-illustration-wrap">
        <img
          src={mentorIllustration}
          alt="Student and AI robot collaborating on an academic project"
          className="rp-illustration-img"
        />
      </div>
    </aside>
  );
}
