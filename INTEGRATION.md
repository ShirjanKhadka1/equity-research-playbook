> **SUPERSEDED (Round 3) — do not use the numbers below as current.**
> The canonical programme map is
> [`finance-research-agents/ops/SYSTEM-MAP.md`](https://github.com/ShirjanKhadka1/finance-research-agents/blob/main/ops/SYSTEM-MAP.md),
> and current counts live in each repo's generated `status.json`
> (produced by `scripts/generate_status.py`, checked by `scripts/check_numbers.py`).
> This file is kept in place, unchanged except for this banner and for
> count claims replaced by pointers below, so its history is preserved.
> Any number still visible below is historical, not current.

# Integration — equity-research-playbook

## Role in the system
The structuring layer. Agents think, the toolkit calculates, and these
templates make sure the answer is complete — no missing downside, no
deleted risk section, no valuation without a sanity check.

## Templates and who fills them
| Template | Filled by |
|---|---|
| initiation-report.md | investment-researcher, then financial + valuation agents |
| earnings-review.md | financial-analyst, then reality-checker |
| forensic-checklist.md | forensic-analyst |
| valuation-sanity-check.md | valuation-analyst |

## Rule that makes it work
A section that does not apply is answered "Not applicable, because…",
never deleted. Deleting a section is how a risk disappears from a report.
## Connections
- Used by: finance-research-agents (all runbooks).
- Used in: nepal-market-research case studies, nepali-capital-market-research
  market reviews (adapted, not copied blindly).
