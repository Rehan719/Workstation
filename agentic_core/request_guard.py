"""W1202 (FU-1835, P4.1) - THROUGH THE SSH TUNNEL NO PAGE FROM ANOTHER SITE ACTS ON THE PLATFORM.

With sign-in off, the release machine's platform acts as the administrator for whoever reaches its port, and step 7 of
docs/DEPLOYMENT.md forwards that port to the Owner's computer. CORS_ORIGINS does not stop a page in the Owner's browser
from acting on it: Starlette's CORSMiddleware runs the app for a simple request from any Origin and only withholds the
answer, a body sent with no Content-Type is parsed as JSON, the stream socket takes any Origin, and a host name rebound
to 127.0.0.1 is the tunnel's own origin to the browser. This guard is the check that does stop it.

IT ACTS ONLY WHERE THE RELEASE MACHINE TURNS IT ON. It reads, at each request, a setting of its own that only
deploy/gcp/startup.sh gives the platform (both of its runs, and so the HTTPS drill's front, which is the script's own):
  WORKSTATION_PAGE_ORIGINS  the origins whose pages may act here, each exactly scheme://host[:port] (http or https), as
                            http://localhost:8800 and http://127.0.0.1:8800 through the tunnel (the same page, opened
                            either way) or https://DOMAIN behind the front;
  WORKSTATION_SERVED_HOSTS  the host names the platform is served under besides localhost, 127.0.0.1 and ::1, as the
                            machine's domain behind the front. It is a setting of its own because a page's origin is not
                            always the platform's host: a split deployment (a backend whose pages are served from
                            another host) names its page's origin in the first and its own host name in the second.
Unset or empty, the guard is off, in silence, and every request is served exactly as before: the Owner's own
platform, the Vite dev server's proxy (which keeps Origin http://localhost:5173) and the test suite (Host testserver)
are unchanged. It is never keyed on CORS_ORIGINS: a .env made from an older .env.example set CORS_ORIGINS to its own
trailing comment. An entry that is not exactly what is asked for, in either setting, leaves the guard OFF and the log
says so once, naming the entry, at startup (the lifespan), or at the first request where no lifespan ran: a guard
that half-read its list would refuse the machine's own page or let another through.

WHAT IT REFUSES, while on (nothing runs: the request never reaches the app, and the membrane, which observes only what
reaches the app, does not observe it):
  - any request, of any method, whose Host is not localhost, 127.0.0.1, ::1 (any port) or a served host: 400 with a
    sentence naming the host it gave and the hosts served (a host name rebound to the machine); a stream socket under
    such a Host is closed with code 1008 before it is accepted, with no sentence;
  - a POST, PUT, PATCH or DELETE whose Origin is present and not listed, 'null' included, or that carries no Origin but
    Sec-Fetch-Site: cross-site: 403 with a sentence;
  - a read under /api/ that the browser says a page of another site asked for without the reader following a link
    (Sec-Fetch-Site: cross-site and a Sec-Fetch-Mode other than navigate: an image, a script or a fetch): 403 with a
    sentence. A link followed from another site still opens, which is why a read is not refused outright;
  - a stream socket whose Origin is present and not listed: closed with code 1008 before it is accepted.
WHAT IT DOES NOT REFUSE:
  - a request with no Origin: a program (curl, set_password, the drills, the image's health check) is not a page, and
    sign-in, not this guard, is what stops a program on the Owner's computer;
  - a preflight (OPTIONS) and every other safe method but the reads above: CORS still answers a preflight, so the
    browser stops a page's request that needs one, and this guard stops the simple ones;
  - a page's cross-site GET still runs, though the page cannot read its answer, when it is a link followed from another
    site or comes from a browser that sends no Sec-Fetch headers. Three reads act when they run:
    GET /api/v1/qep/adaptation/registry saves its store when it is read, until W1220 makes every read free of writes;
    GET /api/v1/intelligence/forecasts makes a gateway call and rewrites its cache, at most once an hour; and
    GET /api/v1/cca/impact/{cca_id} makes a gateway call for a change whose id is known.
"""
from __future__ import annotations

import json
import logging
import os
import re

