# Important Signals and Assumptions Registry

## Relationship to Source Files

| registry section | canonical source | relationship |
| --- | --- | --- |
| P0 Signals | `current-synthesis.md`, `models/token-demand-envelope.md` | Summary of reversal signals; does not create a second numeric source. |
| P0 Assumptions | `models/token-demand-envelope.md` | Reads assumptions from the model and explains sensitivity. |

## P0 Signals

| signal_id | signal | current read | source rows | why it matters | reversal / action |
| --- | --- | --- | --- | --- | --- |
| DEMO-SIG-001 | Infrastructure supply lead times | Demo assumes some delivery constraints remain binding. | `DEMO-CAL-001` | Sustains scarcity rent while demand grows. | If lead times compress and inventory rises, downgrade bottleneck rent. |
| DEMO-SIG-002 | AI-specific revenue coverage | Demo assumes disclosure is still incomplete. | `DEMO-CAL-002` | Determines whether CapEx is productive or speculative. | If revenue/backlog fails to cover capital charges, move CapEx recovery to red. |
| DEMO-SIG-003 | Workflow pricing evidence | Demo assumes work-unit evidence is scarce. | `DEMO-CAL-003` | Determines whether applications retain profit. | If work-unit gross margin appears, upgrade workflow application layer. |

## P0 Assumptions

| assumption_id | assumption | current value / range | source rows | sensitivity | what would invalidate it |
| --- | --- | --- | --- | --- | --- |
| DEMO-ASM-001 | Demand grows with agentic usage, not just chat usage. | low/base/high scenarios | `DEMO-CAL-001` | High | Better primary usage data replacing the scenario envelope. |
| DEMO-ASM-002 | Model/API revenue does not equal operating surplus. | qualitative | `DEMO-CAL-002` | High | Primary P&L showing durable positive compute-adjusted margin. |
| DEMO-ASM-003 | Workflow value depends on system-of-record integration. | qualitative | `DEMO-CAL-003` | Medium | Broad standalone AI tools showing durable paid retention without workflow lock-in. |
