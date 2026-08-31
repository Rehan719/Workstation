import { useEffect, useState, useRef } from 'react';

export const useWebSocket = (url: string) => {
  const [data, setData] = useState<any>(null);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    // Always route WS to the backend port (8000), regardless of Vite dev port
    const isLocalDev = window.location.hostname === 'localhost';
    const host = isLocalDev ? 'localhost:8000' : window.location.host;
    try {
      ws.current = new WebSocket(`${protocol}//${host}${url}`);
    } catch (_e) {
      return;
    }

    ws.current.onerror = () => {
      // Backend WS unavailable — component falls back to static data via axios
    };

    ws.current.onmessage = (event) => {
      setData(jsonSafeParse(event.data));
    };

    return () => {
      ws.current?.close();
    };
  }, [url]);

  return data;
};

const jsonSafeParse = (str: string) => {
  try {
    return JSON.parse(str);
  } catch (e) {
    return str;
  }
};
