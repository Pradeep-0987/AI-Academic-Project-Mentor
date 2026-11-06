import React from 'react';
import {
  Sparkles,
  Bot,
  Compass,
  Code2,
  Users,
  Target,
  HelpCircle,
  Lightbulb,
  Zap,
  CheckCircle2
} from 'lucide-react';
import { useOnboarding } from '../../context/OnboardingContext';

export default function AiMentorInsightPanel({ currentStep = 1 }) {
  const { profile, selectedSkills, selectedInterests } = useOnboarding();

  // Dynamic contextual guidance based on user input
  const studentName = profile.fullName ? profile.fullName.split(' ')[0] : 'there';
  const hasBranch = Boolean(profile.department);
  const skillsCount = selectedSkills.length;
  const interestsCount = selectedInterests.length;

  return (
    <aside className="ai-mentor-panel" aria-label="NEXTSTEP AI project guidance">
      {/* Subtle Aurora orb glow in the card */}
      <div className="mentor-orb-glow" aria-hidden="true" />

      {/* Header with AI Pill */}
      <div className="mentor-panel-header">
        <div className="mentor-header-title-row">
          <div className="mentor-avatar-box">
            <Bot size={18} className="mentor-bot-icon" />
            <span className="mentor-status-ping" />
          </div>
          <div>
            <div className="mentor-tag-label">AI ADVISOR</div>
            <h3 className="mentor-heading">YOUR AI MENTOR</h3>
          </div>
        </div>

        <div className="mentor-active-indicator">
          <span className="mentor-pulse-dot" />
          <span>Online</span>
        </div>
      </div>

      {/* Primary Mentor Guidance Message */}
      <div className="mentor-quote-box">
        <div className="mentor-quote-halo" />
        <p className="mentor-quote-text">
          {currentStep === 1 ? (
            hasBranch ? (
              <>
                "Calibrating project guidelines for <strong>{profile.department.split('(')[0]}</strong>. Ready to match realistic capstone expectations."
              </>
            ) : (
              <>
                "Not sure where to begin? Start with a rough idea. We'll help you refine it into a high-scoring blueprint."
              </>
            )
          ) : (
            <>
              "Every tech stack choice impacts feasibility. Pick your strongest strengths and let AI fill architectural gaps."
            </>
          )}
        </p>
      </div>

      {/* 3 Guidance Tips */}
      <div className="mentor-tips-container">
        <div className="mentor-tips-label">
          <Lightbulb size={13} className="tips-bulb-icon" />
          <span>Blueprint Tips</span>
        </div>

        <div className="mentor-tips-list">
          <div className="mentor-tip-card">
            <div className="tip-index-dot">1</div>
            <div className="tip-text-block">
              <span className="tip-title">Start with the problem you want to solve</span>
              <span className="tip-desc">Focus on user friction or real-world inefficiencies first.</span>
            </div>
          </div>

          <div className="mentor-tip-card">
            <div className="tip-index-dot">2</div>
            <div className="tip-text-block">
              <span className="tip-title">Mention your intended users</span>
              <span className="tip-desc">Faculty evaluators favor clear target audiences &amp; personas.</span>
            </div>
          </div>

          <div className="mentor-tip-card">
            <div className="tip-index-dot">3</div>
            <div className="tip-text-block">
              <span className="tip-title">Share any technology preferences</span>
              <span className="tip-desc">Tell us languages or frameworks you already know.</span>
            </div>
          </div>
        </div>
      </div>

      {/* Calibration status preview */}
      <div className="mentor-readiness-card">
        <div className="readiness-header">
          <span className="readiness-caption">Context Calibration</span>
          <span className="readiness-score">
            {profile.department ? (skillsCount > 0 ? '90%' : '65%') : '30%'}
          </span>
        </div>
        <div className="readiness-bar-bg">
          <div
            className="readiness-bar-fill"
            style={{
              width: profile.department ? (skillsCount > 0 ? '90%' : '65%') : '30%'
            }}
          />
        </div>
        <p className="readiness-helper">
          {profile.department
            ? `Calibrated to ${profile.institution ? profile.institution.slice(0, 26) : 'your university'}`
            : 'Fill academic profile to unlock specialized benchmarks'}
        </p>
      </div>
    </aside>
  );
}
