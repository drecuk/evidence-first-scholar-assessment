# Validation report — 1.0.1

Validation date: 2026-10-18

## Result

**PASS** for Git-backed marketplace distribution and portable package handoff.

## Package

- Archive: `evidence-first-scholar-assessment-1.0.1.zip`
- SHA-256: `2ec3ab4230833a43ce4823815f2d1e24f19c9d1c6cdf53da05a5cd6a37c1e040`
- Archive layout: one enclosing `evidence-first-scholar-assessment/` directory
- Archive entries: 27
- MCP servers: 0
- Skills: 1

## Checks performed

- Root portable manifest parsed and passed the published Agent Plugins 1.0 JSON Schema.
- Codex compatibility manifest and marketplace catalog parsed as valid JSON.
- Both manifests declare version `1.0.1` and SPDX license identifier `Apache-2.0`.
- Canonical Apache License 2.0 text and the attribution `NOTICE` are present at repository and package level; paired copies match.
- `agents/openai.yaml` parsed as valid YAML.
- Plugin identifier and semantic version validated.
- Display name: 29/30 characters.
- Short description: 28/30 characters.
- Long description: 509/4000 characters.
- Three starter prompts are single-line and within 128 characters.
- Logo and composer icon paths resolve to a 1254 × 1254 PNG (1,178,035 bytes).
- Icon was downscaled and visually inspected at 48 × 48 pixels.
- Skill passed the bundled quick validator; `SKILL.md` is 7,314 bytes.
- Helper scripts compiled successfully.
- Two helper behavior tests passed: non-destructive case initialization and deterministic metric calculation.
- The report-template DOCX passed ZIP-container integrity testing.
- The release archive passed compression, unsafe-path, prohibited-file, single-root, license, and notice checks.
- A clean extraction repeated skill, script-entrypoint, DOCX, published-schema, version, license, and attribution validation successfully.

Machine-readable details are in `docs/validation-report.json`.

## Scope and caveats

This validates the package, marketplace layout, and deterministic helpers; it does not certify the substantive accuracy of a future scholar assessment. Each assessment still requires identity validation, lawful evidence access, disciplinary expertise, genuine expert review where required, candidate correction opportunity, and case-specific QA.

The package is ready for direct Git-backed marketplace distribution. OpenAI universal public directory submission remains a separate publisher-controlled review process and is not claimed here.

