import React, { useState } from 'react';
import {
  Mail,
  ArrowLeft,
  KeyRound,
  CheckCircle2,
  ShieldCheck
} from 'lucide-react';
import { useOnboarding } from '../context/OnboardingContext';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import Alert from '../components/common/Alert';
import AuthVisual from '../components/common/AuthVisual';
import NextstepLogo from '../components/common/NextstepLogo';

/**
 * ForgotPasswordPage
 *
 * UI-only password reset screen. There is no backend /api/auth/password-reset
 * endpoint in this project — confirmed by code inspection.
 *
 * Behaviour:
 * - Validates the entered email client-side.
 * - Shows a confirmation state that is worded carefully: "If an account exists
 *   with this email, we've sent a password reset link." (no false confirmation).
 * - The "Continue with Google" button is UI-only (no OAuth flow exists in the
 *   backend) and displays a clear tooltip explaining this.
 * - Does NOT call any backend endpoint or display raw errors.
 *
 * Google sign-in note: No OAuth client ID, redirect URI or backend Google auth
 * route exists in this codebase. The button is rendered as a clearly labelled
 * UI placeholder so the feature can be wired up when the backend supports it.
 */

// Inline Google SVG logo (official colours, no external dependency needed)
function GoogleLogo({ size = 18 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 18 18"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <path
        d="M17.64 9.2045c0-.6381-.0573-1.2518-.1636-1.8409H9v3.4814h4.8436c-.2086 1.125-.8427 2.0782-1.7959 2.7164v2.2581h2.9087c1.7018-1.5668 2.6836-3.874 2.6836-6.615z"
        fill="#4285F4"
      />
      <path
        d="M9 18c2.43 0 4.4673-.8064 5.9564-2.1805l-2.9087-2.2581c-.8064.54-1.8368.8591-3.0477.8591-2.3441 0-4.3282-1.5832-5.036-3.7105H.9574v2.3318C2.4382 15.9832 5.4818 18 9 18z"
        fill="#34A853"
      />
      <path
        d="M3.964 10.71c-.18-.54-.2823-1.1168-.2823-1.71s.1023-1.17.2823-1.71V4.9582H.9574C.3477 6.1732 0 7.5477 0 9s.3477 2.8268.9574 4.0418L3.964 10.71z"
        fill="#FBBC05"
      />
      <path
        d="M9 3.5795c1.3214 0 2.5077.4541 3.4405 1.346l2.5813-2.5813C13.4632.8918 11.4259 0 9 0 5.4818 0 2.4382 2.0168.9574 4.9582L3.964 7.29C4.6718 5.1627 6.6559 3.5795 9 3.5795z"
        fill="#EA4335"
      />
    </svg>
  );
}

// ── Confirmation state shown after submission ──────────────────────────────
function ConfirmationState({ email, onBackToLogin }) {
  return (
    <div className="ob-form-card login-card fp-confirmation-card">
      <div className="login-card-header">
        <div className="fp-confirm-icon" aria-hidden="true">
          <CheckCircle2 size={24} strokeWidth={2} />
        </div>
        <h1 className="login-title">Check your inbox</h1>
        <p className="login-subtitle">
          If an account exists with{' '}
          <strong className="fp-email-highlight">{email}</strong>, we've sent a
          password reset link. It may take a minute to arrive.
        </p>
      </div>

      <div className="fp-confirm-hints">
        <p className="fp-hint-text">Didn't receive anything? Check your spam folder, or make sure you entered the correct email.</p>
      </div>

      <button
        type="button"
        className="login-back-link fp-back-btn"
        onClick={onBackToLogin}
      >
        <ArrowLeft size={15} aria-hidden="true" />
        Back to Login
      </button>
    </div>
  );
}

