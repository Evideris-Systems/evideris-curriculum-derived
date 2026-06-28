#!/usr/bin/env python3
"""Completeness check (derived mode): _meta.provenance with derived-allowed
type + non-trivial reason, and stub-text detection in any string field."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ALLOWED = {"verbatim-from-primary-source", "paraphrased-from-primary-source", "evideris-design", "inferred-from-source"}
VAGUE_TEXT = [r"\bTODO\b", r"\bFIXME\b", r"\.\.\.$", r"\[placeholder\]", r"\[stub\]"]

def stub_text(s: str) -> str | None:
    if not isinstance(s, str): return None
    for pat in VAGUE_TEXT:
        if re.search(pat, s): return f"contains stub marker /{pat}/"
    return None

def check(path: Path) -> list[str]:
    try: d = json.loads(path.read_text())
    except json.JSONDecodeError as e: return [f"{path}: invalid JSON: {e}"]
    errs = []
    meta = d.get("_meta")
    if not meta:
        return [f"{path}: missing _meta block"]
    prov = meta.get("provenance") or {}
    pt = prov.get("type")
    if pt not in ALLOWED:
        errs.append(f"{path}: provenance.type='{pt}' not allowed in derived repo (must be one of {sorted(ALLOWED)})")
    if not prov.get("reason") or len(prov["reason"]) < 10:
        errs.append(f"{path}: provenance.reason missing or <10 chars")
    if pt in {"verbatim-from-primary-source", "paraphrased-from-primary-source"} and not prov.get("primary_source_doi"):
        errs.append(f"{path}: primary-source provenance requires primary_source_doi")
    # Walk strings
    def walk(node, p=""):
        if isinstance(node, str):
            r = stub_text(node)
            if r: errs.append(f"{path}: {p}: {r}")
        elif isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{p}.{k}" if p else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{p}[{i}]")
    walk(d)
    return errs

def main(argv: list[str]) -> int:
    targets = [Path(t).resolve() for t in argv] if argv else sorted(list((ROOT / "derived").rglob("*.json")) + list((ROOT / "releases").rglob("*.json")))
    if not targets:
        print("completeness (derived): nothing to check"); return 0
    all_errs = []
    pas = 0
    for p in targets:
        errs = check(p)
        if errs: all_errs.extend(errs)
        else: pas += 1
    print(f"completeness (derived): {pas}/{len(targets)} files passed")
    if all_errs:
        for e in all_errs[:50]: print(f"  FAIL {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
