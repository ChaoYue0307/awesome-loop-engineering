#!/usr/bin/env python3
"""Build the native Parquet shard published by the Hugging Face mirror."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "resources.jsonl"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="source JSON Lines export")
    parser.add_argument("--output", type=Path, required=True, help="destination Parquet shard")
    args = parser.parse_args()

    try:
        import pyarrow.json as arrow_json
        import pyarrow.parquet as parquet
    except ModuleNotFoundError:
        print("pyarrow is required: python3 -m pip install pyarrow", file=sys.stderr)
        return 1

    expected_rows = sum(1 for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip())
    table = arrow_json.read_json(args.input)
    if table.num_rows != expected_rows:
        print(f"expected {expected_rows} rows, parsed {table.num_rows}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    parquet.write_table(
        table,
        args.output,
        compression="zstd",
        use_dictionary=True,
        write_statistics=True,
    )

    metadata = parquet.read_metadata(args.output)
    if metadata.num_rows != expected_rows or metadata.num_columns != len(table.column_names):
        print("written Parquet metadata does not match the source table", file=sys.stderr)
        return 1

    summary = {
        "columns": metadata.num_columns,
        "output": str(args.output),
        "rows": metadata.num_rows,
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
