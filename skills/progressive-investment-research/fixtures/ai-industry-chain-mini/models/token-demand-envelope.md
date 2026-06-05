# Token Demand Envelope / Demo Calculation Model

This is a public fixture model. The values below are illustrative placeholders, not market facts.

## Model Purpose

Show how a dossier records a formula-backed scenario without hiding the reasoning in prose.

## Calculation Sheet

| row_id | metric | low | base | high | unit | formula / note | review_status |
| --- | --- | ---: | ---: | ---: | --- | --- | --- |
| DEMO-CAL-001 | annual agent users | 25 | 100 | 250 | million users | scenario assumption | demo_only |
| DEMO-CAL-002 | tokens per active user per month | 10 | 50 | 150 | million tokens | scenario assumption | demo_only |
| DEMO-CAL-003 | annual token demand | 3,000 | 60,000 | 450,000 | trillion tokens/year | users * monthly tokens * 12 / 1e6 | demo_only |

## Readout

The model is useful only as a transmission scaffold. Before it can support an investment conclusion, each input needs source-backed rows, date stamps, and a normalization rule.

## Missing Evidence

- Primary usage disclosure by product or workload.
- Effective paid token price after discounting and caching.
- Compute cost per token by model class.
- Work-unit completion metrics for enterprise usage.
