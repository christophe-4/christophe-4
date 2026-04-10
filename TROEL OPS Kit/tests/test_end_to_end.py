import pathlib

import pandas as pd
import pytest

from troel_ops_kit.demo import generate_demo
from troel_ops_kit.pipeline import run


def test_end_to_end(tmp_path: pathlib.Path):
    data_dir = tmp_path / "data"
    out_dir = tmp_path / "out"
    generate_demo(data_dir, n_skus=50, days=90, seed=1)

    res = run(
        sales_path=str(data_dir / "sales.csv"),
        stock_path=str(data_dir / "stock.csv"),
        catalog_path=str(data_dir / "catalog.csv"),
        out_dir=str(out_dir),
    )

    assert (out_dir / "kpi_coverage.csv").exists()
    assert (out_dir / "alerts.csv").exists()
    assert (out_dir / "report.md").exists()
    assert len(res.coverage) > 0


def test_run_accepts_catalog_with_only_required_business_columns(tmp_path: pathlib.Path) -> None:
    data_dir = tmp_path / "data"
    out_dir = tmp_path / "out"
    data_dir.mkdir()

    pd.DataFrame({"date": ["2026-03-01"], "sku": ["SKU-1"], "qty": [3.0]}).to_csv(
        data_dir / "sales.csv", index=False
    )
    pd.DataFrame({"snapshot_date": ["2026-03-01"], "sku": ["SKU-1"], "on_hand_qty": [10.0]}).to_csv(
        data_dir / "stock.csv", index=False
    )
    pd.DataFrame({"sku": ["SKU-1"], "unit_cost": [2.0]}).to_csv(data_dir / "catalog.csv", index=False)

    res = run(
        sales_path=str(data_dir / "sales.csv"),
        stock_path=str(data_dir / "stock.csv"),
        catalog_path=str(data_dir / "catalog.csv"),
        out_dir=str(out_dir),
    )

    assert (out_dir / "kpi_abc.csv").exists()
    assert len(res.abc) == 1
    assert pd.isna(res.abc.iloc[0]["category"])
    assert pd.isna(res.abc.iloc[0]["supplier"])
    assert pd.isna(res.abc.iloc[0]["description"])


def test_run_accepts_catalog_optional_fields_with_nan_values(tmp_path: pathlib.Path) -> None:
    data_dir = tmp_path / "data"
    out_dir = tmp_path / "out"
    data_dir.mkdir()

    pd.DataFrame({"date": ["2026-03-01"], "sku": ["SKU-1"], "qty": [3.0]}).to_csv(
        data_dir / "sales.csv", index=False
    )
    pd.DataFrame({"snapshot_date": ["2026-03-01"], "sku": ["SKU-1"], "on_hand_qty": [10.0]}).to_csv(
        data_dir / "stock.csv", index=False
    )
    pd.DataFrame(
        {
            "sku": ["SKU-1"],
            "description": [float("nan")],
            "category": [float("nan")],
            "supplier": [float("nan")],
            "unit_cost": [float("nan")],
        }
    ).to_csv(data_dir / "catalog.csv", index=False)

    res = run(
        sales_path=str(data_dir / "sales.csv"),
        stock_path=str(data_dir / "stock.csv"),
        catalog_path=str(data_dir / "catalog.csv"),
        out_dir=str(out_dir),
    )

    assert (out_dir / "issues.csv").exists()
    assert len(res.issues[res.issues["level"] == "error"]) == 0
    assert (out_dir / "kpi_abc.csv").exists()


def test_run_stops_before_kpis_when_validation_has_errors(tmp_path: pathlib.Path) -> None:
    data_dir = tmp_path / "data"
    out_dir = tmp_path / "out"
    data_dir.mkdir()

    pd.DataFrame({"date": ["2026-03-01"], "sku": ["SKU-1"], "qty": [-5.0]}).to_csv(
        data_dir / "sales.csv", index=False
    )
    pd.DataFrame({"snapshot_date": ["2026-03-01"], "sku": ["SKU-1"], "on_hand_qty": [10.0]}).to_csv(
        data_dir / "stock.csv", index=False
    )
    pd.DataFrame(
        {
            "sku": ["SKU-1"],
            "description": ["Product"],
            "category": ["CAT"],
            "supplier": ["SUP"],
            "unit_cost": [2.0],
        }
    ).to_csv(data_dir / "catalog.csv", index=False)

    with pytest.raises(ValueError, match="Validation failed with 1 error"):
        run(
            sales_path=str(data_dir / "sales.csv"),
            stock_path=str(data_dir / "stock.csv"),
            catalog_path=str(data_dir / "catalog.csv"),
            out_dir=str(out_dir),
        )

    assert (out_dir / "issues.csv").exists()
    assert not (out_dir / "kpi_coverage.csv").exists()
    assert not (out_dir / "alerts.csv").exists()
