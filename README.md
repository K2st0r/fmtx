<div align="center">

# fmtx

**Universal Data Format Converter — JSON ↔ CSV ↔ YAML ↔ TOML**

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-purple)](https://github.com/K2st0r/fmtx)
[![Donate](https://img.shields.io/badge/Donate-USDT-red)](#donate)

</div>

### 🎯 One command to convert anything

```bash
# JSON → YAML
fmtx data.json -o data.yaml

# CSV → JSON
fmtx users.csv -t json -o users.json

# YAML → TOML
fmtx config.yaml -t toml

# Pipe from stdin
cat data.json | fmtx -f json -t csv
```

### ✨ Supported Conversions

| From → To | JSON | CSV | YAML | TOML |
|-----------|------|-----|------|------|
| **JSON** | — | ✅ | ✅ | ✅ |
| **CSV** | ✅ | — | ✅ | ✅ |
| **YAML** | ✅ | ✅ | — | ✅ |
| **TOML** | ✅ | ✅ | ✅ | — |

### 🚀 Install

```bash
# Core (JSON/CSV): zero deps
python fmtx.py input.csv -t json

# Optional: YAML support
pip install pyyaml

# Optional: TOML support
pip install tomli-w
```

### 📖 Examples

```bash
# Auto-detect format from file extension
fmtx data.yaml -o data.json         # YAML → JSON

# Convert CSV to pretty YAML
fmtx spreadsheet.csv -t yaml

# Pipe: API response → CSV
curl https://api.example.com/data | fmtx -f json -t csv > out.csv

# Batch: convert all JSONs to YAML
for f in *.json; do fmtx "$f" -o "${f%.json}.yaml"; done
```

### 🌟 Why fmtx?

- **Zero config** — auto-detects format from extension
- **Pipe-friendly** — stdin/stdout, works in shell pipelines
- **Minimal deps** — JSON/CSV needs nothing; YAML/TOML optional
- **Fast** — sub-millisecond for typical files

## 💎 Donate

**USDT (ERC20):** `0xAfe9B67B1DF618FAeD32dC71E3458cf549f26697`

---

*MIT License · Made with ❤️ by [K2st0r](https://github.com/K2st0r)*
