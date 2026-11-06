import React, { useState } from 'react';
import {
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowRight,
  LogIn,
  ShieldCheck
} from 'lucide-react';
import { useOnboarding } from '../context/OnboardingContext';
import { loginUser } from '../services/auth';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import Alert from '../components/common/Alert';
import AuthVisual from '../components/common/AuthVisual';
import NextstepLogo from '../components/common/NextstepLogo';

// Inline Google SVG logo (official colours)
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
      <path d="M17.64 9.2045c0-.6381-.0573-1.2518-.1636-1.8409H9v3.4814h4.8436c-.2086 1.125-.8427 2.0782-1.7959 2.7164v2.2581h2.9087c1.7018-1.5668 2.6836-3.874 2.6836-6.615z" fill="#4285F4" />
      <path d="M9 18c2.43 0 4.4673-.8064 5.9564-2.1805l-2.9087-2.2581c-.8064.54-1.8368.8591-3.0477.8591-2.3441 0-4.3282-1.5832-5.036-3.7105H.9574v2.3318C2.4382 15.9832 5.4818 18 9 18z" fill="#34A853" />
      <path d="M3.964 10.71c-.18-.54-.2823-1.1168-.2823-1.71s.1023-1.17.2823-1.71V4.9582H.9574C.3477 6.1732 0 7.5477 0 9s.3477 2.8268.9574 4.0418L3.964 10.71z" fill="#FBBC05" />
      <path d="M9 3.5795c1.3214 0 2.5077.4541 3.4405 1.346l2.5813-2.5813C13.4632.8918 11.4259 0 9 0 5.4818 0 2.4382 2.0168.9574 4.9582L3.964 7.29C4.6718 5.1627 6.6559 3.5795 9 3.5795z" fill="#EA4335" />
    </svg>
  );
}

/**
 * LoginPage Component
 *
 * Responsive, accessible sign-in screen in the NEXTSTEP AI visual system:
 * - Split-screen layout with branded project-planning artwork
 * - Form validation (required checks + email format regex) with inline error messages
 * - Password visibility toggle
 * - Password reset navigation
 * - Integration with backend POST /api/auth/login endpoint
 * - On success: stores the access token and user session, then opens the workspace
 */
