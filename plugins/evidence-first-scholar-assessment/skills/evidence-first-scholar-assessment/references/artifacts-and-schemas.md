# Artifacts, schemas, and quality assurance

## Recommended full-case layout

```text
CandidateName/
├── RESEARCH_IMPACT_REPORT.md
├── COMMITTEE_BRIEF.md
├── README.md
├── RUN_LOG.md
├── QA_REPORT.md
├── config/assessment_protocol.yaml
├── inputs/original/
├── data/
│   ├── identity_decisions.csv
│   ├── evidence_access_plan.csv
│   ├── candidate_validated_works.csv
│   ├── candidate_excluded_works.csv
│   ├── research_trajectory.csv
│   ├── selected_output_expert_review.csv
│   ├── peer_selection.csv
│   ├── peer_validated_works.csv
│   ├── benchmark_metrics.csv
│   ├── benchmark_metrics.json
│   ├── benchmark_sensitivity.csv
│   ├── cross_database_validation.csv
│   ├── google_scholar_profile_snapshot.csv
│   ├── google_scholar_interest_labels.csv
│   ├── contribution_attribution.csv
│   ├── funding_context.csv
│   ├── robustness_integrity_audit.csv
│   ├── adversarial_audit.csv
│   ├── research_scorecard.csv
│   ├── evidence_gaps.csv
│   └── claims_ledger.csv
├── sources/
│   ├── source_manifest.csv
│   ├── search_log.csv
│   ├── bibliometric_raw/
│   ├── publications/
│   ├── expert_review/
│   ├── peers/
│   ├── replication_and_reuse/
│   ├── corrections_and_integrity/
│   ├── methodology/
│   ├── funding/
│   └── optional_external_impact/
├── output/pdf/
├── output/rendered_pages/
└── tmp/
```

Adapt names when local conventions require it, but keep originals, raw sources, curated data, generated outputs, and temporary files separate. `scripts/initialize_case.py` creates a non-destructive version of this scaffold.

## Essential table schemas

### Candidate works

```text
work_id,title,year,output_type,venue,doi,isbn,url,
candidate_identity_status,identity_reason,authors,author_count,
candidate_position,candidate_corresponding,candidate_contribution_evidence,
citations_source_1,citations_source_2,citation_snapshot_date,
fwci,citation_percentile,top_10_percent,open_access,
primary_field,primary_subfield,funding_acknowledgement,grant_id,
candidate_grant_role,scholarly_reuse_evidence,optional_external_use_evidence,notes
```

### Source manifest

```text
source_id,title,source_type,canonical_url,provider,publication_date,
retrieval_date,local_path,file_format,sha256,claim_supported,
evidence_tier,access_status,limitations,notes
```

### Search log

```text
search_id,date_time,evidence_area,source_or_database,query,filters,
result_count,relevant_records,access_result,files_saved,follow_up,notes
```

### Claims ledger

```text
claim_id,report_section,claim_text,claim_type,source_ids,calculation_reference,
evidence_status,confidence,limitation,decision_relevance,last_checked
```

### Evidence access plan

```text
evidence_area,required_for_decision,discovery_input,preferred_verification_source,
access_status,coverage_assessment,known_limitation,candidate_document_request
```

## Full report outline

1. Evidence-only verdict and score if required.
2. Scope and exclusions.
3. Identity and data validity.
4. Independent assessment of selected outputs.
5. Research programme, trajectory, and substantive contributions.
6. Output, citation, normalized-impact, recency, concentration, reach, and uncertainty metrics.
7. Google Scholar profile and interest-label visibility with explicit non-ranking caveats.
8. Cross-database validation.
9. Field- and career-aligned peer comparison with sensitivity analysis.
10. Contribution attribution and intellectual leadership.
11. Robustness, openness, reproducibility, corrections, and integrity.
12. Verified funding context, explicitly unscored by amount/count/prestige.
13. Transparent scorecard and decision rule if used.
14. Research-only gate results.
15. Evidence required to change the conclusion.
16. Final assessment.
17. Appendices, sources, tables, and reproduction commands.
18. Optional external-impact annex, kept outside the research score.

Lead with the result rather than a biography. Separate facts, calculations, interpretation, and uncertainty.

## Completion gates

- **Workspace:** applicable artifacts exist and contain substantive content.
- **Identity:** splits, merges, duplicates, ambiguous and excluded records are documented.
- **Evidence:** supplied inputs and accessible selected outputs are reviewed; inaccessible evidence is logged.
- **Benchmark:** peer selection was frozen and rules are equivalent.
- **Reproducibility:** raw records, curated tables, formulas/scripts, dates, denominators, and commands can reproduce principal results.
- **Claims:** every decision-changing claim maps to evidence or calculation.
- **Reporting:** full report and brief agree on scope, verdict, score, gates, and date.
- **Presentation:** rendered documents are visually inspected and QA is recorded.

If a decision-critical genuine expert review, full text, database, or identity issue remains unresolved, complete unaffected work and mark the case **provisional**. Use **complete with limitations** only when residual gaps are not decision-critical and explain why.

## QA checklist

Before handoff:

1. Rerun calculations from archived inputs and record commands/runtime.
2. Check unique identifiers, non-negative counts, denominator validity, date windows, and peer symmetry.
3. Reconcile every number and claim among reports, tables, scorecard, and brief.
4. Check source links, local paths, hashes, and claims-ledger coverage.
5. Render the requested Word/PDF output and inspect every page for clipping, overflow, broken headings, unreadable notes, missing glyphs, blank pages, and stale values.
6. Confirm supplied originals were not modified and temporary files are not cited as evidence.
7. Record checks, warnings, and case status in `QA_REPORT.md` and principal links in `README.md`.

