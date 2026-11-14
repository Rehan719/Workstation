// W1008 - ONE READER OF A STREAMED ANSWER. Three pages (the Intelligence Lab, the Design & Dev engine and the Authorship
// engine) each carried their own copy of this, and each copy said a refusal by its status alone ("HTTP 422") and a
// server it could not reach in the browser's words ("Failed to fetch"). A refusal now says the server's status and
// reason, a field check (which answers a list) by its field; an answer that carries no stream says so; and a server
// that cannot be reached is said as one, the way every page says it.
import { axiosDetail, bodyOrNull, errorMessage } from './api';
import { silenceIsRight } from '../components/ReadFailures';

/** POST `body` to `url` and hand each `data:` frame of the streamed answer to `onChunk`, then call `onDone`. A refusal,
 *  an answer with no stream, or a server that cannot be reached goes to `onError` as one sentence. */
export async function streamPost<E>(
  url: string,
  body: object,
  onChunk: (ev: E) => void,
  onDone: () => void,
  onError: (e: string) => void,
): Promise<void> {
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const d = await bodyOrNull(res);
      onError(`Failed (HTTP ${res.status}): ${axiosDetail({ response: { data: d } }, 'no reason given')}`);
      return;
    }
    if (!res.body) { onError('The server answered without a stream, so nothing ran here.'); return; }
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let buf = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop()!;
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const raw = line.slice(6).trim();
          if (raw === '[DONE]') continue;
          try { onChunk(JSON.parse(raw) as E); } catch { silenceIsRight('a stream frame that is not JSON, a heartbeat or a cut line, carries nothing to show')(); }
        }
      }
    }
    onDone();
  } catch (e) {
    onError(errorMessage(e));
  }
}
