import React from 'react';
import {
  User,
  Mail,
  School,
  BookOpen,
  Calendar,
  GraduationCap,
  ArrowRight,
  ArrowLeft,
  Info
} from 'lucide-react';
import { useOnboarding } from '../../context/OnboardingContext';
import { DEPARTMENTS, SEMESTERS, GRADUATION_YEARS } from '../../services/api';
import Input from '../common/Input';
import Select from '../common/Select';
import Button from '../common/Button';

/**
 * Screen 1 — Create Student Profile
 * Matches reference: STEP 1 OF 2 pill, serif heading, two-column form
 * grouped into "Personal Details" and "Academic Details" sections.
 * All existing state & validation from OnboardingContext is preserved.
 */
export default function ProfileForm() {
  const {
    profile,
    updateProfileField,
    profileErrors,
    handleSaveProfile,
    isLoading,
    goBack,
    currentStep,
  } = useOnboarding();

  const handleSubmit = (e) => {
    e.preventDefault();
    handleSaveProfile();
  };

  return (
    <>
      {/* ── Page header ── */}
      <div className="ob-page-header">
        <span className="ob-step-pill">Step 1 of 2</span>
        <h1 className="ob-page-title">Set Up Your Student Profile</h1>
        <p className="ob-page-subtitle">
          Tell us about your academic background to get started with your project.
        </p>
      </div>

      {/* ── Form card ── */}
      <div className="ob-form-card">
        <form onSubmit={handleSubmit} noValidate>

          {/* ── Personal Details section ── */}
          <div className="ob-section">
            <div className="ob-section-head">
              <div className="ob-section-icon" aria-hidden="true">
                <User size={17} strokeWidth={2} />
              </div>
              <div className="ob-section-text">
                <h2 className="ob-section-title">Personal Details</h2>
                <p className="ob-section-desc">
                  This information helps us personalize your mentoring experience.
                </p>
              </div>
            </div>

            <div className="form-grid-2">
              <Input
                id="profile-full-name"
                label="Full name"
                placeholder="Enter your full name"
                value={profile.fullName}
                onChange={(e) => updateProfileField('fullName', e.target.value)}
                required
                icon={User}
                error={profileErrors.fullName}
                autoComplete="name"
              />

              <Input
                id="profile-email"
                label="Email address"
                type="email"
                placeholder="you@college.edu"
                value={profile.email}
                onChange={(e) => updateProfileField('email', e.target.value)}
                required
                icon={Mail}
                error={profileErrors.email}
                autoComplete="email"
              />
            </div>

            <div className="form-grid-2" style={{ marginTop: '1.125rem' }}>
              <Select
                id="profile-gender"
                label="Gender"
                placeholder="Select gender"
                value={profile.gender || ''}
                onChange={(e) => updateProfileField('gender', e.target.value)}
                options={[
                  { value: 'Female', label: 'Female' },
                  { value: 'Male', label: 'Male' },
                  { value: 'Other', label: 'Other / Prefer not to say' }
                ]}
                required
                error={profileErrors.gender}
                helperText="Customizes your student avatar icon on the project dashboard."
              />
            </div>
          </div>

          <hr className="ob-section-divider" />

          {/* ── Academic Details section ── */}
          <div className="ob-section">
            <div className="ob-section-head">
              <div className="ob-section-icon" aria-hidden="true">
                <GraduationCap size={17} strokeWidth={2} />
              </div>
              <div className="ob-section-text">
                <h2 className="ob-section-title">Academic Details</h2>
                <p className="ob-section-desc">
                  Your academic information helps us suggest relevant resources and guidance.
                </p>
              </div>
            </div>

            <div className="form-grid" style={{ gap: '1.125rem' }}>
              {/* Row 1: College + Department */}
              <div className="form-grid-2">
                <Input
                  id="profile-institution"
                  label="College / Institution"
                  placeholder="Enter college or institution name"
                  value={profile.institution}
                  onChange={(e) => updateProfileField('institution', e.target.value)}
                  required
                  icon={School}
                  error={profileErrors.institution}
                />

                <Select
                  id="profile-department"
                  label="Department"
                  placeholder="Select department"
                  value={profile.department}
                  onChange={(e) => updateProfileField('department', e.target.value)}
                  options={DEPARTMENTS}
                  required
                  icon={BookOpen}
                  error={profileErrors.department}
                />
              </div>

              {/* Row 2: Semester + Graduation year */}
              <div className="form-grid-2">
                <Select
                  id="profile-semester"
                  label="Current semester"
                  placeholder="Select semester"
                  value={profile.semester}
                  onChange={(e) => updateProfileField('semester', e.target.value)}
                  options={SEMESTERS}
                  required
                  icon={Calendar}
                  error={profileErrors.semester}
                />

                <Select
                  id="profile-grad-year"
                  label="Graduation year"
                  placeholder="Select year"
                  value={profile.graduationYear}
                  onChange={(e) => updateProfileField('graduationYear', e.target.value)}
                  options={GRADUATION_YEARS}
                  required
                  icon={GraduationCap}
                  error={profileErrors.graduationYear}
                />
              </div>
            </div>
          </div>

          {/* ── Footer ── */}
          <div className="ob-card-footer">
            <div className="ob-footer-note">
              <Info size={15} aria-hidden="true" />
              <span>All fields marked with <strong>*</strong> are required.</span>
            </div>

            <div className="ob-footer-actions">
              {currentStep > 1 && (
                <Button
                  type="button"
                  variant="secondary"
                  onClick={goBack}
                  icon={ArrowLeft}
                  disabled={isLoading}
                >
                  Back
                </Button>
              )}

              <Button
                type="submit"
                variant="primary"
                size="lg"
                loading={isLoading}
                icon={ArrowRight}
                iconPosition="right"
              >
                Save profile &amp; continue
              </Button>
            </div>
          </div>

        </form>
      </div>
    </>
  );
}