export default function LoginPage() {
  const { goToStep, goToLogin, goToSignup, handleLoginSuccess, goToForgotPassword } = useOnboarding();
  const [googleAlertVisible, setGoogleAlertVisible] = useState(false);

  // Form input state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  // Validation & API error states
  const [fieldErrors, setFieldErrors] = useState({});
  const [apiError, setApiError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Validate form fields on the frontend
  const validateForm = () => {
    const errors = {};
    const trimmedEmail = email.trim();

    if (!trimmedEmail) {
      errors.email = 'Email address is required.';
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(trimmedEmail)) {
        errors.email = 'Please enter a valid email address (e.g. name@college.edu).';
      }
    }

    if (!password) {
      errors.password = 'Password is required.';
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
    if (fieldErrors.email) {
      setFieldErrors((prev) => ({ ...prev, email: undefined }));
    }
    if (apiError) setApiError(null);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
    if (fieldErrors.password) {
      setFieldErrors((prev) => ({ ...prev, password: undefined }));
    }
    if (apiError) setApiError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError(null);

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    try {
      const response = await loginUser(email, password);
      handleLoginSuccess(response);
    } catch (err) {
      setApiError(err.message || 'Login failed. Please check your credentials and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-viewport">
      {/* ── Minimal Top Navigation Header ── */}
      <header className="acad-header login-header" role="banner">
        <a
          href="#login-card"
          onClick={(e) => {
            e.preventDefault();
            goToLogin();
          }}
          className="acad-header-brand"
          aria-label="NEXTSTEP AI home"
        >
          <NextstepLogo />
        </a>

        <div className="acad-header-spacer" />

        <div className="acad-header-actions">
          <span className="login-header-text">Need an account?</span>
          <button
            type="button"
            className="acad-header-login-btn"
            onClick={goToSignup}
            aria-label="Go to student registration and onboarding"
          >
            Sign up
          </button>
        </div>
      </header>

      {/* ── Main Centered Card Container ── */}
      <main className="login-main" id="login-card">
        <AuthVisual />
        <div className="login-card-container">

          {/* Form Card */}
          <div className="ob-form-card login-card">
            {/* Header / Avatar */}
            <div className="login-card-header">
              <h1 className="login-title">Welcome back</h1>
              <p className="login-subtitle">
                Log in to continue your project journey.
              </p>
            </div>

            {/* Server Error Alert Banner */}
            {apiError && (
              <Alert
                type="error"
                onDismiss={() => setApiError(null)}
                className="login-alert-banner"
              >
                {apiError}
              </Alert>
            )}

            {/* Login Form */}
            <form onSubmit={handleSubmit} noValidate className="login-form">
              {/* Email Input */}
              <Input
                id="login-email"
                label="Email address"
                type="email"
                placeholder="you@college.edu"
                value={email}
                onChange={handleEmailChange}
                required
                icon={Mail}
                error={fieldErrors.email}
                autoComplete="email"
                disabled={isLoading}
              />

              {/* Password Input with Show/Hide Toggle */}
              <div className="login-password-group">
                <div className="login-password-header">
                  <label htmlFor="login-password" className="form-label">
                    <span>
                      Password <span className="required-star" aria-hidden="true">*</span>
                    </span>
                  </label>
                  {/* Clickable 'Forgot password?' — navigates to forgot-password page */}
                  <button
                    type="button"
                    className="login-forgot-link"
                    onClick={goToForgotPassword}
                    aria-label="Reset your password"
                  >
                    Forgot password?
                  </button>
                </div>

                <div className="input-wrapper">
                  <span className="input-icon-left">
                    <Lock size={18} aria-hidden="true" />
                  </span>
                  <input
                    id="login-password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={handlePasswordChange}
                    placeholder="Enter your password"
                    disabled={isLoading}
                    autoComplete="current-password"
                    aria-invalid={!!fieldErrors.password}
                    aria-describedby={fieldErrors.password ? 'login-password-error' : undefined}
                    className={`form-input has-icon-left has-right-element ${
                      fieldErrors.password ? 'has-error' : ''
                    }`.trim()}
                  />
                  <div className="input-element-right">
                    <button
                      type="button"
                      className="password-toggle-btn"
                      onClick={() => setShowPassword((prev) => !prev)}
                      aria-label={showPassword ? 'Hide password' : 'Show password'}
                      title={showPassword ? 'Hide password' : 'Show password'}
                      tabIndex={0}
                    >
                      {showPassword ? (
                        <EyeOff size={18} aria-hidden="true" />
                      ) : (
                        <Eye size={18} aria-hidden="true" />
                      )}
                    </button>
                  </div>
                </div>

                {fieldErrors.password && (
                  <div id="login-password-error" className="form-error-msg" role="alert">
                    <span>{fieldErrors.password}</span>
                  </div>
                )}
              </div>

              {/* Submit Button */}
              <Button
                type="submit"
                variant="primary"
                size="lg"
                loading={isLoading}
                className="login-submit-btn"
                icon={ArrowRight}
                iconPosition="right"
              >
                Log in
              </Button>

              {/* OR divider */}
              <div className="auth-or-divider" aria-hidden="true">
                <span className="auth-or-line" />
                <span className="auth-or-label">OR</span>
                <span className="auth-or-line" />
              </div>

              {/* Continue with Google — UI-only placeholder (no OAuth backend) */}
              {googleAlertVisible && (
                <Alert
                  type="info"
                  onDismiss={() => setGoogleAlertVisible(false)}
                  className="login-alert-banner"
                >
                  Google sign-in is not yet available. This feature will be enabled in a future update.
                </Alert>
              )}
              <button
                type="button"
                className="auth-google-btn"
                onClick={() => setGoogleAlertVisible(true)}
                aria-label="Continue with Google (not yet available)"
                title="Google sign-in is not yet configured"
              >
                <GoogleLogo size={18} />
                <span>Continue with Google</span>
              </button>

              {/* Signup Redirect Link */}
              <div className="login-card-footer">
                <span className="login-footer-text">Don&apos;t have an account?</span>{' '}
                <button
                  type="button"
                  onClick={goToSignup}
                  className="login-signup-link"
                >
                  Sign up
                </button>
              </div>
            </form>
          </div>

          {/* Academic trust badge */}
          <div className="login-security-badge" aria-hidden="true">
            <ShieldCheck size={14} strokeWidth={2} />
            <span>NEXTSTEP AI · Your academic project workspace</span>
          </div>
        </div>
      </main>
    </div>
  );
}