logger = logging.getLogger("workstation.request_guard")

PAGE_ORIGINS_VAR = "WORKSTATION_PAGE_ORIGINS"
SERVED_HOSTS_VAR = "WORKSTATION_SERVED_HOSTS"
LOCAL_HOSTS = ("localhost", "127.0.0.1", "::1")
UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})
_DEFAULT_PORT = {"http": 80, "https": 443}

_LABEL = r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
_NAME = re.compile(rf"^{_LABEL}(?:\.{_LABEL})*$")
_IPV6 = re.compile(r"^[0-9a-f:.]+$")
_ORIGIN = re.compile(r"^(https?)://(\[[0-9a-f:.]+\]|[a-z0-9.-]+)(?::([0-9]{1,5}))?$")


def _host_name(text: str):
    """A bare host name, IPv4 address or IPv6 address (brackets removed), lower-cased; None when it is none of them."""
    h = text.strip().lower()
    if h.startswith("[") and h.endswith("]"):
        h = h[1:-1]
        return h if h and ":" in h and _IPV6.match(h) else None
    if ":" in h:
        return h if _IPV6.match(h) and h.count(":") >= 2 else None
    return h if len(h) <= 253 and _NAME.match(h) else None


def normal_origin(text: str):
    """scheme://host[:port] exactly, lower-cased and with the scheme's default port dropped; None for anything else,
    'null' and a path or a trailing slash included."""
    m = _ORIGIN.match((text or "").strip().lower())
    if not m:
        return None
    scheme, host, port = m.group(1), m.group(2), m.group(3)
    name = _host_name(host)
    if name is None or (port is not None and not 0 < int(port) < 65536):
        return None
    shown = f"[{name}]" if ":" in name else name
    if port is None or int(port) == _DEFAULT_PORT[scheme]:
        return f"{scheme}://{shown}"
    return f"{scheme}://{shown}:{int(port)}"


def host_of(header: str):
    """The host name a Host header gives, without its port and with an IPv6 address's brackets removed ('[::1]:8000'
    is ::1); None for a header that is not one."""
    h = (header or "").strip().lower()
    if h.startswith("["):
        end = h.find("]")
        if end < 0 or (h[end + 1:] and not re.fullmatch(r":[0-9]{1,5}", h[end + 1:])):
            return None
        return _host_name(h[:end + 1])
    name, sep, port = h.rpartition(":")
    if sep and port.isdigit():
        h = name
    elif sep:
        return None
    if h.endswith("."):
        h = h[:-1]
    return _host_name(h) if h else None


class GuardState:
    """What the guard does now: on with its origins and hosts, or off with the reason."""

    def __init__(self, on: bool, origins=(), hosts=(), reason: str = ""):
        self.on, self.origins, self.hosts, self.reason = on, tuple(origins), tuple(hosts), reason


_STATE_CACHE: dict = {}
_SAID_OFF: set = set()


def guard_state(environ=None) -> GuardState:
    """Read the two settings (at each request; parsed once per value). Unset or empty: off. An entry that is not what
    is asked for: off, and logged once, naming it."""
    env = os.environ if environ is None else environ
    raw_origins, raw_hosts = env.get(PAGE_ORIGINS_VAR, ""), env.get(SERVED_HOSTS_VAR, "")
    key = (raw_origins, raw_hosts)
    if key in _STATE_CACHE:
        return _STATE_CACHE[key]
    state = _parse(raw_origins, raw_hosts)
    if not state.on and state.reason and key not in _SAID_OFF:
        _SAID_OFF.add(key)
        logger.warning("the request guard is OFF: %s", state.reason)
    _STATE_CACHE[key] = state
    return state


