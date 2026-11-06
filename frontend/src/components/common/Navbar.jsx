import React from 'react';
import { RotateCcw } from 'lucide-react';
import { useOnboarding } from '../../context/OnboardingContext';
import NextstepLogo from './NextstepLogo';

export default function Navbar() {
  const { resetForm } = useOnboarding();

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <div className="brand-wrapper">
          <NextstepLogo />
        </div>

        <button
          type="button"
          className="navbar-reset-btn"
          onClick={resetForm}
          title="Reset form"
          aria-label="Reset form"
        >
          <RotateCcw size={14} aria-hidden="true" />
          <span>Reset</span>
        </button>
      </div>
    </header>
  );
}
