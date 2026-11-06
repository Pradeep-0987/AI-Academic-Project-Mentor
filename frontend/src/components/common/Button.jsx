import React from 'react';

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  type = 'button',
  loading = false,
  disabled = false,
  icon: Icon,
  iconPosition = 'left',
  onClick,
  className = '',
  ...props
}) {
  const sizeClass = size === 'sm' ? 'btn-sm' : size === 'lg' ? 'btn-lg' : '';
  const variantClass = `btn-${variant}`;

  return (
    <button
      type={type}
      className={`btn ${variantClass} ${sizeClass} ${className}`.trim()}
      disabled={disabled || loading}
      onClick={onClick}
      {...props}
    >
      {loading ? (
        <>
          <span className="spinner" aria-hidden="true" />
          <span>Processing...</span>
        </>
      ) : (
        <>
          {Icon && iconPosition === 'left' && (
            <Icon size={size === 'sm' ? 14 : size === 'lg' ? 20 : 16} aria-hidden="true" />
          )}
          {children}
          {Icon && iconPosition === 'right' && (
            <Icon size={size === 'sm' ? 14 : size === 'lg' ? 20 : 16} aria-hidden="true" />
          )}
        </>
      )}
    </button>
  );
}
