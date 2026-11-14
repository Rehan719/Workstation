// W1013 — one reading of a refusal. A route that refuses answers a `detail` whose shape is the route's: a sentence, a
// field check's list of {loc, msg} (FastAPI's 422, the shape test_w1013 reads off a real route), or a structured
// refusal's object. Every page reads it through one helper, so a field check is said by its field wherever it lands:
// the shared fetch helper (apiJson) said one as JSON text, and twenty-two readers said the status alone.
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ApiError, apiJson, axiosDetail, bodyDetail } from './api';
import { errorMessage } from './api';   // W1015 - W1013's guard holds the line above as its own
import { whoami } from './auth';

const FIELD_CHECK = { detail: [{ type: 'missing', loc: ['body', 'title'], msg: 'Field required', input: {} }] };
const reply = (status: number, body: unknown, statusText = '') =>
  ({ ok: status < 400, status, statusText, json: async () => body });

describe('one reading of a refusal', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('reads a sentence as itself, a field check by its field, an object by its message', () => {
    expect(bodyDetail({ detail: 'the plan could not be read' }, 'none')).toBe('the plan could not be read');
    expect(bodyDetail(FIELD_CHECK, 'none')).toBe('title: Field required');
    expect(bodyDetail({ detail: { message: 'a release needs two signatures' } }, 'none')).toBe('a release needs two signatures');
    expect(bodyDetail({ detail: { error: 'kpi_gate', basis: 'two objectives carry no KPI' } }, 'none')).toBe('kpi_gate');
    expect(bodyDetail(null, 'none')).toBe('none');
    expect(bodyDetail({}, 'none')).toBe('none');
  });

  it('is the reading an axios error gets', () => {
    for (const body of [FIELD_CHECK, { detail: 'a sentence' }, { detail: { note: 'held for review' } }, null]) {
      expect(bodyDetail(body, 'none')).toBe(axiosDetail({ response: { data: body } }, 'none'));
    }
  });

  it('the shared fetch helper says a field check by its field, not as JSON', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => reply(422, FIELD_CHECK, 'Unprocessable Entity')));
    const e = await apiJson('/api/v1/projects/', { method: 'POST', body: {} }).catch((x: unknown) => x);
    expect(e).toBeInstanceOf(ApiError);
    expect((e as ApiError).status).toBe(422);
    expect((e as ApiError).detail).toBe('title: Field required');
  });

  it('the shared fetch helper keeps the status text when a refusal is not JSON', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false, status: 502, statusText: 'Bad Gateway',
                                                json: async () => { throw new SyntaxError('Unexpected token <'); } })));
    const e = await apiJson('/api/v1/anything').catch((x: unknown) => x);
    expect((e as ApiError).detail).toBe('Bad Gateway');
  });

  it('the session read says a refused field check by its field', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => reply(422, FIELD_CHECK)));
    expect(await whoami()).toEqual({ mode: 'unknown', basis: 'Failed (HTTP 422): title: Field required' });
  });
});

// W1015 — a caught failure, said as what it was. errorMessage said every error that was not an ApiError as an
// unreachable server: an axios refusal included, and a sentence the page threw itself. Fifty-four catches said the
// error's own message instead, which is the browser's "Failed to fetch" or axios's "Network Error" for a server that
// could not be reached, and axios's "Request failed with status code 409" for a refusal, its reason dropped.
const axiosRefusal = (status: number, data: unknown) =>
  Object.assign(new Error(`Request failed with status code ${status}`), { isAxiosError: true, response: { status, data } });
const axiosUnreached = () => Object.assign(new Error('Network Error'), { isAxiosError: true });

describe('a caught failure, said as what it was', () => {
  it('says a refusal by its status and reason, whichever client carried it', () => {
    expect(errorMessage(new ApiError(422, 'title: Field required'))).toBe('Failed (HTTP 422): title: Field required');
    expect(errorMessage(axiosRefusal(422, FIELD_CHECK))).toBe('Failed (HTTP 422): title: Field required');
    expect(errorMessage(axiosRefusal(409, { detail: 'the gate is closed' }))).toBe('Failed (HTTP 409): the gate is closed');
    expect(errorMessage(axiosRefusal(500, '<html>boom</html>'))).toBe('Failed (HTTP 500): no reason given');
  });

  it('says a server that could not be reached as one, never in the browser\'s or axios\'s words', () => {
    expect(errorMessage(new TypeError('Failed to fetch'))).toBe('Failed — backend unreachable.');
    expect(errorMessage(axiosUnreached())).toBe('Failed — backend unreachable.');
  });

  it('says a sentence the page threw itself as itself, and a cancelled call as cancelled', () => {
    expect(errorMessage(new Error('Failed (HTTP 409): the run is already going'))).toBe('Failed (HTTP 409): the run is already going');
    expect(errorMessage(Object.assign(new Error('aborted'), { name: 'AbortError' }))).toBe('Cancelled.');
    expect(errorMessage(Object.assign(new Error('canceled'), { isAxiosError: true, name: 'CanceledError' }))).toBe('Cancelled.');
  });

  it('still says what it cannot read as an unreachable server', () => {
    expect(errorMessage(new SyntaxError('Unexpected token <'))).toBe('Failed — backend unreachable.');
    expect(errorMessage('a string')).toBe('Failed — backend unreachable.');
    expect(errorMessage(new Error(''))).toBe('Failed — backend unreachable.');
  });
});
