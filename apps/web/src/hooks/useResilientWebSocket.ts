import { useState, useEffect, useRef } from 'react';

export const useResilientWebSocket = (url: string, onMessage: (data: any) => void) => {
  const ws = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<number | null>(null);

  const connect = () => {
    console.log('Connecting to WebSocket:', url);
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log('Sovereign Stream Connected');
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
      reconnectTimeout.current = window.setTimeout(connect, 3000);
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
      ws.current?.close();
    };
  }, [url]);
};
