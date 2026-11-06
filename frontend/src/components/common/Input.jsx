import React from 'react';
import { AlertCircle } from 'lucide-react';

export default function Input({
  id,
  label,
  type = 'text',
  value,
  onChange,
  placeholder,
  required = false,
  optionalHint,
  error,
  helperText,
  icon: Icon,
  disabled = false,
  autoComplete,
  className = '',
  rightElement,
  ...props
}) {
  const inputId = id || (label ? `input-${label.toLowerCase().replace(/\s+/g, '-')}` : undefined);

  return (
    <div className={`form-group ${className}`}>
      {label && (
        <label htmlFor={inputId} className="form-label">
          <span>
            {label}
            {required && <span className="required-star" aria-hidden="true">*</span>}
          </span>
          {optionalHint && <span className="optional-hint">{optionalHint}</span>}
        </label>
      )}

      <div className="input-wrapper">
        {Icon && (
          <span className="input-icon-left">
            <Icon size={18} aria-hidden="true" />
          </span>
        )}
        <input
          id={inputId}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          disabled={disabled}
          autoComplete={autoComplete}
          aria-invalid={!!error}
          aria-describedby={error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined}
          className={`form-input ${Icon ? 'has-icon-left' : ''} ${rightElement ? 'has-right-element' : ''} ${error ? 'has-error' : ''}`.trim()}
          {...props}
        />
        {rightElement && (
          <div className="input-element-right">
            {rightElement}
          </div>
        )}
      </div>

      {error ? (
        <div id={`${inputId}-error`} className="form-error-msg" role="alert">
          <AlertCircle size={14} aria-hidden="true" />
          <span>{error}</span>
        </div>
      ) : helperText ? (
        <p id={`${inputId}-helper`} className="form-helper-text">
          {helperText}
        </p>
      ) : null}
    </div>
  );
}
