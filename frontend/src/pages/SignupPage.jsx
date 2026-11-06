import React, { useState } from 'react';
import {
  User,
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowRight,
  ShieldCheck
} from 'lucide-react';
import { useOnboarding } from '../context/OnboardingContext';
import { registerUser } from '../services/auth';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import Alert from '../components/common/Alert';
import AuthVisual from '../components/common/AuthVisual';
import NextstepLogo from '../components/common/NextstepLogo';

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

export default function SignupPage() {
  const { goToLogin, handleRegisterSuccess } = useOnboarding();
  const [googleAlertVisible, setGoogleAlertVisible] = useState(false);

  // Form input state
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Validation & API error states
  const [fieldErrors, setFieldErrors] = useState({});
  const [apiError, setApiError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Form validation
  const validateForm = () => {
    const errors = {};
    const trimmedName = name.trim();
    const trimmedEmail = email.trim();

    if (!trimmedName) {
      errors.name = 'Full name is required.';
    } else if (trimmedName.length < 2) {
      errors.name = 'Name must be at least 2 characters.';
    }

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
    } else if (password.length < 8) {
      errors.password = 'Password must be at least 8 characters.';
    }

    if (!confirmPassword) {
      errors.confirmPassword = 'Please confirm your password.';
    } else if (confirmPassword !== password) {
      errors.confirmPassword = 'Passwords do not match.';
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleNameChange = (e) => {
    setName(e.target.value);
    if (fieldErrors.name) setFieldErrors((prev) => ({ ...prev, name: undefined }));
    if (apiError) setApiError(null);
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
    if (fieldErrors.email) setFieldErrors((prev) => ({ ...prev, email: undefined }));
    if (apiError) setApiError(null);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
    if (fieldErrors.password) setFieldErrors((prev) => ({ ...prev, password: undefined }));
    if (fieldErrors.confirmPassword && confirmPassword && e.target.value === confirmPassword) {
      setFieldErrors((prev) => ({ ...prev, confirmPassword: undefined }));
    }
    if (apiError) setApiError(null);
  };

  const handleConfirmPasswordChange = (e) => {
    setConfirmPassword(e.target.value);
    if (fieldErrors.confirmPassword) setFieldErrors((prev) => ({ ...prev, confirmPassword: undefined }));
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
      const response = await registerUser(name, email, password);
      handleRegisterSuccess(response);
    } catch (err) {
      setApiError(err.message || 'Registration failed. Please check your details and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-viewport">
      {/* ── Top Header ── */}
      <header className="acad-header login-header" role="banner">
        <a
          href="#signup-card"
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
          <span className="login-header-text">Already registered?</span>
          <button
            type="button"
            className="acad-header-login-btn"
            onClick={goToLogin}
            aria-label="Go to login page"
          >
            Log in
          </button>
        </div>
      </header>

      {/* ── Main Signup Card ── */}
      <main className="login-main" id="signup-card">
        <AuthVisual />
        <div className="login-card-container">
          <div className="ob-form-card login-card">
            {/* Header */}
            <div className="login-card-header">
              <h1 className="login-title">Create your account</h1>
              <p className="login-subtitle">
                Sign up with your credentials to begin your project journey.
              </p>
            </div>

            {/* Error banner */}
            {apiError && (
              <Alert
                type="error"
                onDismiss={() => setApiError(null)}
                className="login-alert-banner"
              >
                {apiError}
              </Alert>
            )}

            {/* Signup Form */}
            <form onSubmit={handleSubmit} noValidate className="login-form">
              {/* Full Name */}
              <Input
                id="signup-name"
                label="Full name"
                type="text"
                placeholder="e.g. Jaya Prakash"
                value={name}
                onChange={handleNameChange}
                required
                icon={User}
                error={fieldErrors.name}
                autoComplete="name"
                disabled={isLoading}
              />

              {/* Email Address */}
              <Input
                id="signup-email"
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

              {/* Password */}
              <div className="login-password-group">
                <label htmlFor="signup-password" className="form-label">
                  <span>
                    Password <span className="required-star" aria-hidden="true">*</span>
                  </span>
                </label>
                <div className="input-wrapper">
                  <span className="input-icon-left">
                    <Lock size={18} aria-hidden="true" />
                  </span>
                  <input
                    id="signup-password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={handlePasswordChange}
                    placeholder="Create a password (min. 8 characters)"
                    disabled={isLoading}
                    autoComplete="new-password"
                    aria-invalid={!!fieldErrors.password}
                    aria-describedby={fieldErrors.password ? 'signup-password-error' : undefined}
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
                    >
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                </div>
                {fieldErrors.password && (
                  <div id="signup-password-error" className="form-error-msg" role="alert">
                    <span>{fieldErrors.password}</span>
                  </div>
                )}
              </div>

              {/* Confirm Password */}
              <div className="login-password-group">
                <label htmlFor="signup-confirm-password" className="form-label">
                  <span>
                    Confirm password <span className="required-star" aria-hidden="true">*</span>
                  </span>
                </label>
                <div className="input-wrapper">
                  <span className="input-icon-left">
                    <Lock size={18} aria-hidden="true" />
                  </span>
                  <input
                    id="signup-confirm-password"
                    type={showConfirmPassword ? 'text' : 'password'}
                    value={confirmPassword}
                    onChange={handleConfirmPasswordChange}
                    placeholder="Re-enter your password"
                    disabled={isLoading}
                    autoComplete="new-password"
                    aria-invalid={!!fieldErrors.confirmPassword}
                    aria-describedby={fieldErrors.confirmPassword ? 'signup-confirm-error' : undefined}
                    className={`form-input has-icon-left has-right-element ${
                      fieldErrors.confirmPassword ? 'has-error' : ''
                    }`.trim()}
                  />
                  <div className="input-element-right">
                    <button
                      type="button"
                      className="password-toggle-btn"
                      onClick={() => setShowConfirmPassword((prev) => !prev)}
                      aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
                    >
                      {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                </div>
                {fieldErrors.confirmPassword && (
                  <div id="signup-confirm-error" className="form-error-msg" role="alert">
                    <span>{fieldErrors.confirmPassword}</span>
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
                Sign up &amp; Continue
              </Button>

              {/* Divider */}
              <div className="auth-or-divider" aria-hidden="true">
                <span className="auth-or-line" />
                <span className="auth-or-label">OR</span>
                <span className="auth-or-line" />
              </div>

              {googleAlertVisible && (
                <Alert
                  type="info"
                  onDismiss={() => setGoogleAlertVisible(false)}
                  className="login-alert-banner"
                >
                  Google registration is coming soon. Please use email &amp; password.
                </Alert>
              )}
              <button
                type="button"
                className="auth-google-btn"
                onClick={() => setGoogleAlertVisible(true)}
              >
                <GoogleLogo size={18} />
                <span>Continue with Google</span>
              </button>

              {/* Footer switch to login */}
              <div className="login-card-footer">
                <span className="login-footer-text">Already have an account?</span>{' '}
                <button
                  type="button"
                  onClick={goToLogin}
                  className="login-signup-link"
                >
                  Log in
                </button>
              </div>
            </form>
          </div>

          <div className="login-security-badge" aria-hidden="true">
            <ShieldCheck size={14} strokeWidth={2} />
            <span>NEXTSTEP AI · Secure student registration</span>
          </div>
        </div>
      </main>
    </div>
  );
}
