import React from 'react';

export default function Badge({
  children,
  variant = 'primary',
  className = '',
  icon: Icon
}) {
  return (
    <span className={`badge badge-${variant} ${className}`.trim()}>
      {Icon && <Icon size={12} aria-hidden="true" />}
      {children}
    </span>
  );
}
