# Equity Research Playbook

The templates and checklists a research analyst actually uses — initiation,
earnings review, forensic red flags, and a valuation sanity check — written
so that a junior analyst can produce work a senior can review in one pass.

> Educational use only. Templates are not investment advice and not a
> recommendation on any security. Any company example filled into a template
> must cite its source (annual report, filing, exchange data) on the same page.

## Contents

- `templates/initiation-report.md` — full initiation structure: thesis in one
  paragraph, business, industry, financials, valuation, risks, what would
  change the thesis.
- `templates/earnings-review.md` — quarter vs expectation vs last year, with
  a "what actually moved" section and a "what to ask management" section.
- `templates/forensic-checklist.md` — red flags: revenue vs cash, receivables
  vs sales, related parties, auditor changes, tax items, one-off gains.
- `templates/valuation-sanity-check.md` — before you publish a target price:
  implied growth, implied margins, peer multiples, downside case, and the
  question "what has to be true for this price to be right?"
- `templates/data-first-checklist.md` — before any conclusion is written:
  source, licence, and freshness check; every number with source and
  period; confirmation before pattern; downside and falsifier.
- `templates/structured-debate.md` — parallel analysts, Bull/Bear debate, risk scenarios, publication gate
- `templates/ledger-control-checklist.md` — frozen inputs, control totals, cut-off, restatement log
- `templates/research-to-use-case.md` — from a finding to a testable
  proposal: specific use case, evidence gate, and kill criteria written
  before scoring. Testable, not proven; never a recommendation.
- `examples/bottlers-nepal-terai-initiation-example.md` — a filled
  initiation report for Bottlers Nepal (Terai) (BNT, NEPSE), built
  from the verified-inputs ledger of October 2026. Labelled on its
  first lines as an **illustrative filled template, NOT a valuation**:
  no DCF, no target price, no rating, no recommendation. Every figure
  carries its source and period on the page, or is labelled UNKNOWN.
- `scripts/check_template.py` — a stdlib-only, deterministic
  template-completeness checker (see below), with tests in
  `tests/test_check_template.py`.

## The standard this playbook enforces

1. **Thesis first, numbers second.** If the thesis cannot be written in one
   paragraph, the model is not ready.
2. **Every number has a source and a date.** "Revenue fell" is not a fact;
   "Revenue fell 14.2% in FY 2081/82 per the audited annual report" is.
3. **Show the downside.** A report with no bear case is a pitch, not research.
4. **Say what would change your mind.** A thesis with no falsifier is unfalsifiable.

## How to use it

Copy a template into a new file, fill it, delete nothing structural — if a
section does not apply, write "Not applicable, because…" rather than deleting it.
A reviewer should be able to see what you considered, not just what you concluded.

## Quick start

1. Copy the template you need from `templates/` into a new file.
2. Fill it in, deleting nothing structural — if a section does not apply,
   write "Not applicable, because…" rather than deleting it.
3. Cite the source of every company number on the same page, and state
   what would change your conclusion.
4. Run the checker on your filled file (see below) before sharing it.

## Template-completeness checker (executable verification)

The playbook now has executable verification for template structure —
not for the truth of any figure:

```sh
python scripts/check_template.py examples/bottlers-nepal-terai-initiation-example.md
python scripts/check_template.py my-filled-report.md --template earnings
python scripts/check_template.py --list-templates
```

The checker (Python 3.12, stdlib only, no dependencies) reports every
required section that is missing or present-but-empty, and exits 1 in
that case; it exits 0 only when all required sections are present with
content. `--template` defaults to auto-detection across all eight
template types. Run its tests with:

```sh
python -m pytest tests/ -v
```

What the checker does NOT do: it does not verify sources, arithmetic,
or valuation logic, and it does not judge whether a filled template is
a valuation. A file can pass the checker and still be an illustrative
example only — as the Bottlers Nepal (Terai) example is, by its own
label. Sourcing and valuation honesty remain the author's job.

## Limitations

- The templates are blank structures; the one filled example is
  labelled EXAMPLE / illustrative filled template, NOT a valuation,
  and must cite its source on the same page.
- A completed template is still one analyst's work, not a verified
  valuation and not a recommendation.
- The checker verifies section structure only, not figure accuracy.
- Nothing here is a live data source.

> Research only, not investment advice; never a buy/sell recommendation

See `CONTRIBUTING.md` for how to contribute and `SECURITY.md` for how to
report a security issue privately.

## License

MIT for the templates. Company data filled into them remains subject to its
original source's terms.
