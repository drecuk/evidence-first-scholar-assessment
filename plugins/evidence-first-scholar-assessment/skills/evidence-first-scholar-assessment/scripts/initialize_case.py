#!/usr/bin/env python3
"""Create a non-destructive scholar-assessment case workspace."""

from __future__ import annotations

import argparse
import csv
import shutil
from datetime import date
from pathlib import Path


DIRECTORIES = [
    "config",
    "inputs/original",
    "data",
    "sources/institutional",
    "sources/bibliometric_raw",
    "sources/publications",
    "sources/expert_review",
    "sources/independent_reviews_and_uptake",
    "sources/peers",
    "sources/replication_and_reuse",
    "sources/corrections_and_integrity",
    "sources/methodology",
    "sources/funding",
    "sources/optional_external_impact",
    "output/pdf",
    "output/rendered_pages",
    "tmp",
]


CSV_SCHEMAS = {
    "data/identity_decisions.csv": [
        "record_id", "work_id", "title", "year", "name_variant", "affiliation_signal",
        "coauthor_signal", "topic_signal", "identifier_signal", "identity_status",
        "decision_reason", "source_ids", "reviewer", "decision_date",
    ],
    "data/evidence_access_plan.csv": [
        "evidence_area", "required_for_decision", "discovery_input",
        "preferred_verification_source", "access_status", "coverage_assessment",
        "known_limitation", "candidate_document_request",
    ],
    "data/candidate_validated_works.csv": [
        "work_id", "title", "year", "output_type", "venue", "doi", "isbn", "url",
        "candidate_identity_status", "identity_reason", "authors", "author_count",
        "candidate_position", "candidate_corresponding", "candidate_contribution_evidence",
        "citations_source_1", "citations_source_2", "citation_snapshot_date", "fwci",
        "citation_percentile", "top_10_percent", "open_access", "primary_field",
        "primary_subfield", "affiliation_countries", "funding_acknowledgement", "grant_id", "candidate_grant_role",
        "scholarly_reuse_evidence", "optional_external_use_evidence", "notes",
    ],
    "data/candidate_excluded_works.csv": [
        "record_id", "title", "year", "identifier", "identity_status", "exclusion_reason",
        "source_ids", "notes",
    ],
    "data/research_trajectory.csv": [
        "phase_id", "start_year", "end_year", "research_strand", "questions", "methods",
        "important_outputs", "candidate_contribution", "scholarly_reception", "renewal_or_decline",
        "source_ids", "notes",
    ],
    "data/selected_output_expert_review.csv": [
        "work_id", "reviewer_id", "conflict_checked", "expertise_fit", "originality_0_5",
        "significance_0_5", "rigour_0_5", "attributable_contribution_0_5",
        "durability_0_5", "rationale", "evidence_references", "review_status", "notes",
    ],
    "data/peer_selection.csv": [
        "peer_id", "peer_name", "field_match", "subfield_match", "career_stage_match",
        "output_culture_match", "selection_reason", "identity_status", "included", "source_ids", "notes",
    ],
    "data/peer_validated_works.csv": [
        "peer_id", "work_id", "title", "year", "output_type", "doi", "identity_status",
        "citations", "fwci", "top_10_percent", "field", "subfield", "author_count", "notes",
    ],
    "data/benchmark_sensitivity.csv": [
        "scenario", "field_rule", "corpus_rule", "counting_rule", "metric", "candidate_value",
        "peer_median", "peer_iqr", "candidate_rank", "interpretation", "limitation",
    ],
    "data/cross_database_validation.csv": [
        "work_id", "title", "provider_a", "citations_a", "provider_b", "citations_b",
        "snapshot_date", "difference", "candidate_role", "document_type_checked", "notes",
    ],
    "data/google_scholar_profile_snapshot.csv": [
        "snapshot_date", "profile_url", "displayed_name", "affiliation", "verified_email_domain",
        "interests", "citations_all", "citations_recent", "h_index_all", "h_index_recent",
        "i10_index_all", "i10_index_recent", "identity_checked", "data_status", "limitations",
    ],
    "data/google_scholar_interest_labels.csv": [
        "interest_label", "provenance", "exact_label_url_token", "outputs_substantiation",
        "snapshot_conditions", "page", "row", "observed_position", "repeat_result",
        "interpretation_caveat",
    ],
    "data/contribution_attribution.csv": [
        "work_id", "contribution_type", "role_level", "evidence_source", "evidence_status",
        "confidence", "notes",
    ],
    "data/funding_context.csv": [
        "funder", "scheme", "grant_id", "title", "start_date", "end_date", "total_amount",
        "currency", "candidate_role", "verified_role_source", "co_investigators", "linked_outputs",
        "industry_partner", "reported_outcome", "evidence_status",
    ],
    "data/robustness_integrity_audit.csv": [
        "work_id_or_record", "area", "evidence_checked", "finding", "evidence_status",
        "source_ids", "materiality", "follow_up", "notes",
    ],
    "data/adversarial_audit.csv": [
        "test_id", "question", "scenario", "result", "effect_on_metrics", "effect_on_verdict",
        "evidence_reference", "status", "notes",
    ],
    "data/research_scorecard.csv": [
        "dimension", "weight", "lower_rating_0_5", "central_rating_0_5", "upper_rating_0_5",
        "central_weighted_points", "evidence_summary", "limitations",
    ],
    "data/evidence_gaps.csv": [
        "gap_id", "evidence_area", "missing_item", "search_or_request_made", "decision_relevance",
        "effect_on_confidence", "document_or_action_needed", "status",
    ],
    "data/claims_ledger.csv": [
        "claim_id", "report_section", "claim_text", "claim_type", "source_ids",
        "calculation_reference", "evidence_status", "confidence", "limitation",
        "decision_relevance", "last_checked",
    ],
    "sources/source_manifest.csv": [
        "source_id", "title", "source_type", "canonical_url", "provider", "publication_date",
        "retrieval_date", "local_path", "file_format", "sha256", "claim_supported",
        "evidence_tier", "access_status", "limitations", "notes",
    ],
    "sources/search_log.csv": [
        "search_id", "date_time", "evidence_area", "source_or_database", "query", "filters",
        "result_count", "relevant_records", "access_result", "files_saved", "follow_up", "notes",
    ],
}


