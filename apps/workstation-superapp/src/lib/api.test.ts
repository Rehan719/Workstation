// W1013 — one reading of a refusal. A route that refuses answers a `detail` whose shape is the route's: a sentence, a
// field check's list of {loc, msg} (FastAPI's 422, the shape test_w1013 reads off a real route), or a structured
// refusal's object. Every page reads it through one helper, so a field check is said by its field wherever it lands:
// the shared fetch helper (apiJson) said one as JSON text, and twenty-two readers said the status alone.
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ApiError, apiJson, axiosDetail, bodyDetail } from './api';
import { asClause } from './api';   // W1059 - test_w1013 holds the line above as its own
import { errorMessage } from './api';   // W1015 - W1013's guard holds the line above as its own
import { whoami } from './auth';
import repo from '../pages/enterprise/VSBCockpit.repo.fixture.json';   // W1058 - the KPI gate's own refusal
import cell from '../components/InstrumentCellPanel.fixture.json';   // W1062 - the specifications store's own 503

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
    //  W1058 - this pinned the code: a structured refusal is said by its sentence
    expect(bodyDetail({ detail: { error: 'kpi_gate', basis: 'two objectives carry no KPI' } }, 'none')).toBe('two objectives carry no KPI');
    expect(bodyDetail(null, 'none')).toBe('none');
    expect(bodyDetail({}, 'none')).toBe('none');
  });

  //  W1058 - the shapes the routes refuse in: a code in `error` beside the sentence written for a reader
  it('says a structured refusal by its sentence, never by its code', () => {
    const kpi = repo.listed.body as { detail: { error: string; detail: string } };
    expect(repo.listed.status).toBe(409);
    expect(bodyDetail(kpi, 'none')).toBe(kpi.detail.detail);   // the marketplace's KPI gate, as the route answered
    expect(bodyDetail({ detail: { error: 'compliance_fail_hold', refused: 'listing', note: 'NOT DONE: the latest screen is fail' } }, 'none'))
      .toBe('NOT DONE: the latest screen is fail');
    expect(bodyDetail({ detail: { refused: 'organism.rpm_limit', why: 'a live lever is changed through Change Control' } }, 'none'))
      .toBe('a live lever is changed through Change Control');
    expect(bodyDetail({ detail: { refused: 'retirement_is_governed', basis: 'retirement is decided at Change Control' } }, 'none'))
      .toBe('retirement is decided at Change Control');
    //  the review gate writes its sentence in `error` and nothing else; a code with no sentence is said as itself
    expect(bodyDetail({ detail: { error: 'review gate blocks progress - a human review is pending', gate: 'design' } }, 'none'))
      .toBe('review gate blocks progress - a human review is pending');
    expect(bodyDetail({ detail: { error: 'curation_blocked_by_compliance', note: null } }, 'none')).toBe('curation_blocked_by_compliance');
    //  a key that is not a sentence is passed over
    expect(bodyDetail({ detail: { message: { nested: true }, note: 'a sentence' } }, 'none')).toBe('a sentence');
    expect(axiosDetail({ response: { data: kpi } }, 'none')).toBe(kpi.detail.detail);
  });

  //  W1059 - a reason said inside a longer sentence ends that sentence once
  it('says a reason as a clause: its own closing full stop is dropped, nothing else', () => {
    expect(asClause('No repository generated for VSB vsb-1 yet.')).toBe('No repository generated for VSB vsb-1 yet');
    expect(asClause('no reason given')).toBe('no reason given');
    expect(asClause('Failed — backend unreachable. ')).toBe('Failed — backend unreachable');
    expect(asClause('is it held?')).toBe('is it held?');
    expect(asClause('held for a person…')).toBe('held for a person…');
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

  //  W1062 - it cut every reason at 300 characters, mid-word and unmarked
  it('the shared fetch helper says a refusal\'s reason whole, however long', async () => {
    const a = cell.specifications_failed;
    expect(a.status).toBe(503);
    expect(a.body.detail.length).toBeGreaterThan(300);
    vi.stubGlobal('fetch', vi.fn(async () => reply(a.status, a.body, 'Service Unavailable')));
    const e = await apiJson('/api/v1/resources/specifications').catch((x: unknown) => x);
    expect(e).toBeInstanceOf(ApiError);
    expect((e as ApiError).detail).toBe(a.body.detail);
    expect(errorMessage(e)).toBe(`Failed (HTTP 503): ${a.body.detail}`);
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
