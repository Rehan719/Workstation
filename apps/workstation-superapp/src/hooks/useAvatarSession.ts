import { useCallback, useEffect, useRef, useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

export interface AvatarMessage {
  role: 'user' | 'assistant';
  content: string;
  imageDataUrl?: string;
  servedBy?: string;     // which OWNED resource answered (in-house provenance)
  isExternal?: boolean;
}

export type AvatarFaceState = 'idle' | 'thinking' | 'speaking';

// Maps the current route to a domain context the backend uses to tailor its
// system prompt (see DOMAIN_PROMPTS in agentic_core/avatars/api.py).
const routeToContext = (pathname: string): string => {
  const map: { prefix: string; context: string }[] = [
    { prefix: '/ceo', context: 'ceo' },
    { prefix: '/capital', context: 'capital' },
    { prefix: '/bto', context: 'bto' },
    { prefix: '/employment', context: 'employment' },
    { prefix: '/realm', context: 'realms' },
    { prefix: '/qep', context: 'domains' },
    { prefix: '/religion', context: 'domains' },
    { prefix: '/science', context: 'domains' },
    { prefix: '/law', context: 'domains' },
    { prefix: '/care', context: 'domains' },
    { prefix: '/education', context: 'domains' },
    { prefix: '/products', context: 'products' },
    { prefix: '/marketplace', context: 'products' },
    { prefix: '/forge', context: 'coe' },
    { prefix: '/factory', context: 'coe' },
    { prefix: '/admin', context: 'entity' },
    { prefix: '/orchestrator', context: 'organism' },
    { prefix: '/introspection', context: 'organism' },
  ];
  const match = map.find(m => pathname.startsWith(m.prefix));
  return match?.context ?? 'general';
};

/**
 * Single shared source of truth for the user<->avatar interaction, lifted out
 * of the old AvatarWidget popup so it can be consumed by three independent
 * footer sections at once: the voice/sound visualizer (left), the rich-text
 * conversation history (center), and the avatar figure (right) — all reading
 * and driving the exact same real session, not three disconnected copies.
 */
export type AiStatus = 'online' | 'offline' | 'checking';

export function useAvatarSession() {
  const location = useLocation();
  const context = routeToContext(location.pathname);

  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<AvatarMessage[]>([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [recording, setRecording] = useState(false);
  const [transcribing, setTranscribing] = useState(false);
  const [speakReplies, setSpeakReplies] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [pendingImage, setPendingImage] = useState<string | null>(null);
  const [notice, setNotice] = useState('');
  const [volume, setVolume] = useState(1);
  const [hasPlayedAudio, setHasPlayedAudio] = useState(false);
  const [aiStatus, setAiStatus] = useState<AiStatus>('checking');

  // Real-time amplitude (0-100), sampled from an actual Web Audio analyser —
  // never randomized/faked. `amplitude` tracks TTS playback, `micAmplitude`
  // tracks the user's live microphone input while recording.
  const [amplitude, setAmplitude] = useState(0);
  const [micAmplitude, setMicAmplitude] = useState(0);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const audioPlayerRef = useRef<HTMLAudioElement | null>(null);
  const audioCtxRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const micAnalyserRef = useRef<AnalyserNode | null>(null);
  const rafRef = useRef<number | null>(null);

  const getAudioContext = () => {
    if (!audioCtxRef.current) {
      audioCtxRef.current = new AudioContext();
    }
    return audioCtxRef.current;
  };

  const checkAiStatus = useCallback(async () => {
    setAiStatus('checking');
    try {
      const res = await axios.get('/api/v1/avatar/status', { timeout: 6000, validateStatus: () => true });
      // The avatar runs on Workstation's OWN native fabric — always online. Provider flags are
      // optional accelerants only, so they no longer gate the status.
      setAiStatus(res.status === 200 && (res.data?.online || res.data?.native || res.data?.ollama_online || res.data?.openai_configured) ? 'online' : 'offline');
    } catch {
      setAiStatus('offline');
    }
  }, []);

  useEffect(() => {
    checkAiStatus();
  }, [checkAiStatus]);

  // Continuous sampling loop — only reads real analyser data, defaults to 0
  // (not a fake idle wobble) whenever there's no actual audio to measure.
  useEffect(() => {
    const sample = () => {
      if (analyserRef.current && speaking) {
        const data = new Uint8Array(analyserRef.current.frequencyBinCount);
        analyserRef.current.getByteFrequencyData(data);
        const avg = data.reduce((a, b) => a + b, 0) / data.length;
        setAmplitude(Math.min(100, Math.round((avg / 255) * 140)));
      } else {
        setAmplitude(0);
      }
      if (micAnalyserRef.current && recording) {
        const data = new Uint8Array(micAnalyserRef.current.frequencyBinCount);
        micAnalyserRef.current.getByteFrequencyData(data);
        const avg = data.reduce((a, b) => a + b, 0) / data.length;
        setMicAmplitude(Math.min(100, Math.round((avg / 255) * 160)));
      } else {
        setMicAmplitude(0);
      }
      rafRef.current = requestAnimationFrame(sample);
    };
    rafRef.current = requestAnimationFrame(sample);
    return () => { if (rafRef.current) cancelAnimationFrame(rafRef.current); };
  }, [speaking, recording]);

  const speakText = useCallback(async (text: string) => {
    try {
      setSpeaking(true);
      const resp = await axios.post('/api/v1/avatar/speak', { text }, { responseType: 'blob' });
      const url = URL.createObjectURL(resp.data);
      const audio = new Audio(url);
      audio.volume = volume;
      audioPlayerRef.current = audio;
      setHasPlayedAudio(true);

      try {
        const ctx = getAudioContext();
        if (ctx.state === 'suspended') await ctx.resume();
        const source = ctx.createMediaElementSource(audio);
        const analyser = ctx.createAnalyser();
        analyser.fftSize = 64;
        source.connect(analyser);
        analyser.connect(ctx.destination);
        analyserRef.current = analyser;
      } catch {
        // Web Audio graph is best-effort visual flair; playback still works without it.
      }

      audio.onended = () => { setSpeaking(false); setAmplitude(0); };
      await audio.play();
    } catch (err: any) {
      setSpeaking(false);
      setNotice(err?.response?.data?.detail || 'Voice output is currently unavailable.');
    }
  }, [volume]);

  const sendMessage = useCallback(async (overrideText?: string) => {
    const text = (overrideText ?? input).trim();
    if (!text && !pendingImage) return;
    setSending(true);
    setNotice('');
    const userMsg: AvatarMessage = { role: 'user', content: text, imageDataUrl: pendingImage || undefined };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    const imageBase64 = pendingImage ? pendingImage.split(',')[1] : undefined;
    setPendingImage(null);
    try {
      const resp = await axios.post('/api/v1/avatar/chat', {
        session_id: sessionId,
        message: text || 'Describe this image.',
        context,
        image_base64: imageBase64,
      });
      if (!sessionId) setSessionId(resp.data.session_id);
      const replyText: string = resp.data.response;
      setMessages(prev => [...prev, {
        role: 'assistant', content: replyText,
        servedBy: resp.data.served_by, isExternal: resp.data.is_external,
      }]);
      if (speakReplies) speakText(replyText);
      setAiStatus('online');
    } catch (err: any) {
      const detail: string =
        err?.response?.data?.detail ||
        (err?.code === 'ECONNREFUSED' || err?.code === 'ERR_NETWORK'
          ? 'Backend server is not running. Start the Workstation API server.'
          : 'Could not reach the avatar backend.');
      setAiStatus('offline');
      setMessages(prev => [...prev, { role: 'assistant', content: detail }]);
    } finally {
      setSending(false);
    }
  }, [input, pendingImage, sessionId, context, speakReplies, speakText]);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      try {
        const ctx = getAudioContext();
        const micSource = ctx.createMediaStreamSource(stream);
        const micAnalyser = ctx.createAnalyser();
        micAnalyser.fftSize = 64;
        micSource.connect(micAnalyser);
        micAnalyserRef.current = micAnalyser;
      } catch {
        // best-effort; recording still works without the live level visual
      }

      const recorder = new MediaRecorder(stream);
      audioChunksRef.current = [];
      recorder.ondataavailable = (e) => audioChunksRef.current.push(e.data);
      recorder.onstop = async () => {
        stream.getTracks().forEach(t => t.stop());
        micAnalyserRef.current = null;
        const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setTranscribing(true);
        try {
          const formData = new FormData();
          formData.append('file', blob, 'recording.webm');
          const resp = await axios.post('/api/v1/avatar/transcribe', formData);
          const text: string = resp.data.text;
          if (text) sendMessage(text);
        } catch (err: any) {
          setNotice(err?.response?.data?.detail || 'Voice transcription is currently unavailable.');
        } finally {
          setTranscribing(false);
        }
      };
      mediaRecorderRef.current = recorder;
      recorder.start();
      setRecording(true);
    } catch {
      setNotice('Microphone access was denied or is unavailable.');
    }
  }, [sendMessage]);

  const stopRecording = useCallback(() => {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  }, []);

  const toggleRecording = useCallback(() => {
    if (recording) stopRecording(); else startRecording();
  }, [recording, startRecording, stopRecording]);

  const handleImageFile = useCallback((file: File) => {
    const reader = new FileReader();
    reader.onload = () => setPendingImage(reader.result as string);
    reader.readAsDataURL(file);
  }, []);

  const clearConversation = useCallback(() => {
    if (sessionId) {
      axios.delete(`/api/v1/avatar/session/${sessionId}`).catch(() => {});
    }
    setMessages([]);
    setSessionId(null);
    setNotice('');
    setHasPlayedAudio(false);
  }, [sessionId]);

  const rewind = useCallback((seconds: number = 5) => {
    const audio = audioPlayerRef.current;
    if (!audio) return;
    audio.currentTime = Math.max(0, audio.currentTime - seconds);
  }, []);

  const setVolumeLevel = useCallback((v: number) => {
    const clamped = Math.max(0, Math.min(1, v));
    setVolume(clamped);
    if (audioPlayerRef.current) audioPlayerRef.current.volume = clamped;
  }, []);

  const faceState: AvatarFaceState = speaking ? 'speaking' : (sending || transcribing) ? 'thinking' : 'idle';

  return {
    context,
    sessionId,
    messages,
    input, setInput,
    sending,
    recording,
    transcribing,
    speakReplies, setSpeakReplies,
    speaking,
    pendingImage, setPendingImage,
    notice, setNotice,
    volume, setVolumeLevel,
    amplitude, micAmplitude,
    canRewind: hasPlayedAudio,
    aiStatus,
    checkAiStatus,
    sendMessage,
    startRecording,
    stopRecording,
    toggleRecording,
    handleImageFile,
    clearConversation,
    rewind,
    speakText,
    faceState,
  };
}

export type UseAvatarSessionReturn = ReturnType<typeof useAvatarSession>;
