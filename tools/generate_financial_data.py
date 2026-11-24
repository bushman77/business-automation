"""Regenerate synthetic client fixtures for exercise 001 (no dependencies)."""

import csv
from pathlib import Path

OUTPUT = Path(__file__).resolve().parents[1] / "examples" / "financial"
BASIC = [["2026-01-01","Opening Contract",150000],["2026-01-02","Office Supplies",-4599],["2026-01-03","Internet Service",-8999],["2026-01-05","Software Development",75000],["2026-01-07","Groceries",-12550],["2026-01-10","Server Hosting",-2500],["2026-01-15","Consulting",50000],["2026-02-01","Software Development",180000],["2026-02-03","Internet Service",-8999],["2026-02-10","Server Hosting",-2500]]
EDGE = [["2026-01-01","Opening balance adjustment",10000],["2026-01-01","Offset adjustment",-10000],["2026-01-02","Zero amount",0],["2026-01-02","Repeated valid transaction",1],["2026-01-02","Repeated valid transaction",1],["2026-01-03","Two-cent expense",-2],["2026-03-01","Small income",1],["2026-03-02","Small expense",-1],["2026-03-03","Refund",-50000],["2026-03-04","Travel, Parking and Tolls",-1234],["2026-03-05","Equipment \"Repair\"",-2500],["2026-04-01","=1+1",0],["2026-04-02","+example",0],["2026-04-03","-example",0],["2026-04-04","@example",0],["2026-04-05","Café supplies",-1250],["2026-04-06","Reimbursement",1250],["2026-06-01","Large customer payment",99999999],["2026-06-02","Large expense",-99999998],["2026-06-03","Rounding example",1],["2026-06-04","Rounding example",2],["2026-07-01","Zero-only period",0],["2026-07-02","Another zero",0],["2026-12-31","Year end receipt",20000],["2026-12-31","Year end payment",-1000]]
RULES = [["Customer Payment",1,15000,450000],["Consulting Revenue",1,50000,300000],["Software Development",1,100000,700000],["Subscription Revenue",1,1500,25000],["Employee Payroll",-1,125000,350000],["Office Rent",-1,150000,300000],["Software Subscription",-1,999,29999],["Server Hosting",-1,2500,15000],["Office Supplies",-1,500,35000],["Equipment Purchase",-1,20000,250000],["Advertising",-1,10000,100000],["Utility Payment",-1,5000,30000],["Customer Refund",-1,1000,100000],["Travel, Parking and Tolls",-1,500,25000],["Equipment \"Repair\"",-1,2500,50000],["Bank Fee",-1,100,3500]]
BUDGETS = [150000,170000,0,210000,180000,240000,160000,200000,220000,190000,230000,250000]
INVALID = [["2026-02-30","Impossible date","12.00"],["","Missing date","12.00"],["24/11/2026","Non-ISO date","12.00"],["2026-02-01","","12.00"],["2026-02-01","Whitespace description",""],["2026-02-01","Not numeric","abc"],["2026-02-01","Nonfinite amount","NaN"],["2026-02-01","Nonfinite infinity","Infinity"],["2026-02-01","Too many decimal places","1.001"],["2026-02-01","Extra field","10.00","unexpected"]]


def generate(count: int) -> list:
    state = 20261124 + count

    def rand(limit: int) -> int:
        nonlocal state
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        return state % limit

    rows = []
    for i in range(count):
        month = i * 12 // count + 1
        day = rand(28) + 1
        description, sign, lo, hi = RULES[rand(len(RULES))]
        amount = sign * (lo + rand(hi - lo + 1))
        rows.append([f"2026-{month:02d}-{day:02d}", description, amount])
    return sorted(rows, key=lambda row: row[0])


def money(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    whole, remainder = divmod(abs(cents), 100)
    return f"{sign}{whole}.{remainder:02d}"


def write(name: str, rows: list, delimiter: str = ",") -> None:
    with (OUTPUT / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter=delimiter, lineterminator="\n")
        writer.writerows(rows)


def transaction_rows(rows: list) -> list:
    return [[date, description, money(amount)] for date, description, amount in rows]


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    small = generate(100)
    datasets = {
        "transactions_basic.csv": BASIC,
        "transactions_small.csv": small,
        "transactions_medium.csv": generate(1000),
        "transactions_large.csv": generate(10000),
        "transactions_edge_cases.csv": EDGE,
        "transactions.tsv": small,
    }
    header = ["date", "description", "amount"]
    for name, records in datasets.items():
        delimiter = "\t" if name.endswith(".tsv") else ","
        write(name, [header, *transaction_rows(records)], delimiter)
    write(
        "transactions_invalid.csv",
        [header, *transaction_rows(small[:40]), *INVALID],
    )
    write(
        "budget.csv",
        [["month", "budget_net"], *[
            [f"2026-{i:02d}", money(amount)]
            for i, amount in enumerate(BUDGETS, start=1)
        ]],
    )


if __name__ == "__main__":
    main()
