import React from 'react';

export type AvatarFaceState = 'idle' | 'thinking' | 'speaking';

interface AvatarFaceProps {
  /** Fixed pixel size. Omit to have the SVG fill its parent container instead
   * (used by the footer's persistent figure, which auto-sizes to its column). */
  size?: number;
  state?: AvatarFaceState;
  /** Real 0-100 amplitude sampled from the actual TTS audio (see
   * useAvatarSession) — drives genuine lip-sync-style mouth openness while
   * speaking, instead of a generic looping animation. */
  amplitude?: number;
  className?: string;
}

/**
 * A small biomimetic SVG character: gradient-shaded organic head + shoulders,
 * blinking/wandering eyes, breathing torso, micro-moving brows, and a mouth
 * that opens in proportion to real audio amplitude while `state="speaking"`.
 * Built from CSS/SVG (no external image asset or image-generation API — both
 * configured providers are currently blocked, see agentic_core/avatars/api.py)
 * so it's a genuinely live, animated render rather than a static icon or a
 * faked "photo".
 */
export const AvatarFace: React.FC<AvatarFaceProps> = ({ size, state = 'idle', amplitude = 0, className = '' }) => {
  const speaking = state === 'speaking';
  const thinking = state === 'thinking';

  // Real lip-sync: mouth openness buckets directly off the live amplitude
  // sample, not a fixed-rate animation — silence keeps the mouth nearly
  // closed even while `speaking` is technically true (e.g. between words).
  const mouthRy = !speaking ? 6 : amplitude > 55 ? 9.5 : amplitude > 28 ? 7 : amplitude > 6 ? 4.5 : 2.5;
  const mouthRx = !speaking ? 7 : amplitude > 55 ? 8.5 : 7;

  const sizeProps = size ? { width: size, height: size } : { className: 'w-full h-full' };

  return (
    <svg
      {...sizeProps}
      viewBox="0 0 100 100"
      className={`avatar-sway origin-bottom animate-avatar-sway drop-shadow-[0_6px_14px_rgba(100,255,218,0.3)] ${size ? '' : 'w-full h-full'} ${className}`}
      role="img"
      aria-label={speaking ? 'Avatar speaking' : thinking ? 'Avatar thinking' : 'Avatar idle'}
    >
      <defs>
        <radialGradient id="avatarHalo" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stopColor="#64ffda" stopOpacity="0.35" />
          <stop offset="100%" stopColor="#64ffda" stopOpacity="0" />
        </radialGradient>
        <linearGradient id="avatarHead" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#9dffe9" />
          <stop offset="55%" stopColor="#64ffda" />
          <stop offset="100%" stopColor="#1f9b85" />
        </linearGradient>
        <linearGradient id="avatarShoulders" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#1f9b85" />
          <stop offset="100%" stopColor="#0c4a3d" />
        </linearGradient>
      </defs>

      {/* Ambient halo */}
      <circle cx="50" cy="42" r="46" fill="url(#avatarHalo)" />

      {/* Breathing group: head + shoulders rise and fall together */}
      <g className="origin-center animate-avatar-breathe">
        {/* Shoulders / body language */}
        <path d="M18 96 Q50 74 82 96 L82 100 L18 100 Z" fill="url(#avatarShoulders)" />
        {/* Bio-luminescent core — a faint, slowly pulsing inner light, like a heartbeat */}
        <ellipse cx="50" cy="88" rx="5" ry="3.5" fill="#9dffe9" opacity="0.5" className="animate-pulse-subtle" />

        {/* Arms — relaxed at idle/speaking, one rises toward the chin in a
            "thinking" gesture for genuine body-language readability */}
        <path d="M22 94 Q12 84 16 70" stroke="url(#avatarShoulders)" strokeWidth="7" strokeLinecap="round" fill="none" />
        {thinking ? (
          <path d="M78 94 Q86 70 64 56" stroke="url(#avatarShoulders)" strokeWidth="7" strokeLinecap="round" fill="none" className="transition-all duration-500" />
        ) : (
          <path d="M78 94 Q88 84 84 70" stroke="url(#avatarShoulders)" strokeWidth="7" strokeLinecap="round" fill="none" className="transition-all duration-500" />
        )}
        {thinking && (
          <circle cx="63" cy="54" r="5.5" fill="url(#avatarShoulders)" className="animate-in fade-in duration-300" />
        )}

        {/* Head group — tilts slightly when thinking, for added body language */}
        <g className={`origin-center transition-transform duration-500 ${thinking ? '[transform:rotate(-4deg)]' : ''}`}>
          {/* Head — softly irregular/organic silhouette, not a sharp geometric shape */}
          <path
            d="M50 8
               C68 8 80 22 80 42
               C80 60 70 74 50 76
               C30 74 20 60 20 42
               C20 22 32 8 50 8 Z"
            fill="url(#avatarHead)"
          />
          {/* Glossy highlight for a softer, less flat / "finer" rendered look */}
          <ellipse cx="38" cy="26" rx="12" ry="8" fill="white" opacity="0.18" />
          {/* Cheek shading for dimensionality */}
          <ellipse cx="30" cy="52" rx="6" ry="4" fill="#0c4a3d" opacity="0.12" />
          <ellipse cx="70" cy="52" rx="6" ry="4" fill="#0c4a3d" opacity="0.12" />

          {/* Eyebrows — subtle, slightly raised when thinking, with a small
              continuous idle micro-motion so the face never looks frozen */}
          <g className="animate-avatar-brow">
            <path
              d={thinking ? 'M30 33 Q36 28 42 32' : 'M30 32 Q36 29 42 32'}
              stroke="#06291f"
              strokeWidth="2.2"
              strokeLinecap="round"
              fill="none"
              opacity="0.55"
            />
            <path
              d={thinking ? 'M58 32 Q64 29 70 33' : 'M58 32 Q64 29 70 32'}
              stroke="#06291f"
              strokeWidth="2.2"
              strokeLinecap="round"
              fill="none"
              opacity="0.55"
            />
          </g>

          {/* Eyes — blink via scaleY, pupils wander via translateX */}
          <g className="origin-center animate-avatar-blink">
            <ellipse cx="38" cy="42" rx="6.5" ry="7.5" fill="#06291f" />
            <ellipse cx="62" cy="42" rx="6.5" ry="7.5" fill="#06291f" />
          </g>
          <g className="animate-avatar-look">
            <circle cx="39.5" cy="41" r="2.2" fill="#9dffe9" />
            <circle cx="63.5" cy="41" r="2.2" fill="#9dffe9" />
          </g>

          {/* Mouth — calm curve at idle, flatter when thinking; while speaking
              its openness tracks real TTS amplitude (genuine lip-sync, not a
              fixed-rate loop) */}
          {speaking ? (
            <ellipse cx="50" cy="60" rx={mouthRx} ry={mouthRy} fill="#06291f" className="transition-[ry,rx] duration-100" />
          ) : (
            <path
              d={thinking ? 'M42 60 Q50 60 58 58' : 'M40 58 Q50 66 60 58'}
              stroke="#06291f"
              strokeWidth="2.6"
              strokeLinecap="round"
              fill="none"
            />
          )}
        </g>
      </g>
    </svg>
  );
};
