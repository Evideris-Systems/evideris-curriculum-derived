#!/usr/bin/env python3
"""Remove source/derived conflations found in the curriculum audit."""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def save(path: Path, document: dict) -> None:
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    competency_root = REPO_ROOT / "derived/competency/esd"
    for path in sorted(competency_root.glob("*.json")):
        document = load(path)
        for milestone in document.get("milestones", []):
            milestone.pop("expectedAtCases", None)
        document["_meta"]["encodedBy"] = "other:codex-source-fidelity-repair"
        document["_meta"]["encodedAt"] = "2026-08-09"
        save(path, document)

    selection_path = competency_root / "initial-human-esd-selection.v1.0.0.json"
    selection = load(selection_path)
    selection["description"]["en"] = (
        "Correct case selection for the first 20 human ESD procedures: lesions "
        "smaller than 30 mm in the antrum or rectum. Initial human ESD training "
        "in the colon is not recommended; other unsuitable lesions include those "
        "with scarring, ulceration, or a high risk of submucosal invasion."
    )
    save(selection_path, selection)

    epa_path = REPO_ROOT / "derived/epa/esd/independent-esd-practice.v1.0.0.json"
    epa = load(epa_path)
    epa["description"]["en"] = (
        "End-to-end independent performance of ESD—from lesion characterisation "
        "and case selection through dissection, defect management, and interpretation "
        "of histopathology—to a standard a supervisor can entrust without direct "
        "oversight."
    )
    epa.pop("requiredExposure", None)
    epa["_meta"]["provenance"]["reason"] = (
        "Forward-design EPA bundling the 10 Evideris-derived ESD competencies into "
        "an entrustable unit of independent practice. ESGE ESD 2019 does not formally "
        "enumerate EPAs or define a caseload threshold for initial entrustment. Its "
        "25-procedure annual threshold concerns maintenance of proficiency and is "
        "therefore not encoded as an EPA prerequisite."
    )
    epa["_meta"]["provenance"]["derived_from"] = ["cur-esd-2019"]
    epa["_meta"]["encodedBy"] = "other:codex-source-fidelity-repair"
    epa["_meta"]["encodedAt"] = "2026-08-09"
    save(epa_path, epa)

    poem_competency_root = REPO_ROOT / "derived/competency/poem-2"
    poem_competency_paths = sorted(poem_competency_root.glob("*.json"))
    for path in poem_competency_paths:
        document = load(path)
        for milestone in document.get("milestones", []):
            milestone.pop("expectedAtCases", None)
        document["_meta"]["encodedBy"] = "other:codex-source-fidelity-repair"
        document["_meta"]["encodedAt"] = "2026-08-09"
        save(path, document)

    poem_epa_path = REPO_ROOT / "derived/epa/poem-2/independent-poem.v1.0.0.json"
    poem_epa = load(poem_epa_path)
    poem_epa.pop("requiredExposure", None)
    poem_epa["_meta"]["provenance"]["reason"] = (
        "Forward-design EPA bundling the 12 Evideris-derived POEM competencies into "
        "an entrustable unit of independent practice. ESGE POEM 2025 Part II does not "
        "define a 20-case or 12-month threshold for independent entrustment, so no "
        "such threshold is encoded here."
    )
    poem_epa["_meta"]["encodedBy"] = "other:codex-source-fidelity-repair"
    poem_epa["_meta"]["encodedAt"] = "2026-08-09"
    save(poem_epa_path, poem_epa)

    print(
        "Repaired 10 ESD competencies, 12 POEM competencies, and both "
        "independent-practice EPAs"
    )


if __name__ == "__main__":
    main()
