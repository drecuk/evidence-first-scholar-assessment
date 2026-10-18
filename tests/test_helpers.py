from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/evidence-first-scholar-assessment/skills/evidence-first-scholar-assessment"


class HelperTests(unittest.TestCase):
    def run_script(self, script: str, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SKILL / "scripts" / script), *args],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, expected, msg=result.stdout + result.stderr)
        return result

    def test_initialize_is_non_destructive(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp) / "Case"
            args = [str(case), "--candidate", "Test Scholar", "--domain", "Test Field", "--copy-template"]
            self.run_script("initialize_case.py", *args)
            report = case / "RESEARCH_IMPACT_REPORT.md"
            report.write_text("# User content\n", encoding="utf-8")
            second = self.run_script("initialize_case.py", *args)
            self.assertIn("PRESERVED RESEARCH_IMPACT_REPORT.md", second.stdout)
            self.assertEqual(report.read_text(encoding="utf-8"), "# User content\n")
            self.assertTrue((case / "inputs/research-quality-scholarly-impact-template.docx").is_file())

    def test_metric_calculation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            source = temp_path / "works.csv"
            with source.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=[
                    "work_id", "title", "year", "candidate_identity_status", "citations_source_1",
                    "fwci", "top_10_percent", "affiliation_countries",
                ])
                writer.writeheader()
                writer.writerows([
                    {"work_id": "w1", "title": "One", "year": "2025", "candidate_identity_status": "confirmed", "citations_source_1": "10", "fwci": "2.0", "top_10_percent": "true", "affiliation_countries": "CN;GB"},
                    {"work_id": "w2", "title": "Two", "year": "2024", "candidate_identity_status": "confirmed", "citations_source_1": "2", "fwci": "0.5", "top_10_percent": "false", "affiliation_countries": "CN"},
                    {"work_id": "w3", "title": "Probable", "year": "2023", "candidate_identity_status": "probable", "citations_source_1": "100", "fwci": "9", "top_10_percent": "true", "affiliation_countries": "US;CA"},
                ])
            output_dir = temp_path / "out"
            self.run_script(
                "calculate_metrics.py", str(source), "--output-dir", str(output_dir),
                "--provider", "Test Provider", "--assessment-year", "2026", "--snapshot-date", "2026-10-18",
            )
            result = json.loads((output_dir / "benchmark_metrics.json").read_text(encoding="utf-8"))
            metrics = {item["metric"]: item["value"] for item in result["metrics"]}
            self.assertEqual(metrics["validated_work_count"], 2)
            self.assertEqual(metrics["total_citations"], 12)
            self.assertEqual(metrics["h_index"], 2)
            self.assertEqual(metrics["i10_index"], 1)
            self.assertAlmostEqual(metrics["top_1_citation_concentration"], 10 / 12)
            self.assertAlmostEqual(metrics["international_collaboration_share"], 0.5)


if __name__ == "__main__":
    unittest.main()

