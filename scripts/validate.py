#!/usr/bin/env python3
"""Schema validation for derived artifacts."""
from __future__ import annotations
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
TYPE_TO_SCHEMA = {
    "release":              "release.schema.json",
    "competency":           "competency.schema.json",
    "epa":                  "epa.schema.json",
    "evidenceCriterion":    "evidence-criterion.schema.json",
    "competencyAssessment": "competency-assessment.schema.json",
    "catRecommendationMap": "cat-recommendation-map.schema.json",
    "scoringTool":          "scoring-tool.schema.json",
}

def load_registry() -> Registry:
    reg = Registry()
    for sf in sorted(SCHEMAS.glob("*.schema.json")):
        sch = json.loads(sf.read_text())
        res = Resource(contents=sch, specification=DRAFT202012)
        reg = reg.with_resource(uri=sch["$id"], resource=res)
        reg = reg.with_resource(uri=sf.name, resource=res)
    return reg

def validate_instance(path: Path, reg: Registry) -> list[str]:
    inst = json.loads(path.read_text())
    t = inst.get("type")
    if t not in TYPE_TO_SCHEMA:
        return [f"{path}: unknown type {t!r}"]
    sch = json.loads((SCHEMAS / TYPE_TO_SCHEMA[t]).read_text())
    v = Draft202012Validator(sch, registry=reg)
    errs = []
    for e in v.iter_errors(inst):
        loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
        errs.append(f"{path}: {loc}: {e.message}")
    return errs

def main(argv: list[str]) -> int:
    if argv and argv[0] == "--self":
        errs = []
        for sf in sorted(SCHEMAS.glob("*.schema.json")):
            try:
                Draft202012Validator.check_schema(json.loads(sf.read_text()))
            except Exception as e:
                errs.append(f"{sf.name}: {e}")
        if errs:
            for e in errs: print("FAIL", e)
            return 1
        print(f"OK: all {len(list(SCHEMAS.glob('*.schema.json')))} schemas pass meta-schema check.")
        return 0
    reg = load_registry()
    targets = [Path(t).resolve() for t in argv] if argv else sorted(list((ROOT / "derived").rglob("*.json")) + list((ROOT / "releases").rglob("*.json")))
    if not targets:
        print("validate (derived): nothing to check"); return 0
    all_errs = []
    for p in targets:
        errs = validate_instance(p, reg)
        if errs: all_errs.extend(errs)
        else:
            try: disp = str(p.relative_to(ROOT))
            except ValueError: disp = str(p)
            print(f"OK {disp}")
    if all_errs:
        for e in all_errs: print("FAIL", e)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
