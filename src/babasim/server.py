"""Minimal HTTP service around Session (standard library only, JSON in and out).

    python -m babasim.server --port 8765

    GET    /health
    GET    /levels?world=baba                 -> {"levels": [{"level", "name"}]}
    POST   /sessions  {"level": "0level", ...Session options}
                                              -> {"session_id", "system_prompt", "tools", "observation"}
    POST   /sessions/<id>/call  {"name": "move", "arguments": {"actions": ["right"]}}
                                              -> {"observation", "done", "won", "summary"}
    GET    /sessions/<id>                     -> {"summary", "history"}
    DELETE /sessions/<id>

Session options: world, seed, rules (none|lit|list), obs (text|json|image|text+image), grid, lang (en|zh),
max_actions_per_call, max_calls, max_steps, tile_px. No authentication: bind it to a trusted interface.
"""

from __future__ import annotations

import argparse
import json
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from babasim.runtime import DATA
from babasim.session import Session

OPTIONS = ("world", "seed", "rules", "obs", "grid", "lang", "max_actions_per_call", "max_calls",
           "max_steps", "tile_px")


class Store:
    def __init__(self, max_sessions: int = 1000):
        self.sessions: dict[str, tuple[Session, threading.Lock]] = {}
        self.lock = threading.Lock()
        self.max_sessions = max_sessions

    def create(self, body: dict):
        level = body.get("level")
        if not isinstance(level, str):
            raise ValueError("level is required")
        world = body.get("world", "baba")
        if not (DATA / "levels" / world / f"{level}.json").is_file():
            raise ValueError(f"unknown level {world}/{level}")
        unknown = set(body) - set(OPTIONS) - {"level"}
        if unknown:
            raise ValueError(f"unknown options: {sorted(unknown)}")
        s = Session(level, **{k: body[k] for k in OPTIONS if k in body})
        sid = uuid.uuid4().hex
        with self.lock:
            if len(self.sessions) >= self.max_sessions:
                raise ValueError("too many open sessions; delete some first")
            self.sessions[sid] = (s, threading.Lock())
        return sid, s

    def get(self, sid):
        with self.lock:
            return self.sessions.get(sid)

    def delete(self, sid):
        with self.lock:
            return self.sessions.pop(sid, None) is not None


def levels(world: str) -> list[dict]:
    out = []
    for p in sorted((DATA / "levels" / world).glob("*.json")):
        out.append({"level": p.stem, "name": json.loads(p.read_text())["ld"].get("general", {}).get("name", "")})
    return out


def make_handler(store: Store):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, fmt, *args):  # quiet by default
            pass

        def _send(self, code, obj):
            data = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _body(self):
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n) or b"{}")
            if not isinstance(body, dict):
                raise ValueError("request body must be a JSON object")
            return body

        def _route(self, method):
            url = urlparse(self.path)
            parts = [p for p in url.path.split("/") if p]
            try:
                if method == "GET" and parts == ["health"]:
                    return self._send(200, {"ok": True, "sessions": len(store.sessions)})
                if method == "GET" and parts == ["levels"]:
                    world = parse_qs(url.query).get("world", ["baba"])[0]
                    if not world.isidentifier() or not (DATA / "levels" / world).is_dir():
                        return self._send(404, {"error": f"unknown world {world}"})
                    return self._send(200, {"world": world, "levels": levels(world)})
                if method == "POST" and parts == ["sessions"]:
                    sid, s = store.create(self._body())
                    return self._send(201, {"session_id": sid, "system_prompt": s.system_prompt(),
                                            "tools": s.tools(), "observation": s.initial_observation()})
                if len(parts) >= 2 and parts[0] == "sessions":
                    entry = store.get(parts[1])
                    if entry is None:
                        return self._send(404, {"error": "no such session"})
                    s, lock = entry
                    if method == "POST" and parts[2:] == ["call"]:
                        body = self._body()
                        if not isinstance(body.get("name"), str):
                            raise ValueError("name is required")
                        with lock:
                            obs = s.call(body["name"], body.get("arguments"))
                            return self._send(200, {"observation": obs, "done": s.done, "won": s.won,
                                                    "summary": s.summary()})
                    if method == "GET" and len(parts) == 2:
                        with lock:
                            return self._send(200, {"summary": s.summary(), "history": s.history})
                    if method == "DELETE" and len(parts) == 2:
                        store.delete(parts[1])
                        return self._send(200, {"deleted": True})
                return self._send(404, {"error": "not found"})
            except (ValueError, TypeError, json.JSONDecodeError) as e:
                return self._send(400, {"error": str(e)})

        def do_GET(self):
            self._route("GET")

        def do_POST(self):
            self._route("POST")

        def do_DELETE(self):
            self._route("DELETE")

    return Handler


def serve(host: str = "127.0.0.1", port: int = 8765, max_sessions: int = 1000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), make_handler(Store(max_sessions)))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--max-sessions", type=int, default=1000)
    a = ap.parse_args()
    srv = serve(a.host, a.port, a.max_sessions)
    print(f"babasim server on http://{a.host}:{a.port}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
