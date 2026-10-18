# Evidence-First Scholar Assessment

Evidence-First Scholar Assessment is a Codex plugin for rigorous, auditable evaluation of an academic's research quality and scholarly influence.

The evaluator begins by validating the scholar's bibliographic identity, reads and evaluates selected outputs, attributes the candidate's contribution, examines scholarly uptake and durability, compares genuinely similar peers under common rules, and makes uncertainty visible. It does not turn a Google Scholar total, journal title, university affiliation, or administrative rank into a quality judgment.

## Instruction Prompt

The instruction prompt is simple:

```
   Evaluate this scholar: [provide a web link to the scholar profile/bio, or a google scholar page]
   Generate a comprehensive PDF report
```

## DORA-informed assessment

[DORA](https://sfdora.org/) is the San Francisco Declaration on Research Assessment, a global initiative to improve how research and researchers are evaluated. Its central recommendation is to assess research on its own merits rather than use journal-based metrics as a substitute for the quality of individual work. See [Read the Declaration](https://sfdora.org/read/) and DORA's [guidance on responsible quantitative indicators](https://sfdora.org/resource/guidance-on-the-responsible-use-of-quantitative-indicators-in-research-assessment/).

This plugin is **DORA-informed**, not DORA-certified, endorsed, or affiliated. Qualitative assessment of outputs leads; transparent and contextual indicators support it.

The plugin can use dated, identity-checked citation counts, h-index values, and i10-index values as descriptive context and cross-check them against a validated work corpus.

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

## Install from this GitHub repository

1. Install or open the ChatGPT desktop app. It is required separately from Node.js and Codex CLI.
2. Install a supported [Node.js LTS release](https://nodejs.org/) if it is not already available. Node.js 22 or later is recommended. Node.js supplies the runtime and the `npm` package manager used to install Codex CLI.
3. Check that Node.js and npm are available in your console or terminal:

   ```sh
   node --version
   npm --version
   ```

4. Install Codex CLI separately:

   ```sh
   npm install -g @openai/codex@latest
   ```

5. Check that Codex is available:

   ```sh
   codex --version
   ```

6. Add this repository as a Codex plugin marketplace:

   ```sh
   codex plugin marketplace add drecuk/evidence-first-scholar-assessment
   ```

7. Restart the ChatGPT desktop app so the new marketplace is loaded.
8. Open the **Plugins Directory**, select the **drecuk Scholar Tools** marketplace, open **Evidence-First Scholar Review**, and select **Install**.
9. Start a new conversation and try a research-assessment request such as:

   > Assess the research quality and scholarly impact of Professor [Name] for a senior appointment. Begin by validating bibliographic identity and evidence access, and use a DORA-informed, evidence-first method.

10. Supply the relevant CV, institutional profile, publication list, Google Scholar profile, ORCID, or other identifiers that you are authorized to use. Review the proposed scope, evidence-access plan, identity decisions, date windows, and peer-selection rule. Request corrections before the evaluator relies on the corpus.
11. When the identity and assessment rules are correct, explicitly confirm them, for example:

    > The identity, corpus rules, date windows, and peer-selection approach are approved. Continue with the full assessment and matched-peer benchmark.

12. Review the generated report, committee brief, evidence tables, source and search logs, claims ledger, metrics, sensitivity analysis, and QA record. The plugin supports expert and committee judgment; it does not make an appointment decision or turn bibliometric indicators into an automatic ranking.

To refresh the repository package after a new release:

```sh
codex plugin marketplace upgrade drecuk-scholar-tools
```

Restart the ChatGPT desktop app after upgrading if the new version does not appear immediately.

You can also clone the repository and add its root as a local marketplace:

```sh
codex plugin marketplace add ./evidence-first-scholar-assessment
```

The [release ZIP](https://github.com/drecuk/evidence-first-scholar-assessment/releases/latest) is retained for direct downloads, private upload, and package submission. Repository users should normally use the marketplace installation steps above.

## Example prompts

- “Assess this scholar's research quality and impact using an evidence-first, DORA-informed approach.”
- “Audit this Google Scholar profile for identity errors and explain what the metrics do—and do not—show.”
- “Create an auditable research assessment with matched peers and sensitivity analysis.”

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