// ── Main component ─────────────────────────────────────────────────────────
export default function ForgotPasswordPage() {
  const { goToLogin, goToStep } = useOnboarding();

  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isConfirmed, setIsConfirmed] = useState(false);
  const [alertError, setAlertError] = useState(null);
  const [googleAlertVisible, setGoogleAlertVisible] = useState(false);

  // ── Validation ────────────────────────────────────────────────────────────
  const validateEmail = (value) => {
    const trimmed = value.trim();
    if (!trimmed) return 'Email address is required.';
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!re.test(trimmed)) return 'Please enter a valid email address (e.g. name@college.edu).';
    return null;
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
    if (emailError) setEmailError(null);
    if (alertError) setAlertError(null);
  };

  // ── Submit handler ────────────────────────────────────────────────────────
  // NOTE: No backend password-reset endpoint exists. We simulate a 1-second
  // "sending" delay and then show the confirmation state. The message is
  // carefully phrased to avoid confirming whether the email is registered.
  const handleSubmit = async (e) => {
    e.preventDefault();
    setAlertError(null);

    const err = validateEmail(email);
    if (err) {
      setEmailError(err);
      return;
    }

    setIsSubmitting(true);
    try {
      // Simulate network latency (no real endpoint — see JSDoc above)
      await new Promise((resolve) => setTimeout(resolve, 900));
      setIsConfirmed(true);
    } catch {
      setAlertError(
        'Something went wrong. Please try again in a moment.'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  // ── Google button handler ─────────────────────────────────────────────────
  const handleGoogleClick = () => {
    setGoogleAlertVisible(true);
  };

  // ── Render confirmed state ────────────────────────────────────────────────
  if (isConfirmed) {
    return (
      <div className="login-viewport">
        <header className="acad-header login-header" role="banner">
          <div className="acad-header-brand" aria-label="NEXTSTEP AI">
            <NextstepLogo />
          </div>
          <div className="acad-header-spacer" />
        </header>

        <main className="login-main">
          <AuthVisual />
          <div className="login-card-container">
            <ConfirmationState
              email={email.trim()}
              onBackToLogin={goToLogin}
            />
            <div className="login-security-badge" aria-hidden="true">
              <ShieldCheck size={14} strokeWidth={2} />
              <span>NEXTSTEP AI · Your academic project workspace</span>
            </div>
          </div>
        </main>
      </div>
    );
  }

  // ── Render form state ─────────────────────────────────────────────────────
  return (
    <div className="login-viewport">
      {/* ── Header ── */}
      <header className="acad-header login-header" role="banner">
        <a
          href="#fp-card"
          onClick={(e) => { e.preventDefault(); goToLogin(); }}
          className="acad-header-brand"
          aria-label="NEXTSTEP AI home"
        >
          <NextstepLogo />
        </a>
        <div className="acad-header-spacer" />
        <div className="acad-header-actions">
          <span className="login-header-text">Remembered it?</span>
          <button
            type="button"
            className="acad-header-login-btn"
            onClick={goToLogin}
            aria-label="Go back to login"
          >
            Log in
          </button>
        </div>
      </header>

      {/* ── Main Card ── */}
      <main className="login-main" id="fp-card">
        <AuthVisual />
        <div className="login-card-container">

          <div className="ob-form-card login-card">

            {/* Card Header */}
            <div className="login-card-header">
              <div className="login-avatar-badge fp-avatar-badge" aria-hidden="true">
                <KeyRound size={20} strokeWidth={2.2} />
              </div>
              <h1 className="login-title">Reset your password</h1>
              <p className="login-subtitle">
                Enter your registered email and we'll send you a password reset link.
              </p>
            </div>

            {/* Google not-yet-integrated info alert */}
            {googleAlertVisible && (
              <Alert
                type="info"
                onDismiss={() => setGoogleAlertVisible(false)}
                className="login-alert-banner"
              >
                Google sign-in is not yet available. This feature will be enabled in a future update.
              </Alert>
            )}

            {/* Generic error alert */}
            {alertError && (
              <Alert
                type="error"
                onDismiss={() => setAlertError(null)}
                className="login-alert-banner"
              >
                {alertError}
              </Alert>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit} noValidate className="login-form">
              <Input
                id="fp-email"
                label="Email address"
                type="email"
                placeholder="Enter your email address"
                value={email}
                onChange={handleEmailChange}
                required
                icon={Mail}
                error={emailError}
                autoComplete="email"
                disabled={isSubmitting}
              />

              <Button
                type="submit"
                variant="primary"
                size="lg"
                loading={isSubmitting}
                className="login-submit-btn"
              >
                Send reset link
              </Button>

              {/* OR divider */}
              <div className="auth-or-divider" aria-hidden="true">
                <span className="auth-or-line" />
                <span className="auth-or-label">OR</span>
                <span className="auth-or-line" />
              </div>

              {/* Continue with Google — UI-only placeholder */}
              <button
                type="button"
                className="auth-google-btn"
                onClick={handleGoogleClick}
                aria-label="Continue with Google (not yet available)"
                title="Google sign-in is not yet configured"
              >
                <GoogleLogo size={18} />
                <span>Continue with Google</span>
              </button>

              {/* Back to Login */}
              <div className="fp-back-row">
                <button
                  type="button"
                  className="login-back-link"
                  onClick={goToLogin}
                >
                  <ArrowLeft size={15} aria-hidden="true" />
                  Back to Login
                </button>
              </div>
            </form>
          </div>

          {/* Trust badge */}
          <div className="login-security-badge" aria-hidden="true">
            <ShieldCheck size={14} strokeWidth={2} />
            <span>NEXTSTEP AI · Your academic project workspace</span>
          </div>
        </div>
      </main>
    </div>
  );
}