def write_text_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def write_csv_if_missing(path: Path, header: list[str]) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(header)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--assessment-date", default=date.today().isoformat())
    parser.add_argument("--decision-context", default="Research assessment")
    parser.add_argument("--copy-template", action="store_true")
    args = parser.parse_args()

    root = args.case_dir.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    for directory in DIRECTORIES:
        (root / directory).mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    preserved: list[str] = []

    config = f"""assessment_date: {args.assessment_date}
candidate: {args.candidate!r}
domain: {args.domain!r}
decision_context: {args.decision_context!r}
case_status: provisional
scope:
  include: research_quality_and_scholarly_impact
  exclude:
    - administrative_titles
    - management
    - teaching_and_service
    - institutional_prestige
    - publicity
    - funding_volume_by_itself
windows:
  recent_complete_years: [5, 10]
  current_partial_year_separate: true
peer_selection_rule: TO_BE_FROZEN_BEFORE_RESULTS
expert_review_rule: TO_BE_DEFINED
metric_definitions: TO_BE_DEFINED
score_weights: TO_BE_DEFINED_IF_REQUIRED
database_access: TO_BE_RECORDED
"""

    files = {
        "config/assessment_protocol.yaml": config,
        "README.md": f"# {args.candidate}: research assessment case\n\n"
        f"- Assessment date: {args.assessment_date}\n"
        f"- Domain: {args.domain}\n"
        f"- Decision context: {args.decision_context}\n"
        "- Status: provisional\n\n"
        "## Principal deliverables\n\n"
        "- [Full report](RESEARCH_IMPACT_REPORT.md)\n"
        "- [Committee brief](COMMITTEE_BRIEF.md)\n"
        "- [QA report](QA_REPORT.md)\n\n"
        "## Reproduction\n\nRecord calculation, validation, and rendering commands here.\n\n"
        "## Identity warning and limitations\n\nPopulate before relying on metrics.\n",
        "RUN_LOG.md": f"# Run log\n\n- {args.assessment_date}: Case initialized.\n",
        "QA_REPORT.md": "# QA report\n\nStatus: not yet validated.\n",
        "RESEARCH_IMPACT_REPORT.md": "# Research quality and scholarly impact assessment\n\nStatus: provisional scaffold.\n",
        "COMMITTEE_BRIEF.md": "# Committee brief\n\nStatus: provisional scaffold.\n",
    }

    for relative, content in files.items():
        if write_text_if_missing(root / relative, content):
            created.append(relative)
        else:
            preserved.append(relative)

    for relative, header in CSV_SCHEMAS.items():
        if write_csv_if_missing(root / relative, header):
            created.append(relative)
        else:
            preserved.append(relative)

    if args.copy_template:
        source = Path(__file__).resolve().parent.parent / "assets" / "research-quality-scholarly-impact-template.docx"
        destination = root / "inputs" / "research-quality-scholarly-impact-template.docx"
        if destination.exists():
            preserved.append(str(destination.relative_to(root)))
        else:
            if not source.exists():
                raise FileNotFoundError(f"Packaged template not found: {source}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            created.append(str(destination.relative_to(root)))

    print(f"Case workspace: {root}")
    print(f"Created {len(created)} files; preserved {len(preserved)} existing files.")
    for item in created:
        print(f"CREATED {item}")
    for item in preserved:
        print(f"PRESERVED {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