def _parse(raw_origins: str, raw_hosts: str) -> GuardState:
    if not raw_origins.strip():
        return GuardState(False, reason="")          # off, as on every machine but the release machine
    origins = []
    for entry in raw_origins.split(","):
        o = normal_origin(entry)
        if o is None:
            return GuardState(False, reason=(f"{PAGE_ORIGINS_VAR}={raw_origins!r} holds {entry.strip()!r}, which is "
                                             "not scheme://host[:port] (http or https); every request is served "
                                             "unchecked"))
        origins.append(o)
    hosts = list(LOCAL_HOSTS)
    for entry in raw_hosts.split(",") if raw_hosts.strip() else ():
        h = _host_name(entry) if ":" not in entry.strip() or entry.strip().count(":") >= 2 else None
        if h is None:
            return GuardState(False, reason=(f"{SERVED_HOSTS_VAR}={raw_hosts!r} holds {entry.strip()!r}, which is not "
                                             "a host name without a port; every request is served unchecked"))
        if h not in hosts:
            hosts.append(h)
    return GuardState(True, origins, hosts)


def _headers(scope) -> dict:
    """Every value of each header, by its lower-cased name."""
    got: dict = {}
    for k, v in scope.get("headers") or ():
        got.setdefault(k.decode("latin-1").lower(), []).append(v.decode("latin-1"))
    return got


def _under_api(scope) -> bool:
    path = scope.get("path") or ""
    return path == "/api" or path.startswith("/api/")


def _navigates(hdrs) -> bool:
    """A link followed, or a form sent by a top-level navigation: the browser's Sec-Fetch-Mode is navigate."""
    return any(v.strip().lower() == "navigate" for v in hdrs.get("sec-fetch-mode", []))


def refusal(scope, state: GuardState):
    """(status, sentence) when the request is refused; None when it passes."""
    hdrs = _headers(scope)
    hosts = hdrs.get("host", [])
    given = hosts[0] if len(hosts) == 1 else ", ".join(hosts) or "none"
    if len(hosts) != 1 or host_of(hosts[0]) not in state.hosts:
        return 400, (f"Refused: this platform is served only as {', '.join(state.hosts)}, and this request's Host was "
                     f"{given!r}, so a host name rebound to the machine is not served; nothing ran (W1202).")
    origins = hdrs.get("origin", [])
    is_socket = scope.get("type") == "websocket"
    cross_site = any(v.strip().lower() == "cross-site" for v in hdrs.get("sec-fetch-site", []))
    if not is_socket and scope.get("method", "").upper() not in UNSAFE_METHODS:
        if cross_site and _under_api(scope) and not _navigates(hdrs):
            return 403, ("Refused: the browser says a page of another site asked for this read without the reader "
                         "following a link (Sec-Fetch-Site: cross-site, and a Sec-Fetch-Mode other than navigate); "
                         f"only a page of {', '.join(state.origins)} may. Nothing ran (W1202).")
        return None
    if origins:
        if len(origins) != 1 or normal_origin(origins[0]) not in state.origins:
            return 403, (f"Refused: a page of the origin {', '.join(origins)!r} may not act on this platform; only a "
                         f"page of {', '.join(state.origins)} may. Nothing ran (W1202).")
        return None
    if not is_socket and cross_site:
        return 403, ("Refused: the browser says this request comes from a page of another site (Sec-Fetch-Site: "
                     f"cross-site); only a page of {', '.join(state.origins)} may act on this platform. Nothing ran "
                     "(W1202).")
    return None


class OriginHostGuard:
    """A pure ASGI middleware over the http and websocket scopes; lifespan and anything else pass through, the
    lifespan after the settings are read once, so a setting the guard cannot read is said at startup."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "lifespan":
            guard_state()                          # an unreadable setting is logged at startup, not only at a request
        if scope.get("type") not in ("http", "websocket"):
            return await self.app(scope, receive, send)
        state = guard_state()
        if not state.on:
            return await self.app(scope, receive, send)
        refused = refusal(scope, state)
        if refused is None:
            return await self.app(scope, receive, send)
        status, sentence = refused
        if scope["type"] == "websocket":
            message = await receive()                 # the handshake's websocket.connect, answered with a close
            if message.get("type") == "websocket.connect":
                await send({"type": "websocket.close", "code": 1008, "reason": "refused by the request guard (W1202)"})
            return None
        body = json.dumps({"detail": sentence, "refused_by": "W1202 request guard (FU-1835)"}).encode("utf-8")
        await send({"type": "http.response.start", "status": status,
                    "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())]})
        await send({"type": "http.response.body", "body": body})
        return None
