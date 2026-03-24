from __future__ import annotations

import pandas as pd

from troel_ops_kit.kpis import (
    compute_avg_daily_demand,
    compute_coverage_days,
    compute_dormant_stock,
)


def test_compute_avg_daily_demand_keeps_sku_column() -> None:
    demand = pd.DataFrame(
        {
            "date": ["2026-02-20", "2026-02-22"],
            "sku": ["SKU-0001", "SKU-0001"],
            "demand_qty": [10.0, 20.0],
        }
    )

    out = compute_avg_daily_demand(demand, window_days=2)

    assert {"date", "sku", "avg_daily_demand"}.issubset(set(out.columns))
    assert (out["sku"] == "SKU-0001").all()


def test_compute_avg_daily_demand_empty_input() -> None:
    demand = pd.DataFrame(columns=["date", "sku", "demand_qty"])
    out = compute_avg_daily_demand(demand, window_days=28)
    assert list(out.columns) == ["date", "sku", "avg_daily_demand"]
    assert out.empty


def test_compute_avg_daily_demand_extends_until_requested_end_date() -> None:
    demand = pd.DataFrame(
        {
            "date": ["2026-02-20", "2026-02-22"],
            "sku": ["SKU-0001", "SKU-0001"],
            "demand_qty": [10.0, 20.0],
        }
    )

    out = compute_avg_daily_demand(demand, window_days=2, end_date=pd.Timestamp("2026-02-24").date())

    assert out["date"].max().isoformat() == "2026-02-24"
    assert out.iloc[-1]["avg_daily_demand"] == 0.0


def test_compute_avg_daily_demand_uses_full_calendar_window_for_recent_sku() -> None:
    demand = pd.DataFrame(
        {
            "date": ["2026-02-27"],
            "sku": ["SKU-0001"],
            "demand_qty": [10.0],
        }
    )

    out = compute_avg_daily_demand(demand, window_days=28, end_date=pd.Timestamp("2026-02-28").date())

    assert out.iloc[-1]["avg_daily_demand"] == 10.0 / 28.0


def test_compute_coverage_uses_last_available_avg_demand_before_snapshot() -> None:
    avg_demand = pd.DataFrame(
        {
            "date": ["2026-02-22"],
            "sku": ["SKU-0001"],
            "avg_daily_demand": [5.0],
        }
    )
    stock = pd.DataFrame(
        {
            "snapshot_date": ["2026-02-24"],
            "sku": ["SKU-0001"],
            "on_hand_qty": [20.0],
        }
    )

    out = compute_coverage_days(stock, avg_demand)

    assert out.iloc[0]["avg_daily_demand"] == 5.0
    assert out.iloc[0]["coverage_days"] == 4.0


def test_compute_dormant_stock_excludes_sales_outside_exact_lookback_window() -> None:
    sales = pd.DataFrame(
        {
            "date": ["2025-12-31"],
            "sku": ["SKU-0001"],
            "qty": [1.0],
        }
    )
    stock = pd.DataFrame(
        {
            "snapshot_date": ["2026-03-01"],
            "sku": ["SKU-0001"],
            "on_hand_qty": [5.0],
        }
    )

    out = compute_dormant_stock(sales, stock, lookback_days=60)

    assert len(out) == 1
    assert out.iloc[0]["sku"] == "SKU-0001"
