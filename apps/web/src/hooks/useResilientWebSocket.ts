import { useState, useEffect, useRef } from 'react';

export const useResilientWebSocket = (url: string, onMessage: (data: any) => void) => {
  const ws = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<number | null>(null);
  const [status, setStatus] = useState<'CONNECTING' | 'CONNECTED' | 'DISCONNECTED'>('DISCONNECTED');
  const retryCount = useRef(0);

  const connect = async () => {
    if (ws.current?.readyState === WebSocket.OPEN) return;

    // v1.0: Wait for backend health before connecting
    try {
      const resp = await fetch('/api/v154/status');
      if (!resp.ok) throw new Error('Backend not ready');
    } catch (e) {
      console.log('Backend not ready, delaying WebSocket connection...');
      const delay = Math.min(1000 * Math.pow(2, retryCount.current), 30000);
      reconnectTimeout.current = window.setTimeout(connect, delay);
      return;
    }

    console.log('Connecting to WebSocket:', url);
    setStatus('CONNECTING');
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log('Sovereign Stream Connected');
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
      console.log('Sovereign Stream Disconnected. Reconnecting...');
      setStatus('DISCONNECTED');

      // Exponential backoff
      const delay = Math.min(1000 * Math.pow(2, retryCount.current), 30000);
      retryCount.current++;

      reconnectTimeout.current = window.setTimeout(connect, delay);
    };

    ws.current.onerror = (err) => {
      console.error('WebSocket Error:', err);
      ws.current?.close();
    };
  };

  useEffect(() => {
    connect();
    return () => {
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
      if (ws.current) {
        ws.current.onclose = null; // Prevent reconnect on unmount
        ws.current.close();
      }
    };
  }, [url]);

  return { status };
};
