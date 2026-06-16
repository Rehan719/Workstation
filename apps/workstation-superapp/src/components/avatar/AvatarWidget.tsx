import React from 'react';
import { Mic, Square, Loader2 } from 'lucide-react';
import { AvatarFace } from './AvatarFace';
import type { UseAvatarSessionReturn } from '../../hooks/useAvatarSession';

interface AvatarWidgetProps {
  avatar: UseAvatarSessionReturn;
}

/**
 * The persistent avatar figure — fills its footer column, shows real
 * expression/body-language state (idle/thinking/speaking, with genuine
 * audio-amplitude-driven mouth movement while speaking), and doubles as a
 * one-click voice-input shortcut. The actual text conversation lives in the
 * footer's center ConversationPanel, fed by the same shared `avatar` session.
 */
export const AvatarWidget: React.FC<AvatarWidgetProps> = ({ avatar }) => {
  const { faceState, amplitude, recording, transcribing, toggleRecording, context } = avatar;

  return (
    <div className="relative h-full w-full flex flex-col items-center justify-center gap-2 min-h-0 min-w-0">
      <button
        type="button"
        onClick={toggleRecording}
        disabled={transcribing}
        aria-label={recording ? 'Stop voice message to avatar' : 'Start voice message to avatar'}
        title={recording ? 'Stop voice message to avatar' : 'Start voice message to avatar'}
        className="relative flex-1 w-full max-w-[180px] aspect-square min-h-0 p-3 flex items-center justify-center rounded-3xl bg-gradient-to-br from-[#9dffe9]/10 via-aura/5 to-[#1f9b85]/10 ring-1 ring-aura/20 hover:ring-aura/40 hover:scale-[1.02] active:scale-95 transition-all disabled:opacity-60"
      >
        <div className="w-full h-full">
          <AvatarFace state={faceState} amplitude={amplitude} />
        </div>

        {recording && (
          <span className="absolute top-2.5 right-2.5 w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse" aria-hidden="true" />
        )}
        {transcribing && (
          <span className="absolute bottom-2.5 right-2.5" aria-hidden="true">
            <Loader2 size={14} className="animate-spin text-aura" />
          </span>
        )}
      </button>

      <div className="flex items-center gap-1.5 shrink-0">
        {recording ? <Square size={10} className="text-red-400" /> : <Mic size={10} className="text-slate-600" />}
        <span className="text-[8px] font-black uppercase tracking-widest text-slate-600 truncate">{context}</span>
      </div>
    </div>
  );
};
