#!/usr/bin/env python3
"""Custom dashboard and access gate for the RCU Service APIs."""

import html
import json
import os
import secrets
import socket
import threading
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

try:
    import rcupyclient
    import rcu_service_pb2
except Exception as exc:  # pragma: no cover
    rcupyclient = None
    rcu_service_pb2 = None
    IMPORT_ERROR = str(exc)
else:
    IMPORT_ERROR = None

RCU_WEB_HOST = os.environ.get("RCU_WEB_HOST", "0.0.0.0")
RCU_WEB_PORT = int(os.environ.get("RCU_WEB_PORT", "8080"))
RCU_SERVICE_ADDR = os.environ.get("RCU_SERVICE_ADDR", "ni-smartracks-07006271.local")
RCU_SERVICE_PORT = int(os.environ.get("RCU_SERVICE_PORT", "50051"))
RCU_SERVICE_CERT_PATH = os.environ.get("RCU_SERVICE_CERT_PATH", "/etc/ssl/certs/ni_ate_core_cert.pem")
SESSION_COOKIE_NAME = "rcudashboard_session"
SESSIONS = {}
SESSIONS_LOCK = threading.Lock()


def _connect_to_rcu(password, verify=False):
    if rcupyclient is None:
        raise RuntimeError(
            "rcupyclient is unavailable. The generated client and gRPC runtime must be installed. "
            f"Import error: {IMPORT_ERROR}"
        )

    if hasattr(rcupyclient, "initiate_channel"):
        rcupyclient.initiate_channel(
            RCU_SERVICE_ADDR,
            cert_path=RCU_SERVICE_CERT_PATH,
            password=password,
        )

    if verify:
        _get_image_version(rcupyclient)

    return rcupyclient


def _read_form(handler):
    try:
        content_length = int(handler.headers.get("Content-Length", "0"))
    except ValueError:
        content_length = 0

    if content_length <= 0:
        return {}

    raw = handler.rfile.read(content_length)
    if not raw:
        return {}

    form_data = raw.decode("utf-8", errors="replace")
    return {key: values[0] for key, values in parse_qs(form_data, keep_blank_values=True).items()}


def _read_json(handler):
    try:
        content_length = int(handler.headers.get("Content-Length", "0"))
    except ValueError:
        content_length = 0

    if content_length <= 0:
        return {}

    raw = handler.rfile.read(content_length)
    if not raw:
        return {}

    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def _json_response(handler, payload, status=200):
    body = json.dumps(payload, default=str).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _html_response(handler, payload, status=200):
    body = payload.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _get_cookie(handler):
    raw_cookie = handler.headers.get("Cookie", "")
    jar = SimpleCookie()
    jar.load(raw_cookie)
    value = jar.get(SESSION_COOKIE_NAME)
    return value.value if value is not None else ""


def _get_session_password(handler):
    with SESSIONS_LOCK:
        return SESSIONS.get(_get_cookie(handler))


def _is_authorized(handler):
    return _get_session_password(handler) is not None


def _create_session(password):
    session_id = secrets.token_urlsafe(32)
    with SESSIONS_LOCK:
        SESSIONS[session_id] = password
    return session_id


def _set_cookie(handler, session_id):
    jar = SimpleCookie()
    jar[SESSION_COOKIE_NAME] = session_id
    jar[SESSION_COOKIE_NAME]["path"] = "/"
    jar[SESSION_COOKIE_NAME]["httponly"] = True
    jar[SESSION_COOKIE_NAME]["samesite"] = "Strict"
    handler.send_header("Set-Cookie", jar[SESSION_COOKIE_NAME].OutputString())


def _clear_cookie(handler):
    session_id = _get_cookie(handler)
    with SESSIONS_LOCK:
        SESSIONS.pop(session_id, None)

    jar = SimpleCookie()
    jar[SESSION_COOKIE_NAME] = ""
    jar[SESSION_COOKIE_NAME]["path"] = "/"
    jar[SESSION_COOKIE_NAME]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
    handler.send_header("Set-Cookie", jar[SESSION_COOKIE_NAME].OutputString())


def _resolve_enum(enum_type, requested, aliases=()):
    if enum_type is None:
        return None

    targets = (requested, *aliases)
    normalized_targets = ["".join(character for character in target.lower() if character.isalnum()) for target in targets]
    for name in enum_type.keys():
        normalized_name = "".join(character for character in name.lower() if character.isalnum())
        if any(target == normalized_name or target in normalized_name for target in normalized_targets):
            return enum_type.Value(name)
    return None


