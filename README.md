# Evideris Curriculum — Derived Layer

**Sibling to [`esge-curriculum-schema`](https://github.com/Evideris-Systems/esge-curriculum-schema).**

This repo holds the **Evideris-derived layer** that builds on top of the ESGE source-canonical schema:

- **Competencies** — atomic skills decomposed from source recommendations (the recommendation is what ESGE prints; the competency is the atom you score a trainee on)
- **EPAs** — Entrustable Professional Activities; bundles of competencies with ten-Cate trust levels 1–5
- **Evidence criteria** — concrete evidence centres should provide to demonstrate compliance with a source standard (feeds the Centre Accreditation evidence-pack generator)
- **Competency assessments** — cross-refs from source recommendations to the atomic competencies they imply
- **CAT recommendation maps** — Evideris's reading of which recommendation each CAT line evidences, for CATs ESGE published without a recommendation column (GPAT); display and traceability only, never a scoring input
- **Primary-source scoring tools** — clinical scoring systems (NICE classification, JNET, Sydney DMI) that source curricula reference by name but define elsewhere

> ⚠️ **Provenance honesty:** Every artifact carries an explicit `_meta.provenance` block declaring `evideris-design`, `verbatim-from-primary-source`, `paraphrased-from-primary-source`, or `inferred-from-source`. There is no ambiguity about which work is ESGE's and which is Evideris's.

## Licence

[CC BY-NC-SA 4.0](./LICENSE) — share + adapt non-commercially with attribution + share-alike. Commercial licensing: contact Evideris Systems BV.

The sibling source repository separately licenses Evideris-authored schema,
validation code and release metadata under
[CC BY 4.0](https://github.com/Evideris-Systems/esge-curriculum-schema/blob/main/LICENSE).
Encoded ESGE/Thieme publication content retains its original rights; neither
repository's licence should be read as Evideris relicensing third-party source
material.

## Layout

```
schemas/                      # JSON Schema 2020-12 validators (derived artifact types)
  competency.schema.json
  epa.schema.json
  evidence-criterion.schema.json
  competency-assessment.schema.json
  cat-recommendation-map.schema.json
  scoring-tool.schema.json
  release.schema.json
releases/                     # r2026.07.json — manifest snapshot
derived/
  competency/<modality>/      # Atomic-skill descriptors
  epa/<modality>/             # Entrustable Professional Activities
  evidence-criterion/<modality>/  # Evidence specs feeding Centre Accreditation
  competency-assessment/<modality>/  # Rec → competency cross-refs
  cat-recommendation-map/       # CAT line → recommendation crosswalks (Evideris reading)
  scoring-tool/               # Primary-source scoring tools (NICE, JNET, Sydney DMI)
scripts/                      # Schema, completeness and release-hash validation
```

## Verification

```bash
make check
```

Runs schema meta-validation, JSON Schema validation, release path/hash/identity
verification and completeness checks. Completeness requires every artifact to
have an allowed `_meta.provenance` type, a substantive reason and a primary DOI
for primary-source-derived content; it also rejects known placeholder markers.
The repository does not currently run an automated primary-source text trace.

Release members are bound to a repository-relative path and raw-file SHA-256. After changing membership or a released artifact, run `python3 scripts/update-release-hashes.py --write --root derived releases/<release>.json`; `make check` verifies the result.

## How this relates to the source-canonical layer

- Source-canonical artifacts reference each other freely.
- Derived artifacts reference source-canonical via `derived_from: [<source-canonical lineageId>]`.
- Source-canonical artifacts NEVER reference derived artifacts (would create cyclic dependency on optional content).

Release `_meta` describes assembly of the manifest and lists every source
curriculum represented in the aggregate release. Each member artifact retains
its own more specific provenance.

When ESGE publishes a new curriculum, source-canonical gets the verbatim transcription (via the `esge-curriculum-autoupdate` Claude Code skill). The derived layer then gets a separate manual or assisted encoding pass to add Evideris's competencies/EPAs/evidence criteria mapping onto the new recs.

## Related

- Source-canonical schema: <https://github.com/Evideris-Systems/esge-curriculum-schema>
- Architecture rationale: `evideris/docs/plans/2026-06-27-correctness-architecture.md`
- Status snapshot: `evideris/docs/plans/2026-06-28-status.md`
