"""Load test: fire many same-location reports at the live pipeline and watch
the dedup magnitude climb. Validates that the map's data source accumulates and
that the backend stays healthy under repeated reports about one place.

Usage:
  python scripts/load_test_map.py [TOTAL] [CONCURRENCY] [MODE] [DELAY]

  TOTAL        number of reports to fire (default 50)
  CONCURRENCY  parallel workers (default 8)
  MODE         "same" -> one fixed message so dedup funnels into a single
               incident whose magnitude climbs cleanly; "varied" (default) ->
               rotate through realistic Oak Street phrasings
  DELAY        optional seconds to sleep between submissions (paced mode)
"""
from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx

BACKEND = (
    "https://allclear-kt5fw24guxoxy-backend.nicebay-0aac45bb.eastus."
    "azurecontainerapps.io"
)

# All mention "Oak Street" so the classifier extracts a consistent location and
# dedup funnels them toward the same incident(s).
VARIANTS = [
    "A downed power line is sparking on Oak Street.",
    "The transformer on Oak Street is sparking again.",
    "I smell smoke near the Oak Street power line.",
    "Oak Street still has no power and it's getting dark.",
    "There's a small fire by the pole on Oak Street.",
    "Sparks are flying off the line on Oak Street.",
    "The power line on Oak Street is down across the road.",
    "Neighbors on Oak Street report the outage is spreading.",
    "Loud bang and now the Oak Street line is arcing.",
    "Smoke is coming from a transformer on Oak Street.",
]


# A single fixed report. In "same" mode every submission uses this exact text so
# cosine similarity is ~1.0 and the router attaches them all to one incident.
SAME = "A downed power line is sparking on Oak Street."


def fire(i: int, mode: str = "varied") -> dict:
    msg = SAME if mode == "same" else VARIANTS[i % len(VARIANTS)]
    body = {"message": msg, "session_id": "loadtest-oak", "channel": "chat"}
    t0 = time.perf_counter()
    try:
        r = httpx.post(f"{BACKEND}/api/signals", json=body, timeout=90.0)
        dt = time.perf_counter() - t0
        out = {"i": i, "status": r.status_code, "ms": round(dt * 1000)}
        if r.status_code == 200:
            d = r.json()
            out["incident"] = d["action"]["incident_id"]
            out["magnitude"] = d["routing"]["magnitude"]
            out["outcome"] = d["routing"]["outcome"]
            out["location"] = (d["classification"]["entities"] or {}).get("location")
        else:
            out["body"] = r.text[:160]
        return out
    except Exception as exc:  # noqa: BLE001
        return {"i": i, "status": "ERR", "ms": round((time.perf_counter() - t0) * 1000), "err": str(exc)[:160]}


def main() -> None:
    total = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    concurrency = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    mode = sys.argv[3] if len(sys.argv) > 3 else "varied"
    delay = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
    print(
        f"Load test: {total} Oak Street reports, concurrency={concurrency}, "
        f"mode={mode}, delay={delay}s\n"
    )

    results: list[dict] = []
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futs = []
        for i in range(total):
            futs.append(ex.submit(fire, i, mode))
            if delay:
                time.sleep(delay)
        for fut in as_completed(futs):
            res = fut.result()
            results.append(res)
            tag = res.get("magnitude", res.get("err", res.get("body", "")))
            print(
                f"  #{res['i']:>3}  {str(res['status']):>4}  {res['ms']:>6}ms  "
                f"mag={res.get('magnitude','-')}  inc={res.get('incident','-')}  "
                f"loc={res.get('location','-')}"
            )
    wall = time.perf_counter() - t0

    ok = [r for r in results if r["status"] == 200]
    bad = [r for r in results if r["status"] != 200]
    lat = sorted(r["ms"] for r in ok)
    incidents: dict[str, int] = {}
    max_mag = 0
    for r in ok:
        incidents[r["incident"]] = incidents.get(r["incident"], 0) + 1
        max_mag = max(max_mag, r.get("magnitude", 0))

    def pctl(p: float) -> int:
        if not lat:
            return 0
        return lat[min(len(lat) - 1, int(p * len(lat)))]

    print("\n" + "=" * 60)
    print(f"Total:        {len(results)}  in {wall:.1f}s")
    print(f"Success(200): {len(ok)}")
    print(f"Failures:     {len(bad)}")
    if lat:
        print(f"Latency ms:   p50={pctl(0.5)}  p95={pctl(0.95)}  max={lat[-1]}")
    print(f"Max magnitude observed: {max_mag}")
    print(f"Distinct incidents: {len(incidents)}")
    top = sorted(incidents.items(), key=lambda kv: -kv[1])[:6]
    print(f"Top incidents (id: count): {top}")
    locs = {r.get("location") for r in ok}
    print(f"Locations extracted: {sorted(l for l in locs if l)}")
    if bad:
        print("\nFailure samples:")
        for r in bad[:5]:
            print(f"  #{r['i']} {r['status']} {r.get('err') or r.get('body')}")


if __name__ == "__main__":
    main()
