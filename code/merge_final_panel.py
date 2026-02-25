"""Merge processed datasets into a final long-format analysis panel.

Required inputs in data/processed:
- reit_clean.csv (entity-year base panel)
- fred_clean.csv (year-level supplementary controls)

Output in data/final:
- reit_fred_analysis_panel.csv
"""

from __future__ import annotations

import csv
from pathlib import Path

from config_paths import FINAL_DATA_DIR, PROCESSED_DATA_DIR

# ==============================================================================
# CONFIGURATION
# ==============================================================================

KEY_COLUMNS = ["unit_id", "year"]
REQUIRED_FILES = ["reit_clean.csv", "fred_clean.csv"]
OUTPUT_FILE = FINAL_DATA_DIR / "reit_fred_analysis_panel.csv"


# ==============================================================================
# HELPERS
# ==============================================================================


def read_csv_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"No header found in {path}")
        rows = list(reader)
        return rows, reader.fieldnames


def standardize_entity_year_keys(rows: list[dict[str, str]], source_name: str) -> list[dict[str, str]]:
    cleaned: list[dict[str, str]] = []
    dropped = 0
    seen_keys: set[tuple[str, str]] = set()

    for row in rows:
        unit_id = (row.get("unit_id") or "").strip()
        year_raw = (row.get("year") or "").strip()
        if unit_id == "" or year_raw == "":
            dropped += 1
            continue

        try:
            year = str(int(float(year_raw)))
        except ValueError:
            dropped += 1
            continue

        key = (unit_id, year)
        if key in seen_keys:
            dropped += 1
            continue

        seen_keys.add(key)
        out_row = {k: v for k, v in row.items()}
        out_row["unit_id"] = unit_id
        out_row["year"] = year
        cleaned.append(out_row)

    print(f"- {source_name}: before={len(rows):,}, after={len(cleaned):,}, dropped={dropped:,}")
    return cleaned


def standardize_year_keys(rows: list[dict[str, str]], source_name: str) -> list[dict[str, str]]:
    cleaned: list[dict[str, str]] = []
    dropped = 0
    seen_years: set[str] = set()

    for row in rows:
        year_raw = (row.get("year") or "").strip()
        if year_raw == "":
            dropped += 1
            continue

        try:
            year = str(int(float(year_raw)))
        except ValueError:
            dropped += 1
            continue

        if year in seen_years:
            dropped += 1
            continue

        seen_years.add(year)
        out_row = {k: v for k, v in row.items()}
        out_row["year"] = year
        cleaned.append(out_row)

    print(f"- {source_name}: before={len(rows):,}, after={len(cleaned):,}, dropped={dropped:,}")
    return cleaned


