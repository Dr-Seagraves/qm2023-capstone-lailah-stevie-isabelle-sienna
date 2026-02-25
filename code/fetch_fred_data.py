"""Fetch + clean FRED supplementary dataset.

This script reads weekly 15-year mortgage rates, writes a standardized raw
extract, and produces annual supplementary variables for panel merging.
"""

from __future__ import annotations

import csv
from collections import defaultdict

from config_paths import PROCESSED_DATA_DIR, RAW_DATA_DIR

# ==============================================================================
# CONFIGURATION
# ==============================================================================

SOURCE_FILE = RAW_DATA_DIR / "MORTGAGE15US.csv"
RAW_OUTPUT_FILE = RAW_DATA_DIR / "fred_raw.csv"
CLEAN_OUTPUT_FILE = PROCESSED_DATA_DIR / "fred_clean.csv"


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


def std_dev(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    avg = mean(values)
    if avg is None:
        return None
    variance = sum((value - avg) ** 2 for value in values) / (len(values) - 1)
    return variance**0.5


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
        raise FileNotFoundError(f"FRED source file not found: {SOURCE_FILE}")

    annual_rates = defaultdict(list)

    before_rows = 0
    dropped_missing = 0

    with SOURCE_FILE.open("r", newline="", encoding="utf-8") as source, RAW_OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as raw_out:
        reader = csv.DictReader(source)
        raw_writer = csv.DictWriter(raw_out, fieldnames=["observation_date", "MORTGAGE15US"])
        raw_writer.writeheader()

        for row in reader:
            before_rows += 1
            observation_date = row.get("observation_date", "")
            rate = row.get("MORTGAGE15US", "")

            raw_writer.writerow(
                {
                    "observation_date": observation_date,
                    "MORTGAGE15US": rate,
                }
            )

            year = to_year(observation_date)
            rate_num = to_float(rate)
            if year is None or rate_num is None:
                dropped_missing += 1
                continue

            annual_rates[year].append(rate_num)

    cleaned_rows: list[dict[str, str]] = []
    for year in sorted(annual_rates.keys()):
        values = annual_rates[year]
        yearly_mean = mean(annual_rates[year])
        yearly_std = std_dev(values)
        cleaned_rows.append(
            {
                "year": str(year),
                "fred_obs_weeks": str(len(values)),
                "fred_avg_mortgage15us": "" if yearly_mean is None else f"{yearly_mean:.6f}",
                "fred_min_mortgage15us": f"{min(values):.6f}",
                "fred_max_mortgage15us": f"{max(values):.6f}",
                "fred_std_mortgage15us": "" if yearly_std is None else f"{yearly_std:.6f}",
            }
        )

    with CLEAN_OUTPUT_FILE.open("w", newline="", encoding="utf-8") as clean_out:
        writer = csv.DictWriter(
            clean_out,
            fieldnames=[
                "year",
                "fred_obs_weeks",
                "fred_avg_mortgage15us",
                "fred_min_mortgage15us",
                "fred_max_mortgage15us",
                "fred_std_mortgage15us",
            ],
        )
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print("FRED fetch/clean complete")
    print(f"- Raw input rows (before cleaning): {before_rows:,}")
    print(f"- Dropped rows (invalid/missing date or rate): {dropped_missing:,}")
    print(f"- Clean output rows (after cleaning): {len(cleaned_rows):,}")
    print(f"- Wrote raw extract: {RAW_OUTPUT_FILE}")
    print(f"- Wrote cleaned data: {CLEAN_OUTPUT_FILE}")
    numeric_summary(
        cleaned_rows,
        [
            "fred_obs_weeks",
            "fred_avg_mortgage15us",
            "fred_min_mortgage15us",
            "fred_max_mortgage15us",
            "fred_std_mortgage15us",
        ],
    )


if __name__ == "__main__":
    main()
