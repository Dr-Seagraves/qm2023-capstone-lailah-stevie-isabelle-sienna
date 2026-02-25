"""Fetch + clean REIT primary dataset.

This script reads the monthly REIT panel, writes a standardized raw extract,
and produces a long-format entity-year cleaned dataset for panel merging.
"""

from __future__ import annotations

import csv
from collections import defaultdict

from config_paths import PROCESSED_DATA_DIR, RAW_DATA_DIR

# ==============================================================================
# CONFIGURATION
# ==============================================================================

SOURCE_FILE = RAW_DATA_DIR / "REIT_sample_2000_2024_All_Variables.csv"
RAW_OUTPUT_FILE = RAW_DATA_DIR / "reit_raw.csv"
CLEAN_OUTPUT_FILE = PROCESSED_DATA_DIR / "reit_clean.csv"

RAW_FIELDS = [
    "permno",
    "ticker",
    "comnam",
    "rtype",
    "ptype",
    "psub",
    "date",
    "usdret",
    "usdprc",
    "market_equity",
    "assets",
    "sales",
    "net_income",
    "book_equity",
    "debt_at",
    "cash_at",
    "ocf_at",
    "roe",
    "btm",
    "beta",
]

NUMERIC_INPUT_COLUMNS = [
    "usdret",
    "usdprc",
    "market_equity",
    "assets",
    "sales",
    "net_income",
    "book_equity",
    "debt_at",
    "cash_at",
    "ocf_at",
    "roe",
    "btm",
    "beta",
]

NUMERIC_OUTPUT_MAP = {
    "usdret": "reit_avg_usdret",
    "usdprc": "reit_avg_usdprc",
    "market_equity": "reit_avg_market_equity",
    "assets": "reit_avg_assets",
    "sales": "reit_avg_sales",
    "net_income": "reit_avg_net_income",
    "book_equity": "reit_avg_book_equity",
    "debt_at": "reit_avg_debt_at",
    "cash_at": "reit_avg_cash_at",
    "ocf_at": "reit_avg_ocf_at",
    "roe": "reit_avg_roe",
    "btm": "reit_avg_btm",
    "beta": "reit_avg_beta",
}


# ==============================================================================
# HELPERS
# ==============================================================================


def to_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if text == "":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def to_year(date_text: str | None) -> int | None:
    if date_text is None:
        return None
    text = date_text.strip()
    if len(text) < 4:
        return None
    try:
        return int(text[:4])
    except ValueError:
        return None


def mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def first_non_empty(existing: str, candidate: str | None) -> str:
    if existing.strip() != "":
        return existing
    if candidate is None:
        return ""
    return candidate.strip()


def numeric_summary(rows: list[dict[str, str]], columns: list[str]) -> None:
    print("\nSummary statistics (cleaned):")
    for column in columns:
        values = [to_float(row.get(column)) for row in rows]
        valid = [value for value in values if value is not None]
        if not valid:
            print(f"- {column}: no valid numeric values")
            continue
        print(
            f"- {column}: n={len(valid)}, mean={mean(valid):.4f}, "
            f"min={min(valid):.4f}, max={max(valid):.4f}"
        )


# ==============================================================================
# MAIN PIPELINE
# ==============================================================================


def main() -> None:
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"REIT source file not found: {SOURCE_FILE}")

    entity_year = defaultdict(
        lambda: {
            "ticker": "",
            "comnam": "",
            "rtype": "",
            "ptype": "",
            "psub": "",
            "obs": 0,
            **{column: [] for column in NUMERIC_INPUT_COLUMNS},
        }
    )

    before_rows = 0
    dropped_missing_key = 0

    with SOURCE_FILE.open("r", newline="", encoding="utf-8") as source, RAW_OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as raw_out:
        reader = csv.DictReader(source)
        raw_writer = csv.DictWriter(raw_out, fieldnames=RAW_FIELDS)
        raw_writer.writeheader()

        for row in reader:
            before_rows += 1
            raw_writer.writerow({field: row.get(field, "") for field in RAW_FIELDS})

            unit_id = (row.get("permno") or "").strip()
            year = to_year(row.get("date"))
            if unit_id == "" or year is None:
                dropped_missing_key += 1
                continue

            bucket = entity_year[(unit_id, year)]
            bucket["ticker"] = first_non_empty(bucket["ticker"], row.get("ticker"))
            bucket["comnam"] = first_non_empty(bucket["comnam"], row.get("comnam"))
            bucket["rtype"] = first_non_empty(bucket["rtype"], row.get("rtype"))
            bucket["ptype"] = first_non_empty(bucket["ptype"], row.get("ptype"))
            bucket["psub"] = first_non_empty(bucket["psub"], row.get("psub"))
            bucket["obs"] += 1

            for column in NUMERIC_INPUT_COLUMNS:
                numeric_value = to_float(row.get(column))
                if numeric_value is not None:
                    bucket[column].append(numeric_value)

    cleaned_rows: list[dict[str, str]] = []
    for (unit_id, year) in sorted(entity_year.keys(), key=lambda x: (x[0], x[1])):
        bucket = entity_year[(unit_id, year)]
        out_row: dict[str, str] = {
            "unit_id": unit_id,
            "year": str(year),
            "ticker": bucket["ticker"],
            "comnam": bucket["comnam"],
            "rtype": bucket["rtype"],
            "ptype": bucket["ptype"],
            "psub": bucket["psub"],
            "reit_obs_months": str(bucket["obs"]),
        }
        for source_col, out_col in NUMERIC_OUTPUT_MAP.items():
            avg_value = mean(bucket[source_col])
            out_row[out_col] = "" if avg_value is None else f"{avg_value:.6f}"
        cleaned_rows.append(out_row)

    with CLEAN_OUTPUT_FILE.open("w", newline="", encoding="utf-8") as clean_out:
        fieldnames = [
            "unit_id",
            "year",
            "ticker",
            "comnam",
            "rtype",
            "ptype",
            "psub",
            "reit_obs_months",
            *NUMERIC_OUTPUT_MAP.values(),
        ]
        writer = csv.DictWriter(clean_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print("REIT fetch/clean complete")
    print(f"- Raw input rows (before cleaning): {before_rows:,}")
    print(f"- Dropped rows (missing key fields): {dropped_missing_key:,}")
    print(f"- Clean output rows (after cleaning): {len(cleaned_rows):,}")
    print(f"- Wrote raw extract: {RAW_OUTPUT_FILE}")
    print(f"- Wrote cleaned data: {CLEAN_OUTPUT_FILE}")
    numeric_summary(cleaned_rows, ["reit_obs_months", *NUMERIC_OUTPUT_MAP.values()])


if __name__ == "__main__":
    main()
