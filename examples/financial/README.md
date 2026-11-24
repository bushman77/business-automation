# Synthetic client data — Exercise 001

These fictional records are training inputs for [Exercise 001](../../docs/exercises/001-financial-reporting.md), not original client data. All amounts use one assumed currency (CAD), two decimal places, and the calendar year 2026. Generated business activity is illustrative, not a real company's accounting history.

| File | Records (excluding header) | Purpose |
| --- | ---: | --- |
| transactions_basic.csv | 10 | Same hand-checkable records as the initial REPL lesson |
| transactions_small.csv | 100 | Normal reporting |
| transactions_medium.csv | 1,000 | Larger input |
| transactions_large.csv | 10,000 | Performance fixture |
| transactions_invalid.csv | 50 | 40 valid records followed by 10 deliberately invalid records; reject file |
| transactions_edge_cases.csv | 25 | Zero, gaps, exact cents, duplicates, negative net, large values, Unicode, quoting, formula-like text |
| transactions.tsv | 100 | Same records as small CSV, tab-separated |
| budget.csv | 12 | Monthly signed budget net, including zero for March |
| expected_totals.csv | 6 | Exact reference totals by valid dataset |
| expected_monthly.csv | 62 | Exact reference totals by month including intervening empty months |

## Schema

Transaction fields: `date` (ISO YYYY-MM-DD), `description` (nonempty text), `amount` (signed decimal string with two digits after decimal in valid fixtures). Positive = income, negative = expense, zero = neutral. Duplicate rows in the edge dataset are intentional valid transactions. CSV/TSV use UTF-8 with standard quoting; a comma or double quote inside descriptions is valid. Formula-like descriptions must be written as literal text to Excel. Budget fields are `month` (YYYY-MM) and `budget_net` (signed decimal). Missing budget can be tested by omitting the budget input or using a subset of the budget rows.

Invalid file data records 41–50 (physical lines 42–51): impossible date, missing date, non-ISO date, empty description, missing amount, nonnumeric amount, NaN, infinity, excess decimal precision, extra field. The complete file should fail validation; exercise each failure independently by isolating a row with the header. The invalid file does not have financial reference totals.

## Reproduce inputs

From the repository root:

```sh
uv run python tools/generate_financial_data.py
```

The generator uses only Python's standard library, an explicitly seeded 32-bit deterministic pseudorandom sequence, fixed business descriptions and integer cents. No Faker dependency is needed. It regenerates the eight input fixtures, not the independently computed expected files, and does not touch your original local transactions.csv.

The expected files were calculated separately from the generated records using integer-cent aggregation. Compare your implementation against them rather than modifying the expected values to fit your output. Expenses are positive magnitudes, net = income - expenses, and the count includes zero-value transactions. Reference files cover totals and monthly sums/counts, not rounding of averages or variance calculations; the learner should construct additional independent tests for those. The performance and Windows compatibility requirements remain untested until the report application exists.
