#!/usr/bin/env python3
"""Calculate transparent descriptive metrics from an identity-validated works CSV."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import date
from pathlib import Path
from statistics import mean, median
from typing import Any


TRUE_VALUES = {"1", "true", "yes", "y"}


def parse_nonnegative_int(value: str, field: str, row_number: int) -> int:
    text = (value or "").strip().replace(",", "")
    if text == "":
        raise ValueError(f"Row {row_number}: missing {field}")
    number = int(float(text))
    if number < 0:
        raise ValueError(f"Row {row_number}: {field} must be non-negative")
    return number


def parse_optional_float(value: str, field: str, row_number: int) -> float | None:
    text = (value or "").strip()
    if not text:
        return None
    number = float(text)
    if not math.isfinite(number):
        raise ValueError(f"Row {row_number}: {field} must be finite")
    return number


def parse_optional_bool(value: str) -> bool | None:
    text = (value or "").strip().lower()
    if not text:
        return None
    if text in TRUE_VALUES:
        return True
    if text in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"Invalid Boolean value: {value!r}")


def works_for_share(citations: list[int], threshold: float) -> int:
    total = sum(citations)
    if total == 0:
        return 0
    running = 0
    for index, count in enumerate(sorted(citations, reverse=True), start=1):
        running += count
        if running / total >= threshold:
            return index
    return len(citations)


def share_with_flag(rows: list[dict[str, Any]], key: str) -> tuple[float | None, int]:
    eligible = [row[key] for row in rows if row.get(key) is not None]
    if not eligible:
        return None, 0
    return sum(bool(value) for value in eligible) / len(eligible), len(eligible)


def load_rows(path: Path, citation_column: str | None, include_probable: bool) -> tuple[list[dict[str, Any]], str]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("Input CSV has no header")
        resolved_citation_column = citation_column
        if not resolved_citation_column:
            for candidate in ("citations", "citations_source_1"):
                if candidate in reader.fieldnames:
                    resolved_citation_column = candidate
                    break
        if not resolved_citation_column or resolved_citation_column not in reader.fieldnames:
            raise ValueError("No citation column found; use --citation-column")
        required = {"work_id", "title", "year", resolved_citation_column}
        missing = required - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

        rows: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for row_number, raw in enumerate(reader, start=2):
            work_id = (raw.get("work_id") or "").strip()
            if not work_id:
                raise ValueError(f"Row {row_number}: missing work_id")
            if work_id in seen_ids:
                raise ValueError(f"Row {row_number}: duplicate work_id {work_id!r}")
            seen_ids.add(work_id)

            status = (raw.get("candidate_identity_status") or "confirmed").strip().lower()
            if status == "probable" and not include_probable:
                continue
            if status not in {"confirmed", "probable"}:
                continue
            year = parse_nonnegative_int(raw.get("year", ""), "year", row_number)
            citations = parse_nonnegative_int(raw.get(resolved_citation_column, ""), resolved_citation_column, row_number)
            fwci = parse_optional_float(raw.get("fwci", ""), "fwci", row_number)
            top_10 = parse_optional_bool(raw.get("top_10_percent", ""))
            countries_text = (raw.get("affiliation_countries") or "").strip()
            countries = {part.strip() for part in countries_text.replace("|", ";").split(";") if part.strip()}
            rows.append({
                "work_id": work_id,
                "title": (raw.get("title") or "").strip(),
                "year": year,
                "citations": citations,
                "fwci": fwci,
                "top_10_percent": top_10,
                "countries": countries,
            })

    if not rows:
        raise ValueError("No confirmed/probable rows remain after filtering")
    return rows, resolved_citation_column


def metric(name: str, value: Any, numerator: Any = None, denominator: Any = None, definition: str = "") -> dict[str, Any]:
    return {
        "metric": name,
        "value": value,
        "numerator": numerator,
        "denominator": denominator,
        "definition": definition,
    }


def calculate(rows: list[dict[str, Any]], assessment_year: int) -> list[dict[str, Any]]:
    citations = sorted((row["citations"] for row in rows), reverse=True)
    total = sum(citations)
    h_index = max((rank for rank, count in enumerate(citations, start=1) if count >= rank), default=0)
    i10 = sum(count >= 10 for count in citations)
    complete_year_end = assessment_year - 1
    five_year_start = assessment_year - 5
    ten_year_start = assessment_year - 10
    five_year = [row for row in rows if five_year_start <= row["year"] <= complete_year_end]
    ten_year = [row for row in rows if ten_year_start <= row["year"] <= complete_year_end]
    partial_year = [row for row in rows if row["year"] == assessment_year]
    years = sorted({row["year"] for row in rows if row["year"] <= assessment_year})
    career_span = assessment_year - min(years) + 1 if years else 0
    active_year_rate = len(years) / career_span if career_span else None
    fwci_values = [row["fwci"] for row in rows if row["fwci"] is not None]
    above_world = sum(value > 1 for value in fwci_values) / len(fwci_values) if fwci_values else None
    top_10_share, top_10_denominator = share_with_flag(rows, "top_10_percent")
    country_rows = [row for row in rows if row["countries"]]
    international_count = sum(len(row["countries"]) > 1 for row in country_rows)
    international_share = international_count / len(country_rows) if country_rows else None

    metrics = [
        metric("validated_work_count", len(rows), len(rows), len(rows), "Confirmed works; probable works only when explicitly included."),
        metric("total_citations", total, total, len(rows), "Sum from one selected citation column; never combine providers."),
        metric("h_index", h_index, None, len(rows), "Maximum h such that h works have at least h citations."),
        metric("i10_index", i10, i10, len(rows), "Works with at least 10 citations."),
        metric("median_citations_per_work", median(citations), None, len(rows), "Median citations across the validated corpus."),
        metric("mean_citations_per_work", mean(citations), total, len(rows), "Mean citations; report with median because the distribution is often skewed."),
        metric("five_complete_year_work_count", len(five_year), len(five_year), len(rows), f"Works published {five_year_start}–{complete_year_end}."),
        metric("ten_complete_year_work_count", len(ten_year), len(ten_year), len(rows), f"Works published {ten_year_start}–{complete_year_end}."),
        metric("current_partial_year_work_count", len(partial_year), len(partial_year), len(rows), f"Works published in partial year {assessment_year}."),
        metric("active_year_rate", active_year_rate, len(years), career_span, "Years with a validated work divided by career-span years."),
        metric("top_1_citation_concentration", sum(citations[:1]) / total if total else 0, sum(citations[:1]), total, "Share of citations from the most cited work."),
        metric("top_2_citation_concentration", sum(citations[:2]) / total if total else 0, sum(citations[:2]), total, "Share of citations from the two most cited works."),
        metric("top_5_citation_concentration", sum(citations[:5]) / total if total else 0, sum(citations[:5]), total, "Share of citations from the five most cited works."),
        metric("top_10_citation_concentration", sum(citations[:10]) / total if total else 0, sum(citations[:10]), total, "Share of citations from the ten most cited works."),
        metric("works_accounting_for_50_percent_citations", works_for_share(citations, 0.5), None, len(rows), "Minimum number of leading works reaching 50% of citations."),
        metric("works_accounting_for_80_percent_citations", works_for_share(citations, 0.8), None, len(rows), "Minimum number of leading works reaching 80% of citations."),
        metric("median_fwci", median(fwci_values) if fwci_values else None, None, len(fwci_values), "Median provider-defined FWCI among eligible works."),
        metric("mean_fwci", mean(fwci_values) if fwci_values else None, None, len(fwci_values), "Mean provider-defined FWCI among eligible works."),
        metric("above_world_average_fwci_share", above_world, sum(value > 1 for value in fwci_values), len(fwci_values), "Share of eligible works with FWCI > 1."),
        metric("top_10_percent_work_share", top_10_share, sum(bool(row["top_10_percent"]) for row in rows if row["top_10_percent"] is not None), top_10_denominator, "Share of eligible works marked top 10% by the named provider."),
        metric("international_collaboration_share", international_share, international_count, len(country_rows), "Multi-country works divided by works with usable affiliation-country data."),
    ]
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--citation-column")
    parser.add_argument("--assessment-year", type=int, default=date.today().year)
    parser.add_argument("--snapshot-date", default=date.today().isoformat())
    parser.add_argument("--provider", required=True)
    parser.add_argument("--include-probable", action="store_true")
    args = parser.parse_args()

    rows, citation_column = load_rows(args.input_csv, args.citation_column, args.include_probable)
    metrics = calculate(rows, args.assessment_year)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "benchmark_metrics.csv"
    json_path = args.output_dir / "benchmark_metrics.json"

    metadata = {
        "source_file": str(args.input_csv.resolve()),
        "citation_provider": args.provider,
        "citation_column": citation_column,
        "snapshot_date": args.snapshot_date,
        "assessment_year": args.assessment_year,
        "identity_rule": "confirmed plus probable" if args.include_probable else "confirmed only",
        "limitations": [
            "Descriptive indicators do not measure originality, rigour, or individual contribution by themselves.",
            "Provider coverage, field classification, self-citation, and author identity require separate review.",
            "No automatic score or appointment decision is produced.",
        ],
    }

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = ["metric", "value", "numerator", "denominator", "definition", "provider", "snapshot_date"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in metrics:
            writer.writerow({**row, "provider": args.provider, "snapshot_date": args.snapshot_date})

    json_path.write_text(json.dumps({"metadata": metadata, "metrics": metrics}, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

