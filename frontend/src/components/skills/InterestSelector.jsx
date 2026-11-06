import React, { useState, useRef } from 'react';
import {
  Brain,
  Globe,
  Smartphone,
  BarChart3,
  ShieldCheck,
  Cloud,
  Cpu,
  MessageSquare,
  Check,
  Plus,
  X,
  Sparkles
} from 'lucide-react';
import { useOnboarding } from '../../context/OnboardingContext';
import { PRESET_INTERESTS } from '../../services/api';
import Button from '../common/Button';

const ICON_MAP = {
  Brain,
  Globe,
  Smartphone,
  BarChart3,
  ShieldCheck,
  Cloud,
  Cpu,
  MessageSquare
};

export default function InterestSelector() {
  const { selectedInterests, toggleInterest, skillsErrors } = useOnboarding();
  const [isOpen, setIsOpen] = useState(false);
  const [customInput, setCustomInput] = useState('');
  const inputRef = useRef(null);

  // Identify any custom interests currently selected (not in preset IDs)
  const presetIds = PRESET_INTERESTS.map((p) => p.id);
  const customInterests = selectedInterests.filter((id) => !presetIds.includes(id));
  const hasCustomSelected = customInterests.length > 0;

  const handleCardClick = (e) => {
    // If click originated from input or action button, do nothing
    if (e.target.closest('input') || e.target.closest('button')) return;

    if (!isOpen) {
      setIsOpen(true);
      setTimeout(() => inputRef.current?.focus(), 50);
    } else if (hasCustomSelected) {
      // Toggle custom interest off if clicked on the card itself
      customInterests.forEach((ci) => toggleInterest(ci));
    }
  };

  const handleAddCustom = (e) => {
    if (e) e.preventDefault();
    const trimmed = customInput.trim();
    if (!trimmed) return;

    if (!selectedInterests.includes(trimmed)) {
      toggleInterest(trimmed);
    }
    setCustomInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddCustom();
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  return (
    <div style={{ marginTop: '2rem' }}>
      <div className="section-row-label">
        <span className="srl-title">Project Areas of Interest</span>
        <span className="srl-hint">
          Select all that apply ({selectedInterests.length} selected)
        </span>
      </div>

      <div className="interests-grid" role="group" aria-label="Project Areas of Interest">
        {/* 8 Preset Interest Options */}
        {PRESET_INTERESTS.map((interest) => {
          const isSelected = selectedInterests.includes(interest.id);
          const IconComp = ICON_MAP[interest.iconName] || Globe;

          return (
            <div
              key={interest.id}
              className={`interest-card ${isSelected ? 'selected' : ''}`}
              onClick={() => toggleInterest(interest.id)}
              onKeyDown={(e) => {
                if (e.key === ' ' || e.key === 'Enter') {
                  e.preventDefault();
                  toggleInterest(interest.id);
                }
              }}
              tabIndex={0}
              role="checkbox"
              aria-checked={isSelected}
            >
              <div className="interest-checkbox" aria-hidden="true">
                {isSelected && <Check size={12} strokeWidth={3} />}
              </div>

              <div className="interest-card-content">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <IconComp size={15} style={{ color: isSelected ? 'var(--color-primary)' : 'var(--color-text-muted)' }} />
                  <span className="interest-card-title">{interest.title}</span>
                </div>
                <span className="interest-card-desc">{interest.description}</span>
              </div>
            </div>
          );
        })}

        {/* 9th Optional Card: + Add your own interest */}
        <div
          className={`interest-card custom-interest-card ${hasCustomSelected ? 'selected' : ''} ${isOpen ? 'is-open' : ''}`}
          onClick={handleCardClick}
          tabIndex={0}
          role="checkbox"
          aria-checked={hasCustomSelected}
        >
          <div className="interest-checkbox" aria-hidden="true">
            {hasCustomSelected && <Check size={12} strokeWidth={3} />}
          </div>

          <div className="interest-card-content" style={{ width: '100%' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <Plus size={15} style={{ color: hasCustomSelected ? 'var(--color-primary)' : 'var(--color-text-muted)' }} />
                <span className="interest-card-title">+ Add your own interest</span>
              </div>
              {!isOpen && !hasCustomSelected && (
                <span style={{ fontSize: '0.6875rem', color: 'var(--color-sage-mid)', fontWeight: 600 }}>Optional</span>
              )}
            </div>

            {!isOpen && !hasCustomSelected && (
              <span className="interest-card-desc">Specify a custom domain or research topic</span>
            )}

            {/* Render selected custom interest chips */}
            {customInterests.length > 0 && (
              <div className="custom-interest-chips">
                {customInterests.map((ci) => (
                  <span key={ci} className="custom-interest-tag">
                    <span>{ci}</span>
                    <button
                      type="button"
                      className="custom-interest-tag-remove"
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleInterest(ci);
                      }}
                      aria-label={`Remove custom interest ${ci}`}
                    >
                      <X size={12} />
                    </button>
                  </span>
                ))}
              </div>
            )}

            {/* Input field revealed when selected / open */}
            {isOpen && (
              <div className="custom-interest-input-row" onClick={(e) => e.stopPropagation()}>
                <input
                  ref={inputRef}
                  type="text"
                  className="form-input custom-interest-input"
                  placeholder="e.g. Quantum Computing, AR/VR..."
                  value={customInput}
                  onChange={(e) => setCustomInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  aria-label="Custom project area of interest"
                />
                <Button
                  type="button"
                  variant="primary"
                  size="sm"
                  disabled={!customInput.trim()}
                  onClick={handleAddCustom}
                >
                  Add
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>

      {skillsErrors.interests && (
        <p className="form-error-msg" style={{ marginTop: '0.625rem' }}>
          {skillsErrors.interests}
        </p>
      )}
    </div>
  );
}
