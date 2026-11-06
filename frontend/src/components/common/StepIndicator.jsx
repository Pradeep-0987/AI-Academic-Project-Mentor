import React from 'react';
import { Check, User, Code2, Award } from 'lucide-react';
import { useOnboarding } from '../../context/OnboardingContext';

export default function StepIndicator({ compact = false }) {
  const { currentStep, goToStep } = useOnboarding();

  const steps = [
    {
      id: 1,
      name: 'Student Profile',
      desc: 'Academic Background',
      icon: User
    },
    {
      id: 2,
      name: 'Skill Assessment',
      desc: 'Technical & Interests',
      icon: Code2
    },
    {
      id: 3,
      name: 'Complete',
      desc: 'Ready for Projects',
      icon: Award
    }
  ];

  // If on dashboard, hide onboarding stepper
  if (currentStep === 'dashboard') {
    return null;
  }

  // Calculate line progress percentage
  // 1 -> 0%, 2 -> 50%, 3 -> 100%
  const progressPercent = currentStep === 1 ? 0 : currentStep === 2 ? 50 : 100;

  return (
    <div className={`stepper-container ${compact ? 'stepper-compact' : ''}`} aria-label="Onboarding Progress">
      <div className="stepper-track">
        {/* Background Track Line */}
        <div className="stepper-line-bg" />
        {/* Dynamic Active Progress Line */}
        <div
          className="stepper-line-progress"
          style={{ width: `calc(${progressPercent}% * (100% - ${compact ? '48px' : '80px'}) / 100)` }}
        />

        {steps.map((step) => {
          const isCompleted = currentStep > step.id;
          const isActive = currentStep === step.id;
          const StepIcon = step.icon;

          return (
            <button
              key={step.id}
              type="button"
              className={`step-item ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}
              onClick={() => goToStep(step.id)}
              disabled={step.id > currentStep}
              aria-current={isActive ? 'step' : undefined}
            >
              <div className="step-circle">
                {isCompleted ? (
                  <Check size={18} strokeWidth={2.5} />
                ) : (
                  <StepIcon size={18} strokeWidth={isActive ? 2.5 : 2} />
                )}
              </div>
              <div className="step-labels">
                <span className="step-label-title">{step.name}</span>
                <span className="step-label-desc">{step.desc}</span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
