import React from 'react';
import { X, Sparkles, CheckCircle, BarChart } from 'lucide-react';
import { useOnboarding } from '../../context/OnboardingContext';
import EmptySkillState from './EmptySkillState';
import Badge from '../common/Badge';

const LEVELS = [
  { id: 'Beginner', label: 'Beginner', desc: 'Basics & coursework' },
  { id: 'Intermediate', label: 'Intermediate', desc: 'Comfortable with projects' },
  { id: 'Advanced', label: 'Advanced', desc: 'Production / complex systems' }
];

export default function SelectedSkillList() {
  const { selectedSkills, removeSkill, updateSkillLevel, skillsErrors } = useOnboarding();

  return (
    <div style={{ marginBottom: '2rem' }}>
      <div className="section-row-label">
        <span className="srl-title">
          Selected Skills & Proficiency ({selectedSkills.length})
        </span>
        <span className="srl-hint">
          Assign your comfort level
        </span>
      </div>

      {selectedSkills.length === 0 ? (
        <EmptySkillState />
      ) : (
        <div className="selected-skills-container" role="list">
          {selectedSkills.map((skill) => (
            <div key={skill.name} className="skill-item-row" role="listitem">
              <div className="skill-item-info">
                <span className="skill-item-name">{skill.name}</span>
                {skill.isCustom && (
                  <Badge variant="neutral" style={{ fontSize: '0.6875rem', padding: '0.15rem 0.4rem' }}>
                    Custom
                  </Badge>
                )}
              </div>

              <div className="skill-item-actions" style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div
                  className="proficiency-segmented-control"
                  role="radiogroup"
                  aria-label={`Proficiency level for ${skill.name}`}
                >
                  {LEVELS.map((lvl) => {
                    const isLevelActive = skill.level === lvl.id;
                    return (
                      <button
                        key={lvl.id}
                        type="button"
                        role="radio"
                        aria-checked={isLevelActive}
                        title={`${lvl.label}: ${lvl.desc}`}
                        className={`proficiency-pill ${isLevelActive ? `active ${lvl.id.toLowerCase()}` : ''}`}
                        onClick={() => updateSkillLevel(skill.name, lvl.id)}
                      >
                        {lvl.label}
                      </button>
                    );
                  })}
                </div>

                <button
                  type="button"
                  className="skill-remove-btn"
                  onClick={() => removeSkill(skill.name)}
                  aria-label={`Remove skill ${skill.name}`}
                  title={`Remove ${skill.name}`}
                >
                  <X size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {skillsErrors.skills && (
        <p className="form-error-msg" style={{ marginTop: '0.625rem' }}>
          {skillsErrors.skills}
        </p>
      )}
    </div>
  );
}
