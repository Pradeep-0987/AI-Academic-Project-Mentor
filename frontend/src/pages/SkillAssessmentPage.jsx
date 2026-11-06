import React from 'react';
import { ArrowLeft, ArrowRight, Code2, Target } from 'lucide-react';
import { useOnboarding } from '../context/OnboardingContext';
import Button from '../components/common/Button';
import SkillSelector from '../components/skills/SkillSelector';
import SelectedSkillList from '../components/skills/SelectedSkillList';
import InterestSelector from '../components/skills/InterestSelector';

/**
 * Screen 2 — Access Your Skills
 * Matches reference design: STEP 2 OF 2 pill, serif heading,
 * Technical Skills section + Areas of Interest section inside a single
 * ob-form-card. The primary action advances to the CompletionPage (step 3).
 * All existing context logic and API calls are preserved.
 */
export default function SkillAssessmentPage() {
  const { goBack, handleSubmitSkills, isLoading } = useOnboarding();

  const handleContinue = (e) => {
    e.preventDefault();
    handleSubmitSkills();
  };

  return (
    <>
      {/* ── Page header ── */}
      <div className="ob-page-header">
        <span className="ob-step-pill">Step 2 of 2</span>
        <h1 className="ob-page-title">Access your skills</h1>
        <p className="ob-page-subtitle">
          Select the technologies you know and the areas you want to explore.
          Your mentor will calibrate project complexity accordingly.
        </p>
      </div>

      {/* ── Form card ── */}
      <div className="ob-form-card">
        <form onSubmit={handleContinue} noValidate>

          {/* ── Technical Skills ── */}
          <div className="ob-section">
            <div className="ob-section-head">
              <div className="ob-section-icon" aria-hidden="true">
                <Code2 size={17} strokeWidth={2} />
              </div>
              <div className="ob-section-text">
                <h2 className="ob-section-title">Technical Skills</h2>
                <p className="ob-section-desc">
                  Pick your comfortable programming languages, frameworks, and tools.
                </p>
              </div>
            </div>

            <div className="ob-skills-section">
              {/* Preset chips + custom adder */}
              <SkillSelector />

              {/* Selected skills with proficiency controls */}
              <SelectedSkillList />
            </div>
          </div>

          <hr className="ob-section-divider" />

          {/* ── Areas of Interest ── */}
          <div className="ob-section">
            <div className="ob-section-head">
              <div className="ob-section-icon" aria-hidden="true">
                <Target size={17} strokeWidth={2} />
              </div>
              <div className="ob-section-text">
                <h2 className="ob-section-title">Areas of Interest</h2>
                <p className="ob-section-desc">
                  Choose the project domains that excite you most. Select all that apply.
                </p>
              </div>
            </div>

            <InterestSelector />
          </div>

          {/* ── Footer ── */}
          <div className="ob-card-footer">
            <div className="ob-footer-note" />

            <div className="ob-footer-actions">
              <Button
                type="button"
                variant="secondary"
                onClick={goBack}
                icon={ArrowLeft}
                disabled={isLoading}
              >
                Back
              </Button>

              <Button
                type="submit"
                variant="primary"
                size="lg"
                loading={isLoading}
                icon={ArrowRight}
                iconPosition="right"
              >
                Save &amp; continue
              </Button>
            </div>
          </div>

        </form>
      </div>
    </>
  );
}
