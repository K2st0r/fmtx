#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fmtx — Universal Data Format Converter
========================================
JSON / CSV / YAML / TOML — convert between any two, in one command.

Usage:
  fmtx input.json -o output.yaml          # JSON → YAML
  cat file.json | fmtx -f json -t yaml    # stdin → stdout
  fmtx data.csv -t json -o out.json       # CSV → JSON
  fmtx config.yaml -t toml                # YAML → TOML (print to stdout)

Install:
  pip install pyyaml tomli-w

License: MIT
Donate:  0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697 (USDT ERC20)
"""
import argparse, csv, json, io, sys, os
from typing import Any, Dict, List

__version__ = "1.0.0"
__wallet__  = "0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697"

try:
    import yaml
except ImportError:
    yaml = None
try:
    import tomli_w
except ImportError:
    tomli_w = None

SUPPORTED = ["json", "csv", "yaml", "toml"]
EXT_MAP = {
    ".json": "json", ".csv": "csv", ".tsv": "csv",
    ".yaml": "yaml", ".yml": "yaml", ".toml": "toml"
}

# ── Readers ──────────────────────────────────

def read_json(text: str) -> Any:
    return json.loads(text)

def read_csv(text: str, delimiter: str = ",") -> List[Dict]:
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    return [row for row in reader]

def read_yaml(text: str) -> Any:
    if yaml is None:
        sys.exit("yaml support requires: pip install pyyaml")
    return yaml.safe_load(text)

def read_toml(text: str) -> Any:
    return read_json(text)  # TOML is a JSON superset for reading

# ── Writers ──────────────────────────────────

def write_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)

def write_csv(data: List[Dict]) -> str:
    if not data:
        return ""
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return out.getvalue()

def write_yaml(data: Any) -> str:
    if yaml is None:
        sys.exit("yaml support requires: pip install pyyaml")
    return yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)

def write_toml(data: Any) -> str:
    if tomli_w is None:
        sys.exit("toml support requires: pip install tomli-w")
    if not isinstance(data, dict):
        data = {"data": data}
    return tomli_w.dumps(data)

# ── Core ─────────────────────────────────────

READERS = {"json": read_json, "csv": read_csv, "yaml": read_yaml, "toml": read_toml}
WRITERS = {"json": write_json, "csv": write_csv, "yaml": write_yaml, "toml": write_toml}

def convert(input_text: str, from_fmt: str, to_fmt: str) -> str:
    if from_fmt not in READERS:
        sys.exit(f"Unsupported input format: {from_fmt}")
    if to_fmt not in WRITERS:
        sys.exit(f"Unsupported output format: {to_fmt}")
    
    data = READERS[from_fmt](input_text)
    
    # If converting to CSV but data is not a list, wrap it
    if to_fmt == "csv" and not isinstance(data, list):
        data = [data] if isinstance(data, dict) else []
    # If converting from CSV but output needs to be list wrapping
    if from_fmt == "csv" and to_fmt in ("json", "yaml", "toml"):
        pass  # CSV already returns list
    
    return WRITERS[to_fmt](data)

def detect_format(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    return EXT_MAP.get(ext, "json")

# ── CLI ──────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="fmtx",
        description="Universal data format converter — JSON/CSV/YAML/TOML",
        epilog=f"Examples:\n  fmtx data.json -o data.yaml\n  cat data.csv | fmtx -f csv -t json\n  fmtx config.toml -t yaml",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", nargs="?", help="Input file path (or stdin if omitted)")
    parser.add_argument("-o", "--output", help="Output file path (stdout if omitted)")
    parser.add_argument("-f", "--from", dest="from_fmt", choices=SUPPORTED, help="Input format (auto-detect from extension if omitted)")
    parser.add_argument("-t", "--to", dest="to_fmt", choices=SUPPORTED, default="json", help="Output format (default: json)")
    parser.add_argument("--version", action="version", version=f"fmtx {__version__}")
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        with open(args.input, "r", encoding="utf-8-sig") as f:
            text = f.read()
        if not args.from_fmt:
            args.from_fmt = detect_format(args.input)
    else:
        text = sys.stdin.buffer.read().decode("utf-8")
        if not args.from_fmt:
            sys.exit("Reading from stdin: please specify -f/--from format")
    
    if not args.from_fmt:
        args.from_fmt = "json"
    
    # Convert
    result = convert(text, args.from_fmt, args.to_fmt)
    
    # Write output
    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="") as f:
            f.write(result)
        print(f"Converted {args.input or 'stdin'} -> {args.output} ({args.from_fmt} -> {args.to_fmt})", file=sys.stderr)
    else:
        if sys.stdout.encoding and sys.stdout.encoding.lower() in ('gbk','cp936','cp1252'):
            sys.stdout.reconfigure(encoding='utf-8')
        sys.stdout.write(result)

if __name__ == "__main__":
    main()
