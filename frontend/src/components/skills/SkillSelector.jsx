import React, { useState } from 'react';
import { Plus, Check } from 'lucide-react';
import { useOnboarding } from '../../context/OnboardingContext';
import { PRESET_SKILLS } from '../../services/api';
import Button from '../common/Button';

export default function SkillSelector() {
  const { selectedSkills, addSkill, skillsErrors } = useOnboarding();
  const [customInput, setCustomInput] = useState('');

  const isSelected = (skillName) =>
    selectedSkills.some((s) => s.name.toLowerCase() === skillName.toLowerCase());

  const handleAddCustom = (e) => {
    e.preventDefault();
    if (!customInput.trim()) return;
    addSkill(customInput.trim(), 'Intermediate', true);
    setCustomInput('');
  };

  return (
    <div>
      {/* Label row */}
      <div className="section-row-label">
        <span className="srl-title">Popular Technical Skills</span>
        <span className="srl-hint">Click to add</span>
      </div>

      {/* Preset chips */}
      <div className="skill-chips-row" role="group" aria-label="Suggested skills">
        {PRESET_SKILLS.map((skill) => {
          const active = isSelected(skill);
          return (
            <button
              key={skill}
              type="button"
              className={`quick-skill-chip ${active ? 'selected' : ''}`}
              onClick={() => { if (!active) addSkill(skill, 'Intermediate', false); }}
              disabled={active}
              aria-pressed={active}
            >
              {active ? <Check size={13} strokeWidth={3} /> : <Plus size={13} />}
              <span>{skill}</span>
            </button>
          );
        })}
      </div>

      {/* Custom skill input */}
      <div className="custom-skill-bar" onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleAddCustom(e); } }}>
        <input
          type="text"
          className="form-input custom-skill-input"
          placeholder="Add custom skill (e.g. Docker, TypeScript, Flutter)..."
          value={customInput}
          onChange={(e) => setCustomInput(e.target.value)}
          aria-label="Custom skill name"
        />
        <Button
          type="button"
          onClick={handleAddCustom}
          variant="secondary"
          size="sm"
          disabled={!customInput.trim()}
          icon={Plus}
        >
          Add Skill
        </Button>
      </div>

      {skillsErrors.skill && (
        <p className="form-error-msg" style={{ marginTop: '0.5rem' }}>
          {skillsErrors.skill}
        </p>
      )}
    </div>
  );
}
