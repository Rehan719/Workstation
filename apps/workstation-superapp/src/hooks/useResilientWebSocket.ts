import { useState, useEffect, useRef } from 'react';

export const useResilientWebSocket = (url: string, onMessage: (data: any) => void) => {
  const ws = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<number | null>(null);
  const [status, setStatus] = useState<'CONNECTING' | 'CONNECTED' | 'DISCONNECTED'>('DISCONNECTED');
  const retryCount = useRef(0);

  const connect = () => {
    if (
      ws.current?.readyState === WebSocket.OPEN ||
      ws.current?.readyState === WebSocket.CONNECTING
    ) return;

    setStatus('CONNECTING');
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      setStatus('CONNECTED');
      retryCount.current = 0;
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (e) {
        console.error('WebSocket message parse error:', e);
      }
    };

    ws.current.onclose = () => {
      setStatus('DISCONNECTED');

      // Exponential backoff
      const delay = Math.min(1000 * Math.pow(2, retryCount.current), 30000);
      retryCount.current++;

      reconnectTimeout.current = window.setTimeout(connect, delay);
    };

    ws.current.onerror = () => {
      ws.current?.close();
    };
  };

  useEffect(() => {
    // Deferred so React 18 StrictMode's mount->cleanup->mount dev-only
    // double-invoke cancels this before a real socket ever opens, instead
    // of opening one and immediately closing it mid-handshake.
    const connectTimeout = window.setTimeout(connect, 0);
    return () => {
      clearTimeout(connectTimeout);
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
      if (ws.current) {
        ws.current.onclose = null; // Prevent reconnect on unmount
        ws.current.close();
      }
    };
  }, [url]);

  return { status };
};
