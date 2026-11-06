import React from 'react';
import { RotateCcw, Bot, ChevronRight } from 'lucide-react';
import { useOnboarding } from '../../context/OnboardingContext';
import NextstepLogo from './NextstepLogo';

export default function WorkspaceTopBar() {
  const { currentStep, resetForm } = useOnboarding();

  const stepName =
    currentStep === 1
      ? 'Academic Setup'
      : currentStep === 2
      ? 'Skill & Tech Alignment'
      : currentStep === 3
      ? 'Roadmap Ready'
      : 'Dashboard';

  const stepNum = typeof currentStep === 'number' ? currentStep : 3;

  return (
    <header className="workspace-top-bar" aria-label="Workspace Header">
      {/* Mobile Branding (shown when sidebar hidden on small screens) */}
      <div className="mobile-brand-wrapper">
        <NextstepLogo size={34} />
      </div>

      {/* Breadcrumbs */}
      <div className="workspace-breadcrumbs">
        <span className="breadcrumb-root">Workspace</span>
        <ChevronRight size={14} className="breadcrumb-sep" />
        <span className="breadcrumb-current">New Project</span>
        <span className="breadcrumb-tag">{stepName}</span>
      </div>

      {/* Center/Right Status Indicators */}
      <div className="workspace-actions-group">
        {/* NEXTSTEP AI Assistant status */}
        <div className="ai-status-badge" title="NEXTSTEP AI Assistant is active">
          <span className="status-ping-dot">
            <span className="ping-wave" />
            <span className="ping-core" />
          </span>
          <Bot size={14} className="ai-status-bot" />
          <span className="ai-status-text">NEXTSTEP AI READY</span>
        </div>

        {/* Minimal Step Indicator */}
        <div className="step-counter-chip">
          <span className="step-number-highlight">Step {stepNum}</span>
          <span className="step-total">of 3</span>
        </div>

        {/* Reset / Clear Button */}
        <button
          type="button"
          onClick={resetForm}
          className="workspace-ghost-btn"
          title="Reset form"
          aria-label="Reset onboarding form"
        >
          <RotateCcw size={14} />
          <span className="btn-label-desktop">Reset</span>
        </button>
      </div>
    </header>
  );
}
