export function NextstepMark({ size = 38, className = '' }) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 40 40"
      fill="none"
      role="img"
      aria-label="NEXTSTEP AI progress mark"
    >
      <rect x="1" y="1" width="38" height="38" rx="12" fill="url(#nextstep-gradient)" />
      <path d="M10 28h7v-6h6v-6h7" stroke="white" strokeWidth="2.8" strokeLinecap="round" strokeLinejoin="round" />
      <path d="m25.5 11 5.5 0 0 5.5" stroke="white" strokeWidth="2.8" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="10" cy="28" r="2" fill="#7DD3FC" />
      <circle cx="17" cy="22" r="1.7" fill="#C4B5FD" />
      <circle cx="23" cy="16" r="1.7" fill="#C4B5FD" />
      <circle cx="31" cy="11" r="2" fill="#7DD3FC" />
      <defs>
        <linearGradient id="nextstep-gradient" x1="4" y1="3" x2="37" y2="38" gradientUnits="userSpaceOnUse">
          <stop stopColor="#4338CA" />
          <stop offset="1" stopColor="#7C3AED" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export default function NextstepLogo({ size = 38, className = '' }) {
  return (
    <span className={`nextstep-logo ${className}`}>
      <NextstepMark size={size} />
      <span className="nextstep-logo-copy">
        <strong>NEXTSTEP <i>AI</i></strong>
        <small>Every Step Builds Success.</small>
      </span>
    </span>
  );
}
