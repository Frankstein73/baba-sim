"""Let a model play a level through an OpenAI-compatible chat/completions endpoint.

    OPENAI_BASE_URL=http://host:4000/v1 OPENAI_API_KEY=... \\
        python tools/play_llm.py 0level --model DeepSeek-V4.1-Flash-1017 --max-calls 30

Standard library only; proxies from the environment are ignored (the gateway is on the intranet).
Writes the full transcript and the result summary to --out.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request

from babasim.session import Session


def chat(base_url, key, payload, timeout):
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions", data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def play(session: Session, complete, max_turns: int = 200, log=print) -> list[dict]:
    """Agent loop. `complete(messages, tools)` returns the assistant message (dict)."""
    messages = [{"role": "system", "content": session.system_prompt()},
                {"role": "user", "content": session.initial_observation()}]
    idle = 0
    for _ in range(max_turns):
        if session.done:
            break
        msg = complete(messages, session.tools())
        messages.append(msg)
        calls = msg.get("tool_calls") or []
        if not calls:
            idle += 1
            if idle >= 3:
                break  # the model stopped using the tools
            messages.append({"role": "user", "content": "Please continue by calling a tool."})
            continue
        idle = 0
        for c in calls:
            fn = c["function"]
            result = session.call(fn["name"], fn.get("arguments"))
            log(f"{fn['name']} {fn.get('arguments')} -> {session.game.status}, turn {session.game.turn}")
            messages.append({"role": "tool", "tool_call_id": c["id"], "content": result})
    return messages


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("level")
    ap.add_argument("--world", default="baba")
    ap.add_argument("--model", required=True)
    ap.add_argument("--rules", choices=["none", "lit", "list"], default="lit")
    ap.add_argument("--obs", choices=["text", "json", "image", "text+image"], default="text")
    ap.add_argument("--grid", action="store_true")
    ap.add_argument("--lang", choices=["en", "zh"], default="en")
    ap.add_argument("--max-calls", type=int, default=50)
    ap.add_argument("--max-steps", type=int)
    ap.add_argument("--max-actions-per-call", type=int, default=32)
    ap.add_argument("--timeout", type=float, default=1800)
    ap.add_argument("--extra", default="{}", help="JSON merged into the request body (sampling, reasoning_effort, ...)")
    ap.add_argument("--out", help="transcript JSON path")
    a = ap.parse_args()

    base, key = os.environ["OPENAI_BASE_URL"], os.environ.get("OPENAI_API_KEY", "dummy")
    extra = json.loads(a.extra)
    s = Session(a.level, a.world, rules=a.rules, obs=a.obs, grid=a.grid, max_calls=a.max_calls,
                max_steps=a.max_steps, max_actions_per_call=a.max_actions_per_call, lang=a.lang)

    def complete(messages, tools):
        r = chat(base, key, {"model": a.model, "messages": messages, "tools": tools, **extra}, a.timeout)
        return r["choices"][0]["message"]

    messages = play(s, complete, log=lambda line: print(line, file=sys.stderr))
    summary = s.summary()
    print(json.dumps(summary, ensure_ascii=False))
    if a.out:
        with open(a.out, "w") as f:
            json.dump({"summary": summary, "history": s.history, "messages": messages}, f, ensure_ascii=False, indent=1)
    return 0 if s.won else 1


if __name__ == "__main__":
    sys.exit(main())
