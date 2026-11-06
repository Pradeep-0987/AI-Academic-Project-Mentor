import React from 'react';
import { AlertCircle } from 'lucide-react';

export default function Select({
  id,
  label,
  value,
  onChange,
  options = [],
  placeholder = 'Select an option',
  required = false,
  optionalHint,
  error,
  helperText,
  icon: Icon,
  disabled = false,
  className = '',
  ...props
}) {
  const selectId = id || (label ? `select-${label.toLowerCase().replace(/\s+/g, '-')}` : undefined);

  return (
    <div className={`form-group ${className}`}>
      {label && (
        <label htmlFor={selectId} className="form-label">
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
        <select
          id={selectId}
          value={value}
          onChange={onChange}
          disabled={disabled}
          aria-invalid={!!error}
          aria-describedby={error ? `${selectId}-error` : helperText ? `${selectId}-helper` : undefined}
          className={`form-select ${Icon ? 'has-icon-left' : ''} ${error ? 'has-error' : ''}`.trim()}
          {...props}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((opt) => {
            const val = typeof opt === 'object' ? opt.value : opt;
            const lbl = typeof opt === 'object' ? opt.label : opt;
            return (
              <option key={val} value={val}>
                {lbl}
              </option>
            );
          })}
        </select>
      </div>

      {error ? (
        <div id={`${selectId}-error`} className="form-error-msg" role="alert">
          <AlertCircle size={14} aria-hidden="true" />
          <span>{error}</span>
        </div>
      ) : helperText ? (
        <p id={`${selectId}-helper`} className="form-helper-text">
          {helperText}
        </p>
      ) : null}
    </div>
  );
}
