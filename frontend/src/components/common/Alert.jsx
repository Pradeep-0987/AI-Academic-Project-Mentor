import React from 'react';
import { AlertCircle, CheckCircle2, Info, AlertTriangle, X } from 'lucide-react';

export default function Alert({
  type = 'info',
  title,
  children,
  onDismiss,
  className = ''
}) {
  const icons = {
    info: Info,
    success: CheckCircle2,
    warning: AlertTriangle,
    error: AlertCircle
  };

  const IconComponent = icons[type] || Info;

  return (
    <div className={`alert alert-${type} ${className}`.trim()} role="alert">
      <IconComponent size={20} style={{ flexShrink: 0, marginTop: '2px' }} aria-hidden="true" />
      <div style={{ flex: 1, minWidth: 0 }}>
        {title && <div style={{ fontWeight: 600, marginBottom: '0.125rem' }}>{title}</div>}
        <div>{children}</div>
      </div>
      {onDismiss && (
        <button
          type="button"
          onClick={onDismiss}
          style={{
            background: 'none',
            border: 'none',
            color: 'currentColor',
            opacity: 0.7,
            cursor: 'pointer',
            padding: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
          aria-label="Dismiss alert"
        >
          <X size={16} />
        </button>
      )}
    </div>
  );
}
