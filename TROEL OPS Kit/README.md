# TROEL OPS Kit

![CI](docs/assets/badge-ci.svg)
![Python](docs/assets/badge-python.svg)

Pragmatic Supply Chain toolkit for **ingest -> validate -> KPI -> alerts -> report** using only synthetic demo data.

## Why this project exists
`TROEL OPS Kit` is a portfolio-grade CLI that demonstrates how to operationalize supply/stock analytics without over-engineering.

- Explainable and auditable business rules
- Clean Python packaging + CLI + repo-level CI
- Windows-friendly commands (PowerShell compatible)
- No client data, only synthetic datasets

This project lives in the `TROEL OPS Kit/` folder of the portfolio repository.
The GitHub Actions workflow that validates it is defined at the repository root.

## Business utility (what this application is for)
`TROEL OPS Kit` helps operations teams turn raw ERP exports into daily action lists:
- Detect stockout risks before they happen
- Detect dormant inventory that ties up cash
- Prioritize SKUs by value impact (ABC)
- Keep data quality visible and auditable

In practice, the tool replaces manual spreadsheet checks with a reproducible CLI pipeline.

## What it calculates
From `sales + stock + catalog`, the pipeline computes:
- **Coverage days**: `on_hand_qty / avg_daily_demand` (risk of stockout)
- **Dormant stock**: `stock > 0` and `0 sales` over a lookback window (default 60 days)
- **ABC class**: consumption value ranking (`total_qty * unit_cost`) with cumulative buckets:
  - `A` up to 80%
  - `B` from 80% to 95%
  - `C` above 95%

It also computes validation issues and alert rules:
- `LOW_COVERAGE`
- `DEAD_SKU`
- `DATA_QUALITY`

## Exact commands (copy/paste)
Run from project folder:

```bash
cd "/home/christophetroel/Documents/Les projets/christophe-4/TROEL OPS Kit"
```

Create environment and install:

```bash
python3 -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -e ".[dev]"
```

Check CLI:

```bash
troel-ops --help
```

Generate synthetic demo data and run the full pipeline:

```bash
troel-ops demo generate --out ./data/demo
troel-ops run \
  --sales ./data/demo/sales.csv \
  --stock ./data/demo/stock.csv \
  --catalog ./data/demo/catalog.csv \
  --out ./out
```

Run with your own CSV files (`data/Mes fichiers`):

```bash
troel-ops run \
  --sales "./data/Mes fichiers/sales.csv" \
  --stock "./data/Mes fichiers/stock.csv" \
  --catalog "./data/Mes fichiers/catalog.csv" \
  --out ./out
```

Minimum required columns:
- `sales.csv`: `date`, `sku`, `qty`
- `stock.csv`: `snapshot_date`, `sku`, `on_hand_qty`
- `catalog.csv`: `sku`

Run with custom column mapping:

```bash
troel-ops run \
  --sales "./data/Mes fichiers/sales.csv" \
  --stock "./data/Mes fichiers/stock.csv" \
  --catalog "./data/Mes fichiers/catalog.csv" \
  --mapping ./mapping.example.json \
  --out ./out
```

## Expected outputs
After `troel-ops run`, the `./out` folder contains:
- `issues.csv`
- `kpi_coverage.csv`
- `kpi_dormant.csv`
- `kpi_abc.csv`
- `alerts.csv`
- `report.md`

## Screenshots (placeholders)
![CLI run placeholder](docs/assets/cli-screenshot-placeholder.svg)
![Report placeholder](docs/assets/report-screenshot-placeholder.svg)

## Architecture in 1 minute
```text
CSV/XLSX exports
    |
    v
[ingest + column mapping]
    |
    v
[validation contracts + cross checks]
    |
    v
[KPI engine: coverage / dormant / ABC]
    |
    v
[alert rules: explainable thresholds]
    |
    v
[report.md (+ optional PDF)]
```

## What this repo intentionally does NOT include
- Real client datasets or proprietary business rules
- Opaque AI scoring or black-box recommendations
- Heavy orchestration frameworks for a simple portfolio workflow

## CLI summary
- `troel-ops demo generate` -> creates synthetic datasets
- `troel-ops run` -> full pipeline and report generation
- `troel-ops report --format pdf` -> rendered PDF export (`pip install -e ".[pdf]"`)

## Roadmap
- Add optional DuckDB materialization for intermediate tables
- Add scenario simulation (`what-if` coverage thresholds)
- Publish sample GitHub release with frozen demo artifacts

## License
MIT - see [LICENSE](LICENSE)
