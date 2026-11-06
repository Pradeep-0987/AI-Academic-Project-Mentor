import React from 'react';
import { Check } from 'lucide-react';
import { useOnboarding } from '../../context/OnboardingContext';

const STEPS = [
  {
    id: 1,
    num: '01',
    name: 'Create Student Profile',
  },
  {
    id: 2,
    num: '02',
    name: 'Access Your Skills',
  },
];

export default function AcadSidebar() {
  const { currentStep, goToStep } = useOnboarding();

  // Hide sidebar entirely on dashboard
  if (currentStep === 'dashboard') return null;

  return (
    <aside className="acad-sidebar" aria-label="Onboarding steps">
      <p className="acad-sidebar-section-label">Student Onboarding</p>

      {/* Step list */}
      <div className="acad-step-list" role="list">
        {/* Thin connector line */}
        <div className="acad-step-connector" aria-hidden="true" />

        {STEPS.map((step) => {
          const isActive    = currentStep === step.id;
          const isCompleted = typeof currentStep === 'number' && currentStep > step.id;
          const isInactive  = !isActive && !isCompleted;

          return (
            <div
              key={step.id}
              role="listitem"
              className={
                `acad-step-item ${
                  isActive ? 'is-active' :
                  isCompleted ? 'is-completed' :
                  'is-inactive'
                }`
              }
              onClick={() => isCompleted && goToStep(step.id)}
              tabIndex={isCompleted ? 0 : undefined}
              onKeyDown={(e) => {
                if (isCompleted && (e.key === 'Enter' || e.key === ' ')) {
                  e.preventDefault();
                  goToStep(step.id);
                }
              }}
              aria-current={isActive ? 'step' : undefined}
              aria-label={`${isCompleted ? 'Completed: ' : ''}${step.name}`}
            >
              <div className="acad-step-num" aria-hidden="true">
                {isCompleted ? <Check size={14} strokeWidth={3} /> : step.num}
              </div>
              <div className="acad-step-body">
                <span className="acad-step-name">{step.name}</span>
              </div>
            </div>
          );
        })}
      </div>
    </aside>
  );
}