def _get_image_version(client):
    if hasattr(client, "get_rcu_image_version"):
        return str(client.get_rcu_image_version())
    if not hasattr(client, "get_attribute") or rcu_service_pb2 is None:
        return "unknown"

    attribute_type = getattr(rcu_service_pb2, "Attribute", None)
    if attribute_type is None:
        return "unknown"
    attribute = attribute_type.Value("Attr_UTF8_RcuImageVersion")
    return str(client.get_attribute(attribute, 0))


def _collect_status(password):
    result = {"service": "unknown", "grpc": "unknown", "network": "unknown", "version": "unknown"}

    try:
        _connect_to_rcu(password)
        result["grpc"] = "ok"
    except Exception:
        result["grpc"] = "error"

    try:
        with socket.create_connection((RCU_SERVICE_ADDR, RCU_SERVICE_PORT), timeout=2):
            result["network"] = "ok"
    except Exception:
        result["network"] = "error"

    try:
        client = _connect_to_rcu(password)
        result["version"] = _get_image_version(client)
    except Exception:
        result["version"] = "unknown"

    if result["grpc"] == "ok" and result["network"] == "ok":
        result["service"] = "ok"
    else:
        result["service"] = "degraded"

    return result


def _login_page(message=""):
    note = html.escape(message or "Enter the panel password to continue.")
    return f"""<!doctype html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>RCU Access</title>
    <style>
        :root {{
            --bg: #0b1120;
            --panel: #101a2a;
            --panel-alt: #141f32;
            --line: rgba(148, 163, 184, 0.18);
            --text: #edf6ff;
            --muted: #a0b8d0;
            --accent: #4cc9f0;
            --danger: #f87171;
            --good: #34d399;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            background: radial-gradient(circle at top, #162238 0%, var(--bg) 42%, #050b14 100%);
            color: var(--text);
            font-family: Arial, Helvetica, sans-serif;
        }}
        .panel {{
            width: min(440px, 92vw);
            background: rgba(16, 26, 42, 0.92);
            border: 1px solid var(--line);
            border-radius: 18px;
            box-shadow: 0 18px 42px rgba(15, 23, 42, 0.65);
            padding: 32px 28px;
        }}
        h1 {{ margin: 0 0 10px; font-size: 28px; }}
        p {{ color: var(--muted); line-height: 1.5; }}
        .msg {{
            background: rgba(248, 113, 113, 0.09);
            border: 1px solid rgba(248, 113, 113, 0.28);
            color: #fecaca;
            border-radius: 10px;
            padding: 12px 14px;
            margin: 16px 0 18px;
        }}
        form {{ display: grid; gap: 16px; }}
        label {{
            display: grid;
            gap: 8px;
            font-size: 14px;
            color: var(--muted);
        }}
        input {{
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 12px 14px;
            font-size: 16px;
            background: rgba(15, 23, 42, 0.9);
            color: var(--text);
        }}
        button {{
            border: none;
            border-radius: 10px;
            padding: 12px 16px;
            font-size: 16px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent), #2dd4bf);
            color: #03131d;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <div class=\"panel\">
        <h1>RCU Service</h1>
        <p>Access the device control dashboard with the configured admin password.</p>
        <div class=\"msg\">{note}</div>
        <form method=\"post\" action=\"/login\">
            <label>
                Password
                <input type=\"password\" name=\"password\" placeholder=\"Enter password\" autocomplete=\"current-password\" required>
            </label>
            <button type=\"submit\">Unlock dashboard</button>
        </form>
    </div>
</body>
</html>
"""


