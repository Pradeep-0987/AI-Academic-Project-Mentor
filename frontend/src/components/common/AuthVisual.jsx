import { Sparkles } from 'lucide-react';
import { NextstepMark } from './NextstepLogo';

export default function AuthVisual() {
  return (
    <aside className="auth-visual" aria-label="NEXTSTEP AI">
      <div className="auth-visual-brand">
        <NextstepMark size={39} className="auth-visual-brand-icon" />
        <span>NEXTSTEP AI</span>
      </div>
      <div className="auth-visual-copy">
        <span className="auth-visual-kicker"><Sparkles size={14} /> PLAN SMART. BUILD BETTER. ACHIEVE MORE.</span>
        <h2>Your Next Big Idea Starts Here.</h2>
        <p>Plan smarter, track progress, and build projects with AI-powered guidance.</p>
      </div>
      <div className="auth-visual-art" aria-hidden="true">
        <img src="/nextstep-hero.svg" alt="" />
        <span className="auth-visual-art-caption"><Sparkles size={14} /> A smarter path from idea to impact</span>
      </div>
      <div className="auth-visual-foot"><span>Plan with purpose</span><i /><span>Build with confidence</span><i /><span>Grow as you go</span></div>
    </aside>
  );
}
