import { useEffect, useState, useRef } from 'react';

export const useWebSocket = (url: string) => {
  const [data, setData] = useState<any>(null);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host === 'localhost:5173' ? 'localhost:8000' : window.location.host;
    ws.current = new WebSocket(`${protocol}//${host}${url}`);

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
