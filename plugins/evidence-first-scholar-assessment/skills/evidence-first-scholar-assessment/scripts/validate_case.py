#!/usr/bin/env python3
"""Validate the structure and core invariants of a scholar-assessment case."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIRED_FILES = [
    "README.md",
    "RUN_LOG.md",
    "QA_REPORT.md",
    "RESEARCH_IMPACT_REPORT.md",
    "COMMITTEE_BRIEF.md",
    "config/assessment_protocol.yaml",
    "data/identity_decisions.csv",
    "data/evidence_access_plan.csv",
    "data/candidate_validated_works.csv",
    "data/candidate_excluded_works.csv",
    "data/peer_selection.csv",
    "data/benchmark_sensitivity.csv",
    "data/contribution_attribution.csv",
    "data/robustness_integrity_audit.csv",
    "data/adversarial_audit.csv",
    "data/research_scorecard.csv",
    "data/evidence_gaps.csv",
    "data/claims_ledger.csv",
    "sources/source_manifest.csv",
    "sources/search_log.csv",
]


CSV_REQUIRED_COLUMNS = {
    "data/candidate_validated_works.csv": {"work_id", "title", "year", "candidate_identity_status", "citations_source_1"},
    "data/identity_decisions.csv": {"work_id", "identity_status", "decision_reason"},
    "data/peer_selection.csv": {"peer_id", "peer_name", "selection_reason", "included"},
    "data/claims_ledger.csv": {"claim_id", "claim_text", "source_ids", "evidence_status", "decision_relevance"},
    "sources/source_manifest.csv": {"source_id", "canonical_url", "retrieval_date", "evidence_tier", "access_status"},
    "sources/search_log.csv": {"search_id", "date_time", "source_or_database", "query", "access_result"},
}


PLACEHOLDER_MARKERS = {
    "Status: provisional scaffold.",
    "Status: not yet validated.",
    "TO_BE_FROZEN_BEFORE_RESULTS",
    "TO_BE_DEFINED",
    "TO_BE_RECORDED",
}


def check_csv(path: Path, required: set[str]) -> list[str]:
    errors: list[str] = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration:
            return [f"{path}: empty CSV"]
    missing = required - set(header)
    if missing:
        errors.append(f"{path}: missing columns {', '.join(sorted(missing))}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--allow-provisional", action="store_true", help="Treat scaffold markers as warnings rather than errors.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    root = args.case_dir.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        errors.append(f"Case directory does not exist: {root}")
    else:
        for relative in REQUIRED_FILES:
            path = root / relative
            if not path.is_file():
                errors.append(f"Missing required file: {relative}")
            elif path.stat().st_size == 0:
                errors.append(f"Empty required file: {relative}")

        for relative, required in CSV_REQUIRED_COLUMNS.items():
            path = root / relative
            if path.is_file():
                errors.extend(check_csv(path, required))

        for relative in ["README.md", "QA_REPORT.md", "RESEARCH_IMPACT_REPORT.md", "COMMITTEE_BRIEF.md", "config/assessment_protocol.yaml"]:
            path = root / relative
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            found = sorted(marker for marker in PLACEHOLDER_MARKERS if marker in text)
            if found:
                target = warnings if args.allow_provisional else errors
                target.append(f"{relative}: unfinished markers: {', '.join(found)}")

        reports = [root / "RESEARCH_IMPACT_REPORT.md", root / "COMMITTEE_BRIEF.md"]
        for path in reports:
            if path.is_file() and len(path.read_text(encoding="utf-8", errors="replace").split()) < 100:
                target = warnings if args.allow_provisional else errors
                target.append(f"{path.name}: fewer than 100 words")

    result = {
        "case_dir": str(root),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
    }
    output = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

