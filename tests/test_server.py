"""HTTP service: one level played end to end over real sockets."""

import json
import threading
import urllib.error
import urllib.request

import pytest

from babasim.server import serve


@pytest.fixture(scope="module")
def base():
    srv = serve("127.0.0.1", 0)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def req(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(r, timeout=30) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_play_level_over_http(base):
    assert req("GET", base + "/health")[1]["ok"]
    code, lv = req("GET", base + "/levels?world=baba")
    assert code == 200 and {"level": "0level", "name": "baba is you"} in lv["levels"]

    code, s = req("POST", base + "/sessions", {"level": "0level", "max_calls": 10})
    assert code == 201 and [t["function"]["name"] for t in s["tools"]] == ["move", "undo", "restart", "look"]
    assert "baba  (12,10)" in s["observation"] and "puzzle game" in s["system_prompt"]
    url = f"{base}/sessions/{s['session_id']}"

    code, r = req("POST", url + "/call", {"name": "move", "arguments": {"actions": ["right"] * 4}})
    assert code == 200 and not r["done"] and "rock (16,10)→(17,10)" in r["observation"]
    code, r = req("POST", url + "/call", {"name": "undo", "arguments": {"steps": 1}})
    assert r["summary"]["turn"] == 3
    code, r = req("POST", url + "/call", {"name": "move", "arguments": {"actions": ["right"] * 8}})
    assert r["won"] and r["done"] and r["summary"]["steps"] == 9

    code, info = req("GET", url)
    assert [h["tool"] for h in info["history"]] == ["move", "undo", "move"]
    assert req("DELETE", url)[0] == 200 and req("GET", url)[0] == 404


def test_errors(base):
    assert req("POST", base + "/sessions", {"level": "nope"})[0] == 400
    assert req("POST", base + "/sessions", {"level": "0level", "bogus": 1})[0] == 400
    assert req("POST", base + "/sessions/abc/call", {"name": "look"})[0] == 404
    assert req("GET", base + "/levels?world=../x")[0] == 404
    code, s = req("POST", base + "/sessions", {"level": "0level"})
    code, r = req("POST", f"{base}/sessions/{s['session_id']}/call", {"name": "move", "arguments": {"actions": ["fly"]}})
    assert code == 200 and r["observation"].startswith("Invalid call")  # bad tool use is the model's, not HTTP's
