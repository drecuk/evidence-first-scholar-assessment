# Evidence-First Scholar Assessment

Evidence-First Scholar Assessment is a Codex plugin for rigorous, auditable evaluation of an academic's research quality and scholarly influence. It is intended for promotion and tenure, senior appointments, chair-professorship review, peer benchmarking, and research due diligence.

The evaluator begins with the work itself: it validates the scholar's bibliographic identity, reads and evaluates selected outputs, attributes the candidate's contribution, examines scholarly uptake and durability, compares genuinely similar peers under common rules, and makes uncertainty visible. It does not turn a Google Scholar total, journal title, university affiliation, or administrative rank into a quality judgment.

## DORA-informed assessment

[DORA](https://sfdora.org/) is the San Francisco Declaration on Research Assessment, a global initiative to improve how research and researchers are evaluated. Its central recommendation is to assess research on its own merits rather than use journal-based metrics as a substitute for the quality of individual work. See [Read the Declaration](https://sfdora.org/read/) and DORA's [guidance on responsible quantitative indicators](https://sfdora.org/resource/guidance-on-the-responsible-use-of-quantitative-indicators-in-research-assessment/).

This plugin is **DORA-informed**, not DORA-certified, endorsed, or affiliated. Qualitative assessment of outputs leads; transparent and contextual indicators support it.

Google Scholar profiles do not inherently conflict with DORA. The plugin can use dated, identity-checked citation counts, h-index values, and i10-index values as descriptive context and cross-check them against a validated work corpus. It must not use those figures as automatic scores, proof of quality, universal thresholds, or substitutes for reading the research. Self-declared Google Scholar interest labels are treated only as observed discoverability signals—not official field rankings.

## What it does

- Separates candidate identity, included works, ambiguous records, and exclusions.
- Establishes an evidence-access plan before making claims.
- Reviews originality, significance, rigour, attributable contribution, and durability at output level.
- Recomputes transparent metrics from a validated bibliography and records provider, formula, window, denominator, and snapshot date.
- Uses matched peers and sensitivity analysis without false percentile precision.
- Audits authorship, intellectual leadership, robustness, openness, correction history, and integrity.
- Keeps funding and optional external impact in their proper evidentiary roles.
- Produces reports, data tables, source and search logs, a claims ledger, and a QA record.
- Includes a Word report template plus deterministic case-initialization, metric, and validation helpers.

It does **not** provide an automatic scholar ranking or replace disciplinary expert judgment. It never fabricates expert reviews. A report remains provisional when decision-critical evidence is unavailable.

## Install from the Git-backed marketplace

```bash
codex plugin marketplace add drecuk/evidence-first-scholar-assessment
```

Restart the ChatGPT desktop app, open the Plugins Directory, choose **drecuk Scholar Tools**, and install **Evidence-First Scholar Review**.

To refresh later:

```bash
codex plugin marketplace upgrade drecuk-scholar-tools
```

You can also clone the repository and add its root as a local marketplace:

```bash
codex plugin marketplace add ./evidence-first-scholar-assessment
```

## Example prompts

- “Assess this scholar's research quality and impact using an evidence-first, DORA-informed approach.”
- “Audit this Google Scholar profile for identity errors and explain what the metrics do—and do not—show.”
- “Create an auditable chair-professorship research assessment with matched peers and sensitivity analysis.”

## Repository layout

```text
.agents/plugins/marketplace.json
plugins/evidence-first-scholar-assessment/
  plugin.json
  .codex-plugin/plugin.json
  assets/icon.png
  skills/evidence-first-scholar-assessment/
    SKILL.md
    agents/openai.yaml
    references/
    scripts/
    assets/research-quality-scholarly-impact-template.docx
```

The root `plugin.json` is the portable Agent Plugins manifest. The compatibility manifest supports older Codex plugin loaders. The plugin is skills-only: it does not bundle an MCP server, request credentials, or transmit data on its own. Research carried out by Codex may use tools and data sources the user authorizes in the host environment.

## Release package

The versioned ZIP contains one plugin folder and excludes the repository marketplace catalog. Its SHA-256 checksum and validation report are published with each GitHub release.

## Responsible use

Research assessment can materially affect careers. Reviewers remain responsible for lawful data use, conflicts of interest, disciplinary context, accessibility adjustments, candidate correction opportunities, and the final decision. Absence of public evidence is an evidence gap—not proof of absence or poor performance.

## Support

Please use [GitHub Issues](https://github.com/drecuk/evidence-first-scholar-assessment/issues) for reproducible problems, documentation gaps, or feature requests. Do not post confidential candidate materials or personal data in a public issue.

## Public directory status

This repository is prepared for direct Git-backed marketplace distribution. It is not represented as approved or listed in OpenAI's universal public Plugins Directory. See [submission readiness](docs/submission-readiness.md) for the remaining publisher-controlled steps.

