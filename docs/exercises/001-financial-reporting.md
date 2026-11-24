# Exercise 001 — Automated Excel Financial Report Generator

Status: assigned; implementation not yet submitted.

This independent training and portfolio exercise is inspired by a public, closed Freelancer advertisement. It is not paid client work or an awarded contract.

## 1. Marketplace brief

Source: [Automated Excel Financial Report Generator](https://www.freelancer.com/projects/data-analysis/automated-excel-financial-report), project 40726196, consulted 2026-11-24.

Advertised budget: INR 12,500–37,500. The listing was closed, with 63 proposals and an average bid of INR 20,845 at review.

The client seeks repeatable reporting from financial records, including ledgers, balance sheets and transaction files, prioritizing reliability, speed and presentation over forecasting. Flat files (CSV/TSV) or database connectivity are contemplated. Reports need totals, averages, period changes and variance analysis, with an editable Excel dashboard, detail tabs and useful charts. Python/Pandas/openpyxl or alternatives that work on Windows 10 without additional licensing charges are acceptable.

Original acceptance targets: produce a populated workbook from the sample within two minutes; selectable input/output locations; totals within ±0.01% of manual checks; concise setup, dependency and extension documentation. Code should be modular and extensible.

## 2. Training scope and assumptions

These are exercise-specific decisions, not additional claims about the original client.

- Use Python 3.12, uv, pandas, openpyxl, pytest and Ruff, already declared in the repository.
- Start with a command-line tool and transaction CSV/TSV files. General ledger/balance-sheet schema mapping and optional database connectivity are follow-up scope.
- The local example path is `examples/financial/transactions.csv`. All public fixtures must be synthetic; never use personal bank data or client information.
- Input columns: date (ISO YYYY-MM-DD), description (nonempty text), amount (signed monetary value with at most two decimal places). One currency per file; no conversion. Positive amounts are income, negative amounts expenses, zero is neutral.
- Report by calendar month: income, expenses as positive magnitudes, net as income minus expenses, count and average signed transaction amount. Include empty months between the first and last dates.
- Month-over-month net change is current net minus prior net; percentage change is absolute change (signed difference) divided by the absolute prior net times 100. The first month and percentage changes against zero are unavailable. For budget variance, use actual net minus budget net, with an optional budget file containing month and budget_net. Missing budget is unavailable, not zero.
- Preserve exact cents in financial computations (e.g. integer cents or Decimal from original strings). Define rounding for averages and percentage displays. Do not construct Decimal from floats. Earlier float-based REPL exercises were exploratory.
- Reject invalid schema, dates, missing/invalid/nonfinite amounts and malformed records with helpful errors. Do not silently drop or deduplicate valid repeated records.
- Write one .xlsx with Summary, Monthly and Transactions sheets; add a chart of monthly income and expenses. Make summary/monthly formulas live against detail data for the existing period set. Document if adding new periods requires regeneration. Treat transaction descriptions as literal text, not Excel formulas.
- Windows 10 is a target, not a verified compatibility claim. Develop on Linux, then explicitly test or document the unverified status.

## 3. Milestones and exercises

Complete one milestone at a time. The developer writes the implementation; the mentor explains, asks questions and reviews rather than supplying an unsolicited full solution.

- [ ] M1 — Requirements and architecture: identify ambiguities, define module responsibilities, inputs/outputs, error contracts, dependencies and tests. Submit a short architecture note before implementing.
- [ ] M2 — Ingestion: load CSV and TSV through a configurable path; validate and normalize records; write happy-path and failure tests.
- [ ] M3 — Transformations: filter income and expenses, classify zero, group by description and calendar month; retain original details and avoid unintended mutation.
- [ ] M4 — Financial analysis: exact monetary totals, averages, monthly changes and budget variances; test zero and missing baselines.
- [ ] M5 — Workbook export: generate sheets, formatting, live formulas and chart; test workbook structure and formula references. Verify recalculation using Excel or a compatible spreadsheet application; openpyxl does not calculate formulas.
- [ ] M6 — CLI integration: selectable source, destination and optional budget paths, meaningful errors and exit statuses. Document invocation and overwrite behavior.
- [ ] M7 — QA: run unit and integration tests, Ruff, manual workbook checks and a repeatable performance benchmark. Record Windows compatibility evidence or limitations.
- [ ] M8 — Commercial delivery: complete usage README, sample input/output, release notes, time estimate and simulated bid. Present as self-directed portfolio work.

## 4. First assignment: design the architecture

Do not write new production code yet. Create `docs/exercises/001-architecture.md` and answer:

1. Which modules would you create and why? Which responsibilities belong together?
2. What is the input and return type of each public function? Consider Python annotations and your experience with Elixir typespecs and Elm.
3. Where should file I/O, input validation, pure financial computation and Excel output occur?
4. How will invalid input be communicated to callers?
5. How will you prevent floating-point errors and unintended DataFrame mutation?
6. Which questions would you ask the actual client before offering a fixed-price bid? Consider schema, accounting definitions, budget data, Windows delivery and expected data volume.
7. Identify the smallest useful deliverable and propose an implementation order.

No prescribed module layout is supplied: designing it is part of the exercise. A concise diagram or data-flow description is welcome. Commit your note for mentor review before M2.

## 5. Acceptance checks (training fixtures)

Use the ten synthetic transactions already explored in the Python REPL as a baseline. If your local fixture matches those records, the expected reference values are:

| Period | Income | Expenses | Net | Count |
| --- | ---: | ---: | ---: | ---: |
| 2026-01 | 2750.00 | 286.48 | 2463.52 | 7 |
| 2026-02 | 1800.00 | 114.99 | 1685.01 | 3 |
| Total | 4550.00 | 401.47 | 4148.53 | 10 |

January expenses consist of 45.99, 89.99, 125.50 and 25.00; February expenses are 89.99 and 25.00. Add independent fixtures covering zero, missing months, invalid rows, negative net, absent budget and zero budget. Compare exact-cent totals to independently calculated expectations; for the original percentage tolerance, require exact zero when the reference is zero.

Performance: generate a reproducible synthetic file of 10,000 records and measure end-to-end time from invocation to saved workbook; training target under 120 seconds on the recorded test machine. This substitute benchmark is not evidence of performance on the unavailable original dataset.

Quality gates (once tests exist):

```sh
uv run pytest
uv run ruff check .
```

Record actual results, not inferred passes. Check that output formulas recalculate when an existing detail amount changes and that a missing/zero denominator does not cause spreadsheet errors.

## 6. Learning workflow

Work in short increments: explain the concept, attempt an exercise, inspect the result, write a test, review and commit. Use Python/Elixir/Elm comparisons where helpful. Initial REPL lessons covered CSV loading, Series, Boolean masks, row filtering, combined conditions, sum and derived columns. Next study grouping, aggregation, financial precision and validation as needed.

The original client's samples are unavailable. Keep the source brief separate from simulated decisions; record assumptions and unresolved requirements in the architecture note. Do not claim client approval, Windows testing or original-data benchmarks without evidence.
