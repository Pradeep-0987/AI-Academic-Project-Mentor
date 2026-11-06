import React from 'react';

export default function Card({ children, className = '' }) {
  return <div className={`card ${className}`.trim()}>{children}</div>;
}

export function CardHeader({ title, subtitle, badge, action, className = '' }) {
  return (
    <div className={`card-header ${className}`.trim()}>
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '1rem' }}>
        <div>
          {badge && <div style={{ marginBottom: '0.5rem' }}>{badge}</div>}
          {title && <h2 style={{ margin: 0 }}>{title}</h2>}
          {subtitle && (
            <p style={{ marginTop: '0.375rem', fontSize: '0.9375rem', color: 'var(--color-text-secondary)' }}>
              {subtitle}
            </p>
          )}
        </div>
        {action && <div>{action}</div>}
      </div>
    </div>
  );
}

export function CardBody({ children, className = '' }) {
  return <div className={`card-body ${className}`.trim()}>{children}</div>;
}

export function CardFooter({ children, className = '' }) {
  return <div className={`card-footer ${className}`.trim()}>{children}</div>;
}