def _dashboard_page(status):
    status_json = json.dumps(status)
    service_endpoint = html.escape(f"{RCU_SERVICE_ADDR}:{RCU_SERVICE_PORT}")
    return f"""<!doctype html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>RCU Dashboard</title>
    <style>
        :root {{
            --bg: #07111c;
            --panel: #0f1b2d;
            --panel-alt: #12253d;
            --line: rgba(148, 163, 184, 0.18);
            --text: #ecf5ff;
            --muted: #a9bfd7;
            --accent: #7dd3fc;
            --good: #34d399;
            --warn: #fbbf24;
            --danger: #f87171;
            --shadow: rgba(15, 23, 42, 0.5);
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            background: linear-gradient(180deg, #07111c 0%, #0e1726 45%, #111827 100%);
            color: var(--text);
            font-family: Arial, Helvetica, sans-serif;
        }}
        .shell {{
            max-width: 1100px;
            margin: 32px auto;
            padding: 0 20px 40px;
        }}
        .topbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 18px;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 18px 20px;
            margin-bottom: 24px;
        }}
        .title {{ font-size: 28px; font-weight: 700; }}
        .meta {{ color: var(--muted); font-size: 14px; }}
        .actions {{ display: flex; gap: 12px; flex-wrap: wrap; }}
        button {{
            border: none;
            border-radius: 10px;
            padding: 10px 14px;
            font-weight: 700;
            cursor: pointer;
            color: var(--text);
            transition: transform 0.1s ease;
        }}
        button:hover {{ transform: translateY(-1px); }}
        .primary {{ background: linear-gradient(135deg, #0ea5e9, #2dd4bf); color: #06222a; }}
        .secondary {{ background: rgba(148, 163, 184, 0.14); border: 1px solid var(--line); }}
        .danger {{ background: rgba(248, 113, 113, 0.12); border: 1px solid rgba(248, 113, 113, 0.28); color: #fecaca; }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 18px;
        }}
        .card {{
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.88), rgba(21, 34, 52, 0.9));
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 10px 25px var(--shadow);
        }}
        .label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--muted);
            margin-bottom: 12px;
        }}
        .value {{ font-size: 30px; font-weight: 700; }}
        .good {{ color: var(--good); }}
        .warn {{ color: var(--warn); }}
        .bad {{ color: var(--danger); }}
        .subtext {{ color: var(--muted); font-size: 12px; margin-top: 8px; }}
        .console {{
            margin-top: 22px;
            background: rgba(10, 17, 26, 0.9);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 16px 18px;
            min-height: 120px;
            white-space: pre-wrap;
            color: var(--text);
            font-family: monospace;
        }}
    </style>
</head>
<body>
    <div class=\"shell\">
        <div class=\"topbar\">
            <div>
                <div class=\"title\">RCU Service Dashboard</div>
                <div class=\"meta\">Endpoint: {service_endpoint}</div>
            </div>
            <div class=\"actions\">
                <button class=\"primary\" data-action=\"refresh\">Refresh</button>
                <button class=\"secondary\" data-action=\"logout\">Logout</button>
            </div>
        </div>

        <div class=\"grid\">
            <div class=\"card\">
                <div class=\"label\">System</div>
                <div class=\"value\" id=\"serviceStatus\">--</div>
                <div class=\"subtext\">RCU web wrapper</div>
            </div>
            <div class=\"card\">
                <div class=\"label\">gRPC</div>
                <div class=\"value\" id=\"grpcStatus\">--</div>
                <div class=\"subtext\">Backend health</div>
            </div>
            <div class=\"card\">
                <div class=\"label\">Network</div>
                <div class=\"value\" id=\"networkStatus\">--</div>
                <div class=\"subtext\">Service socket</div>
            </div>
            <div class=\"card\">
                <div class=\"label\">Version</div>
                <div class=\"value\" id=\"versionStatus\" style=\"font-size: 22px;\">--</div>
                <div class=\"subtext\">Built image</div>
            </div>
        </div>

        <div class=\"topbar\" style=\"margin-top: 22px;\">
            <div class=\"title\" style=\"font-size: 22px;\">Actions</div>
            <div class=\"actions\">
                <button class=\"primary\" data-action=\"restart\">Restart service</button>
                <button class=\"secondary\" data-action=\"power\">Set power state</button>
                <button class=\"danger\" data-action=\"health\">Health check</button>
            </div>
        </div>

        <div id=\"console\" class=\"console\">Loading status…</div>
    </div>

    <script>
        const initialStatus = {status_json};
        const setText = (id, value, tone = '') => {{
            const el = document.getElementById(id);
            if (!el) return;
            el.textContent = value;
            el.className = 'value ' + tone;
        }};

        const setStatus = (summary) => {{
            const toTone = (state) => state === 'ok' ? 'good' : (state === 'degraded' ? 'warn' : 'bad');
            setText('serviceStatus', summary.service || 'unknown', toTone(summary.service || 'unknown'));
            setText('grpcStatus', summary.grpc || 'unknown', toTone(summary.grpc || 'unknown'));
            setText('networkStatus', summary.network || 'unknown', toTone(summary.network || 'unknown'));
            setText('versionStatus', summary.version || 'unknown', '');
        }};

        const statusLine = (message) => {{
            document.getElementById('console').textContent = message;
        }};

        const fetchJson = async (url, options = {{}}) => {{
            const response = await fetch(url, {{
                headers: {{ 'Accept': 'application/json' }},
                ...options
            }});
            const payload = await response.json();
            if (!response.ok) {{
                throw new Error(payload.error || payload.message || 'Request failed');
            }}
            return payload;
        }};

        const refresh = async () => {{
            try {{
                const data = await fetchJson('/api/health');
                setStatus(data);
                statusLine(JSON.stringify(data, null, 2));
            }} catch (error) {{
                statusLine('Error: ' + error.message);
                setStatus(initialStatus);
            }}
        }};

        const actionRunner = async (name) => {{
            try {{
                if (name === 'logout') {{
                    window.location.href = '/logout';
                    return;
                }}
                if (name === 'refresh') {{
                    await refresh();
                    return;
                }}
                const methods = {{
                    'restart': {{ method: 'POST', body: JSON.stringify({{ type: 'service' }}), headers: {{ 'Content-Type': 'application/json' }} }},
                    'power': {{ method: 'POST', body: JSON.stringify({{ state: 'running' }}), headers: {{ 'Content-Type': 'application/json' }} }},
                    'health': {{ method: 'GET' }}
                }};
                const method = methods[name];
                const result = name === 'health' ? await fetchJson('/api/health') : await fetchJson('/api/' + name, method);
                statusLine(JSON.stringify(result, null, 2));
                if (name !== 'health') {{
                    await refresh();
                }}
            }} catch (error) {{
                statusLine('Action error: ' + error.message);
            }}
        }};

        document.querySelectorAll('[data-action]').forEach((node) => {{
            node.addEventListener('click', () => actionRunner(node.dataset.action));
        }});

        setStatus(initialStatus);
        refresh();
    </script>
</body>
</html>
"""


class RcuServiceWebHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _send_redirect(self, location):
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            password = _get_session_password(self)
            if password is not None:
                _html_response(self, _dashboard_page(_collect_status(password)))
                return
            _html_response(self, _login_page())
            return

        if path == "/logout":
            self.send_response(303)
            _clear_cookie(self)
            self.send_header("Location", "/")
            self.end_headers()
            return

        if path in ("/health", "/api/health"):
            if not _is_authorized(self):
                _json_response(self, {"error": "not authorized"}, status=401)
                return
            try:
                status = _collect_status(_get_session_password(self))
                _json_response(self, status)
                return
            except Exception as exc:  # pragma: no cover
                _json_response(self, {"error": str(exc)}, status=503)
                return

        if path == "/api/version":
            if not _is_authorized(self):
                _json_response(self, {"error": "not authorized"}, status=401)
                return
            try:
                client = _connect_to_rcu(_get_session_password(self))
                version = _get_image_version(client)
                _json_response(self, {"version": version})
                return
            except Exception as exc:  # pragma: no cover
                _json_response(self, {"error": str(exc)}, status=503)
                return

        _json_response(self, {"error": "not found"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/login":
            form = _read_form(self)
            password = form.get("password", "")
            try:
                _connect_to_rcu(password, verify=False)
            except Exception as exc:
                message = f"Login failed: {exc}"
                _html_response(self, _login_page(message), status=401)
                return

            session_id = _create_session(password)
            self.send_response(303)
            _set_cookie(self, session_id)
            self.send_header("Location", "/")
            self.end_headers()
            return

        if path == "/api/restart":
            if not _is_authorized(self):
                _json_response(self, {"error": "not authorized"}, status=401)
                return
            try:
                payload = _read_json(self)
                client = _connect_to_rcu(_get_session_password(self))
                kind = payload.get("type", "service")
                if hasattr(client, "initiate_restart"):
                    enum_type = getattr(rcu_service_pb2, "RcuRestartType", None)
                    value = _resolve_enum(enum_type, kind, aliases=("servicelevelrestart",))
                    if value is None:
                        _json_response(self, {"error": f"unsupported restart type '{kind}'"}, status=400)
                        return
                    client.initiate_restart(value)
                    _json_response(self, {"status": "ok", "type": str(kind)})
                    return
                _json_response(self, {"error": "restart is unavailable"}, status=501)
                return
            except Exception as exc:  # pragma: no cover
                _json_response(self, {"error": str(exc)}, status=503)
                return

        if path == "/api/power":
            if not _is_authorized(self):
                _json_response(self, {"error": "not authorized"}, status=401)
                return
            try:
                payload = _read_json(self)
                desired = payload.get("state", "running")
                client = _connect_to_rcu(_get_session_password(self))
                if hasattr(client, "request_rack_power_state"):
                    enum_type = getattr(rcu_service_pb2, "PowerState", None)
                    value = _resolve_enum(enum_type, desired)
                    if value is None:
                        _json_response(self, {"error": f"unsupported power state '{desired}'"}, status=400)
                        return
                    client.request_rack_power_state(value)
                    _json_response(self, {"status": "ok", "state": str(desired)})
                    return
                _json_response(self, {"error": "power control is unavailable"}, status=501)
                return
            except Exception as exc:  # pragma: no cover
                _json_response(self, {"error": str(exc)}, status=503)
                return

        _json_response(self, {"error": "not found"}, status=404)


def main():
    server = ThreadingHTTPServer((RCU_WEB_HOST, RCU_WEB_PORT), RcuServiceWebHandler)
    print(f"RCU dashboard listening on http://{RCU_WEB_HOST}:{RCU_WEB_PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
