"""What changed between two runs of the same project: files, links, outside services, risks and promises.

Everything is compared in a language-independent way: a check finding by (probe, file, original message), a
compromise by what it bypassed, a promise by its own words. Only the texts shown to the reader are translated."""
from __future__ import annotations

import json
import re
from pathlib import Path

from ledger_report.i18n import probe_message, t

NEEDED = ("graph.json", "ledger.verified.json", "explain.verified.json", "probes.json", "run.json")
RUN_NAME = re.compile(r"^(\d{8}-\d{6})(?:-(\d+))?$")  # vl.py start: a timestamp, "-N" for runs in the same second


def run_key(name: str):
    """Sortable key of a run folder name, or None when the folder is not a run."""
    m = RUN_NAME.match(name)
    return (m.group(1), int(m.group(2) or 0)) if m else None


def _load(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def previous_run(run: Path) -> Path | None:
    """The latest run of the same project made before `run` whose check passed (all of NEEDED present)."""
    run = Path(run)
    me = run_key(run.name)
    if me is None or not run.parent.is_dir():
        return None
    earlier = sorted((p for p in run.parent.iterdir() if p.is_dir() and run_key(p.name) is not None and run_key(p.name) < me),
                     key=lambda p: run_key(p.name))
    for cand in reversed(earlier):
        if all((cand / name).is_file() for name in NEEDED):
            return cand
    return None


def _risks(ledger: dict, probes: dict, lang: str) -> dict:
    """{key: {"path", "level", "text"}} — probe findings that are certain or hints, and compromises still in place."""
    out = {}
    for f in probes.get("findings", []):
        if f.get("level") in ("certain", "hint"):
            out[("probe", f.get("probe"), f.get("path"), f.get("message"))] = {
                "path": f.get("path", ""), "level": "bad" if f["level"] == "certain" else "warn",
                "text": probe_message(f.get("message", ""), lang)}
    ev = ledger.get("evidence", {})
    for c in ledger.get("compromises", []):
        if c.get("still_present") is True:
            paths = sorted({ev[i]["path"] for i in c.get("now", []) if ev.get(i, {}).get("path")})
            out[("compromise", c.get("bypassed"))] = {"path": ", ".join(paths), "level": "bad",
                                                     "text": f"{t(lang, 'g_compromise')}: {c.get('bypassed', '')}"}
    return out


def _promises(ledger: dict) -> dict:
    """{(words, n): status} — a promise is known by its words; two with the same words are told apart by order."""
    seen: dict[str, int] = {}
    out = {}
    for p in ledger.get("promises", []):
        n = seen[p["plain"]] = seen.get(p["plain"], -1) + 1
        out[(p["plain"], n)] = p["status"]
    return out


def compare(prev: Path, cur: Path, lang: str) -> dict:
    prev, cur = Path(prev), Path(cur)
    g0, g1 = _load(prev / "graph.json", {}), _load(cur / "graph.json", {})
    n0 = {n["id"]: n for n in g0.get("nodes", [])}
    n1 = {n["id"]: n for n in g1.get("nodes", [])}
    sha_known = bool(n0) and all("sha" in n for n in n0.values())
    changed = sorted(i for i in n0.keys() & n1.keys() if sha_known and n0[i].get("sha") != n1[i].get("sha"))
    e0 = {(e["from"], e["to"]) for e in g0.get("edges", [])}
    e1 = {(e["from"], e["to"]) for e in g1.get("edges", [])}
    x0 = {x["id"] for x in g0.get("externals", [])}
    x1 = {x["id"] for x in g1.get("externals", [])}
    r0 = _risks(_load(prev / "ledger.verified.json", {}), _load(prev / "probes.json", {}), lang)
    r1 = _risks(_load(cur / "ledger.verified.json", {}), _load(cur / "probes.json", {}), lang)
    p0 = _promises(_load(prev / "ledger.verified.json", {}))
    p1 = _promises(_load(cur / "ledger.verified.json", {}))
    order = lambda items: sorted(items, key=lambda r: (r["path"], r["text"]))  # noqa: E731
    return {
        "prev_run": prev.name,
        "since": _load(prev / "run.json", {}).get("created", ""),
        "sha_known": sha_known,
        "files": {"added": sorted(n1.keys() - n0.keys()), "removed": sorted(n0.keys() - n1.keys()), "changed": changed},
        "links": {"added": [list(e) for e in sorted(e1 - e0)], "removed": [list(e) for e in sorted(e0 - e1)]},
        "services": {"added": sorted(x1 - x0), "removed": sorted(x0 - x1)},
        "risks": {"new": order(r1[k] for k in r1.keys() - r0.keys()),
                  "resolved": order(r0[k] for k in r0.keys() - r1.keys())},
        "promises": {"changed": [{"plain": k[0], "before": p0[k], "after": p1[k]} for k in sorted(p0.keys() & p1.keys())
                                 if p0[k] != p1[k]],
                     "new": [{"plain": k[0], "status": p1[k]} for k in sorted(p1.keys() - p0.keys())],
                     "gone": [{"plain": k[0], "status": p0[k]} for k in sorted(p0.keys() - p1.keys())]},
    }


def summary_line(d: dict, lang: str = "en") -> str:
    f, r = d["files"], d["risks"]
    return (t(lang, "g_diff_cli", date=d["since"][:10] or d["prev_run"], added=len(f["added"]), changed=len(f["changed"]),
              removed=len(f["removed"]), new=len(r["new"]), resolved=len(r["resolved"]))
            + ("" if d["sha_known"] else t(lang, "g_diff_cli_nosha")))
