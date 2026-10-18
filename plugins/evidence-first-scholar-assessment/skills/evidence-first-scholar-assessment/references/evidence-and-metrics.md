# Evidence and metrics

## Source hierarchy

Use sources according to the claim they can establish.

1. **Primary and auditable:** the output itself; publisher and DOI metadata; official award, patent, standards, regulatory, policy, or adoption records; candidate-supplied documents labeled as such.
2. **Structured scholarly databases:** Scopus, Web of Science, OpenAlex, Dimensions, Lens, Crossref, PubMed, Semantic Scholar, DBLP, INSPIRE, RePEc, SSRN, Google Scholar, or domain equivalents.
3. **Institutional and independent secondary sources:** repositories, government and professional bodies, independent reports, reputable media documenting actual use.
4. **Discovery-only:** search snippets, social profiles, aggregators, press releases, and promotional biographies. Use them to locate stronger evidence, not to carry a material judgment.

Archive lawful copies or stable metadata for decisive sources. Record inaccessible and unsuccessful searches. Never claim to have read paywalled or blocked content that was not accessible.

## Corpus and lineage rules

- Calculate from identity-confirmed, in-scope works rather than a raw author profile.
- Keep provider-specific citation counts separate; never sum them.
- Record raw retrievals before manual cleaning and preserve pagination, query/filter, date, and version information.
- Make deduplication, date, document-type, field, missing-value, and fractional-counting rules explicit.
- Generate human-readable CSV and machine-readable JSON where practical.
- Fail visibly when a required corpus or preregistered peer is missing.
- Validate unique work IDs, non-negative counts, valid denominators, shares between zero and one, deterministic ordering, and report/table agreement.

## Productivity and currency

Report validated works by type, five- and ten-complete-year outputs, current partial-year outputs, active-year rate, recent citation flow, current accepted/in-press work supported by documentation, and recent verified leading-contribution share.

Raw output volume is discipline-sensitive. Do not compare book-centered, conference-centered, and high-volume biomedical records without adaptation.

## Citation scale and durability

From one named provider and snapshot date, compute:

- total citations;
- h-index and i10-index;
- median citations per work;
- citations attached to recent works;
- publication-age profile and continuing citation flow to older work;
- self-citation-adjusted and coauthor-adjusted reach when reliable data exist;
- independent citing groups and consequential citation contexts where feasible.

Use h-index and i10-index only as contextual descriptors. They combine productivity and citations, vary by field/career length/database, and do not measure originality, rigour, or individual contribution.

## Google Scholar

Take a dated profile snapshot only after checking identity, duplicates, and omissions. Record displayed name, affiliation, verified-email domain, URL, all self-declared interests, citation values, h-index values, i10-index values, public/private state, and suspected data problems.

Keep the raw profile snapshot separate from recomputed metrics. For interest labels, record exact token/URL, locale, signed-in state, page size, page, row, timestamp, substantiation from outputs, and a repeat observation when feasible. If position is reproducible, calculate only:

```text
observed position = (page number - 1) * results per page + row position
```

Do not call this an official field/world rank or calculate a percentile without a complete, stable, enumerable denominator. Give interest-label visibility no automatic points.

## Field-normalized influence

Where stable, report provider-defined FWCI/CNCI or equivalent, median and mean normalized impact, share above world average, top-1/5/10-percent shares, and stability intervals. State eligible denominators and field/year/document-type classification. Small samples, database undercoverage, and unstable classifications require wide uncertainty and cautious language.

## Concentration and breadth

For descending citation counts `c` and total `T`:

```text
top-k concentration = sum(c[0:k]) / T
```

Report top-1, top-2, top-5, and top-10 concentration where meaningful, plus the number of works accounting for 50% and 80% of citations. High concentration is not automatically adverse; it makes close reading and contribution attribution to decisive works especially important.

## Reach, reuse, and collaboration

Consider international collaboration share, institutional and geographic diversity, repeat/new collaborators, cross-domain engagement, independent replication or extension, method/theory adoption, dataset/software reuse, and a sample of consequential citation contexts. Large teams or international addresses do not themselves establish leadership or reach.

## Authorship and contribution

Interpret sole/first/middle/last/corresponding/consortium roles using field conventions. Seek CRediT-style evidence for conceptualization, methodology, investigation, formal analysis/software, validation, funding acquisition, original drafting, and review/editing. Record roles as lead, equal, supporting, claimed, or independently verified with a confidence level. Do not build a mechanical author-position score.

## Robustness, openness, and integrity

Check data/code/protocol/instrument availability, preregistration or equivalent safeguards, independent validation, coherence between methods and conclusions, limitations and uncertainty reporting, correction/retraction history, duplicated outputs, and material criticism. Interpret openness against field, ethical, legal, confidentiality, and historical norms. Missing open materials are not automatically evidence of poor research.

## Core formulas

```python
from statistics import median

citations = sorted(citations, reverse=True)
total_citations = sum(citations)
h_index = max(
    (rank for rank, count in enumerate(citations, start=1) if count >= rank),
    default=0,
)
i10_index = sum(count >= 10 for count in citations)
median_citations = median(citations) if citations else 0
top_5_concentration = sum(citations[:5]) / total_citations if total_citations else 0
```

The packaged `scripts/calculate_metrics.py` implements these descriptive calculations and selected normalized/share metrics. Inspect its output metadata and limitations; do not treat it as a scoring engine.

