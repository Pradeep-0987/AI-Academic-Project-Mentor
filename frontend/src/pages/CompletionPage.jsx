import React, { useState, useMemo } from 'react';
import {
  CheckCircle2,
  ArrowRight,
  ArrowLeft,
  GraduationCap,
  Code2,
  Target
} from 'lucide-react';
import { useOnboarding } from '../context/OnboardingContext';
import { PRESET_INTERESTS, saveStudentProfileOnboarding, submitStudentSkillAssessment } from '../services/api';
import Button from '../components/common/Button';

/**
 * Screen 3 — Completion & Summary
 * Matches the academic design system: Warm Ivory, Forest Green, Lora typography.
 * Summarizes the student's profile, calibrated skills, and project focus areas.
 */
export default function CompletionPage() {
  const { goToDashboard, goBack, profile, selectedSkills, selectedInterests, setStatusMessage } = useOnboarding();
  const [isSaving, setIsSaving] = useState(false);

  const firstName = profile.fullName ? profile.fullName.trim().split(' ')[0] : 'Innovator';

  // Map interest IDs to full titles
  const interestMap = useMemo(() => {
    const map = {};
    PRESET_INTERESTS.forEach((item) => {
      map[item.id] = item.title;
    });
    return map;
  }, []);

  const handleSaveAndContinue = async () => {
    if (isSaving) return;
    setIsSaving(true);
    if (setStatusMessage) setStatusMessage(null);

    try {
      await saveStudentProfileOnboarding(profile);
      await submitStudentSkillAssessment({
        skills: selectedSkills,
        interests: selectedInterests
      });

      // Navigate cleanly to dashboard (student starts with 0 projects until they add one)
      goToDashboard();
    } catch (err) {
      if (setStatusMessage) {
        setStatusMessage({
          type: 'error',
          text: err.message || 'Failed to save student onboarding data. Please try again.'
        });
      }
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <>
      {/* ── Page header ── */}
      <div className="ob-page-header">
        <span className="ob-step-pill">Summary &amp; Confirmation</span>
        <h1 className="ob-page-title">Welcome aboard, {firstName}!</h1>
        <p className="ob-page-subtitle">
          Your student profile, technical capabilities, and project interests have been calibrated.
          Your personalized mentoring workspace is ready to launch.
        </p>
      </div>

      {/* ── Form Card ── */}
      <div className="ob-form-card">
        {/* Success Banner */}
        <div className="completion-banner" role="status">
          <div className="completion-banner-icon" aria-hidden="true">
            <CheckCircle2 size={24} strokeWidth={2.5} />
          </div>
          <div className="completion-banner-text">
            <h3>Profile &amp; Curriculum Calibrated</h3>
            <p>
              Your academic background and technology stack are synchronized with our mentor guidance models.
            </p>
          </div>
        </div>

        {/* Summary Grid */}
        <div className="summary-grid">
          {/* Card 1: Academic Profile */}
          <div className="summary-card">
            <div className="summary-card-header">
              <div className="summary-card-icon" aria-hidden="true">
                <GraduationCap size={16} />
              </div>
              <h3>Academic Background</h3>
            </div>
            <div className="summary-field-list">
              <div className="summary-field-row">
                <span className="summary-field-label">Full Name</span>
                <span className="summary-field-value">{profile.fullName || '—'}</span>
              </div>
              <div className="summary-field-row">
                <span className="summary-field-label">Email</span>
                <span className="summary-field-value">{profile.email || '—'}</span>
              </div>
              <div className="summary-field-row">
                <span className="summary-field-label">Gender</span>
                <span className="summary-field-value">{profile.gender || '—'}</span>
              </div>
              <div className="summary-field-row">
                <span className="summary-field-label">Institution</span>
                <span className="summary-field-value">{profile.institution || '—'}</span>
              </div>
              <div className="summary-field-row">
                <span className="summary-field-label">Department</span>
                <span className="summary-field-value">{profile.department || '—'}</span>
              </div>
              <div className="summary-field-row">
                <span className="summary-field-label">Semester</span>
                <span className="summary-field-value">{profile.semester || '—'}</span>
              </div>
              <div className="summary-field-row">
                <span className="summary-field-label">Graduation Year</span>
                <span className="summary-field-value">{profile.graduationYear || '—'}</span>
              </div>
            </div>
          </div>

          {/* Card 2: Technical Skills */}
          <div className="summary-card">
            <div className="summary-card-header">
              <div className="summary-card-icon" aria-hidden="true">
                <Code2 size={16} />
              </div>
              <h3>Technical Skills ({selectedSkills.length})</h3>
            </div>
            {selectedSkills.length === 0 ? (
              <p style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)' }}>
                No technical skills recorded yet.
              </p>
            ) : (
              <div className="summary-chip-wrap">
                {selectedSkills.map((skill) => (
                  <div key={skill.name} className="summary-skill-chip">
                    <span>{skill.name}</span>
                    <span className={`summary-skill-level ${skill.level.toLowerCase()}`}>
                      {skill.level}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Card 3: Areas of Interest */}
          <div className="summary-card full-width">
            <div className="summary-card-header">
              <div className="summary-card-icon" aria-hidden="true">
                <Target size={16} />
              </div>
              <h3>Project Areas of Interest ({selectedInterests.length})</h3>
            </div>
            {selectedInterests.length === 0 ? (
              <p style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)' }}>
                No interest areas selected yet.
              </p>
            ) : (
              <div className="summary-chip-wrap">
                {selectedInterests.map((id) => (
                  <div
                    key={id}
                    className="summary-skill-chip"
                    style={{
                      background: 'var(--color-primary-light)',
                      borderColor: 'var(--color-primary-border)',
                      color: 'var(--color-primary)'
                    }}
                  >
                    <span>{interestMap[id] || id}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* ── Footer ── */}
        <div className="ob-card-footer">
          <Button
            type="button"
            variant="secondary"
            onClick={goBack}
            icon={ArrowLeft}
            disabled={isSaving}
          >
            Back to Skills
          </Button>

          <Button
            type="button"
            variant="primary"
            size="lg"
            loading={isSaving}
            onClick={handleSaveAndContinue}
            icon={ArrowRight}
            iconPosition="right"
          >
            Save &amp; Continue
          </Button>
        </div>
      </div>
    </>
  );
}
