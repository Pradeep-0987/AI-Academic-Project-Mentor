import React from 'react';
import { Code2 } from 'lucide-react';

export default function EmptySkillState() {
  return (
    <div className="empty-skill-state" role="status">
      <div className="empty-skill-icon" aria-hidden="true">
        <Code2 size={18} />
      </div>
      <span style={{ fontWeight: 600, color: 'var(--color-text-body)', fontSize: '0.875rem' }}>
        No technical skills selected yet
      </span>
      <p style={{ margin: 0, fontSize: '0.8125rem' }}>
        Click on the popular skills above or add a custom one below to begin your skill profile.
      </p>
    </div>
  );
}
