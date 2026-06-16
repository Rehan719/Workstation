import React from 'react';
import { Volume2, VolumeX, RotateCcw } from 'lucide-react';
import { heightPercentClass } from '../../lib/progressWidth';
import type { UseAvatarSessionReturn } from '../../hooks/useAvatarSession';

interface VoiceVisualizerProps {
  avatar: UseAvatarSessionReturn;
}

// Five literal idle-state bar classes (decorative "ready" pulse, same honest
// pattern as the Channels equalizer icon — clearly idle, never pretending to
// be live audio when there's nothing to measure).
const IDLE_BAR_CLASSES = [
  'h-[20%] [animation-delay:0ms] [animation-duration:1.1s]',
  'h-[30%] [animation-delay:120ms] [animation-duration:0.9s]',
  'h-[45%] [animation-delay:240ms] [animation-duration:0.75s]',
  'h-[30%] [animation-delay:360ms] [animation-duration:0.95s]',
  'h-[20%] [animation-delay:480ms] [animation-duration:1.05s]',
];

// Shapes the one real amplitude signal across 5 bars like a graphic
// equalizer (center-weighted) — still entirely derived from the real value,
// not fabricated per-bar data.
const BAR_WEIGHTS = [0.4, 0.7, 1, 0.7, 0.4];

/**
 * Footer-left "voice/sound avatar interaction display" — a real-time visual
 * of the actual user<->avatar audio channel (TTS playback level while the
 * avatar speaks, live mic level while the user records), plus real playback
 * controls: volume (sets the actual <audio> element's volume) and a 5s
 * rewind of the last spoken reply. Fills its column height/width.
 */
export const VoiceVisualizer: React.FC<VoiceVisualizerProps> = ({ avatar }) => {
  const { speaking, recording, amplitude, micAmplitude, volume, setVolumeLevel, rewind, canRewind } = avatar;

  const isLive = speaking || recording;
  const liveValue = speaking ? amplitude : recording ? micAmplitude : 0;
  const barColor = speaking ? 'text-aura' : 'text-emerald-400';
  const statusLabel = speaking ? 'Avatar speaking' : recording ? 'Listening' : 'Idle';

  return (
    <div className="h-full w-full flex flex-col gap-2 min-h-0 min-w-0">
      <div className="flex-1 flex items-end justify-center gap-1.5 min-h-0 px-1" role="img" aria-label={`Voice interaction level: ${statusLabel}`}>
        {BAR_WEIGHTS.map((w, i) =>
          isLive ? (
            <span
              key={i}
              aria-hidden="true"
              className={`w-2 flex-1 max-w-3 origin-bottom rounded-full bg-current transition-[height] duration-100 ${barColor} ${heightPercentClass(Math.max(10, Math.round(liveValue * w)))}`}
            />
          ) : (
            <span
              key={i}
              aria-hidden="true"
              className={`w-2 flex-1 max-w-3 origin-bottom rounded-full bg-current text-slate-700 animate-eq-bar ${IDLE_BAR_CLASSES[i]}`}
            />
          )
        )}
      </div>

      <div className="flex items-center gap-2 shrink-0">
        <span className={`text-[8px] font-black uppercase tracking-widest truncate ${isLive ? barColor : 'text-slate-600'}`}>
          {statusLabel}
        </span>
      </div>

      <div className="flex items-center gap-2 shrink-0">
        <button
          type="button"
          onClick={() => rewind(5)}
          disabled={!canRewind}
          aria-label="Rewind avatar's last reply 5 seconds"
          title="Rewind 5s"
          className="shrink-0 p-1.5 rounded-lg text-slate-500 hover:text-aura disabled:opacity-30 disabled:hover:text-slate-500 transition-colors"
        >
          <RotateCcw size={13} />
        </button>

        {volume === 0 ? <VolumeX size={13} className="shrink-0 text-slate-600" /> : <Volume2 size={13} className="shrink-0 text-slate-600" />}
        <input
          type="range"
          min={0}
          max={1}
          step={0.05}
          value={volume}
          onChange={(e) => setVolumeLevel(parseFloat(e.target.value))}
          aria-label="Avatar voice volume"
          className="flex-1 min-w-0 h-1 accent-aura cursor-pointer"
        />
      </div>
    </div>
  );
};