def rows_to_index(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    indexed: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = (row["unit_id"], row["year"])
        indexed[key] = row
    return indexed


def merge_left_on_entity_year(
    left_rows: list[dict[str, str]],
    right_rows: list[dict[str, str]],
    right_name: str,
) -> list[dict[str, str]]:
    right_index = rows_to_index(right_rows)
    right_columns = [col for col in right_rows[0].keys() if col not in KEY_COLUMNS] if right_rows else []

    before = len(left_rows)
    matched = 0
    merged: list[dict[str, str]] = []

    for left in left_rows:
        key = (left["unit_id"], left["year"])
        out = dict(left)
        right = right_index.get(key)

        if right is not None:
            matched += 1
            for column in right_columns:
                out[column] = right.get(column, "")
        else:
            for column in right_columns:
                out[column] = ""

        merged.append(out)

    print(f"- Merge with {right_name} on unit_id+year: before={before:,}, after={len(merged):,}, matched_keys={matched:,}")
    return merged


def merge_inner_on_year(
    left_rows: list[dict[str, str]],
    right_rows: list[dict[str, str]],
    right_name: str,
) -> list[dict[str, str]]:
    right_index = {row["year"]: row for row in right_rows}
    right_columns = [col for col in right_rows[0].keys() if col != "year"] if right_rows else []

    before = len(left_rows)
    matched = 0
    merged: list[dict[str, str]] = []
    dropped_unmatched = 0

    for left in left_rows:
        out = dict(left)
        right = right_index.get(left["year"])
        if right is None:
            dropped_unmatched += 1
            continue

        matched += 1
        for column in right_columns:
            out[column] = right.get(column, "")
        merged.append(out)

    print(
        f"- Merge with {right_name} on year (inner): before={before:,}, after={len(merged):,}, "
        f"matched_rows={matched:,}, dropped_unmatched={dropped_unmatched:,}"
    )
    return merged


def is_number(value: str | None) -> bool:
    if value is None:
        return False
    text = value.strip()
    if text == "":
        return False
    try:
        float(text)
        return True
    except ValueError:
        return False


def print_summary_stats(rows: list[dict[str, str]]) -> None:
    if not rows:
        print("No rows available for summary statistics.")
        return

    print("\nSummary statistics (final panel):")
    columns = list(rows[0].keys())
    numeric_columns = [
        column
        for column in columns
        if column not in KEY_COLUMNS and any(is_number(row.get(column)) for row in rows)
    ]

    for column in numeric_columns:
        values = [float(row[column]) for row in rows if is_number(row.get(column))]
        if not values:
            continue
        mean = sum(values) / len(values)
        print(f"- {column}: n={len(values)}, mean={mean:.4f}, min={min(values):.4f}, max={max(values):.4f}")


def write_output(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("Cannot write output: merged panel has zero rows.")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def assert_no_missing_keys(rows: list[dict[str, str]]) -> None:
    missing = 0
    for row in rows:
        if (row.get("unit_id") or "").strip() == "" or (row.get("year") or "").strip() == "":
            missing += 1
    if missing > 0:
        raise ValueError(f"Final panel has {missing:,} rows with missing unit_id/year keys")


# ==============================================================================
# MAIN PIPELINE
# ==============================================================================


def main() -> None:
    print("Merge pipeline started")
    print("Cleaning and validating processed inputs:")

    reit_path = PROCESSED_DATA_DIR / "reit_clean.csv"
    fred_path = PROCESSED_DATA_DIR / "fred_clean.csv"
    if not reit_path.exists():
        raise FileNotFoundError(f"Required processed file missing: {reit_path}")
    if not fred_path.exists():
        raise FileNotFoundError(f"Required processed file missing: {fred_path}")

    reit_rows_raw, reit_columns = read_csv_rows(reit_path)
    for required_key in KEY_COLUMNS:
        if required_key not in reit_columns:
            raise ValueError(f"reit_clean.csv missing required key: {required_key}")
    reit_rows = standardize_entity_year_keys(reit_rows_raw, "reit_clean.csv")

    fred_rows_raw, fred_columns = read_csv_rows(fred_path)
    if "year" not in fred_columns:
        raise ValueError("fred_clean.csv missing required key: year")
    fred_rows = standardize_year_keys(fred_rows_raw, "fred_clean.csv")

    merged_rows = merge_inner_on_year(reit_rows, fred_rows, "fred_clean.csv")

    optional_files = sorted(PROCESSED_DATA_DIR.glob("*_clean.csv"))
    for optional_path in optional_files:
        optional_name = optional_path.name
        if optional_name in REQUIRED_FILES:
            continue

        optional_rows, optional_columns = read_csv_rows(optional_path)
        if len(optional_rows) == 0:
            print(f"- Skipping {optional_name}: file has zero rows")
            continue
        if all(key in optional_columns for key in KEY_COLUMNS):
            cleaned_optional = standardize_entity_year_keys(optional_rows, optional_name)
            merged_rows = merge_left_on_entity_year(merged_rows, cleaned_optional, optional_name)
        elif "year" in optional_columns:
            cleaned_optional = standardize_year_keys(optional_rows, optional_name)
            merged_rows = merge_inner_on_year(merged_rows, cleaned_optional, optional_name)
        else:
            print(f"- Skipping {optional_name}: missing join keys")

    merged_rows.sort(key=lambda row: (row["unit_id"], int(row["year"])))
    assert_no_missing_keys(merged_rows)
    write_output(OUTPUT_FILE, merged_rows)

    print("\nMerge complete")
    print(f"- Final rows: {len(merged_rows):,}")
    print(f"- Final columns: {len(merged_rows[0].keys()) if merged_rows else 0}")
    print(f"- Wrote final panel: {OUTPUT_FILE}")
    print_summary_stats(merged_rows)


if __name__ == "__main__":
    main()
