from __future__ import annotations

import sys

import pandas as pd
import polars as pl
import pytest
from polars.testing import assert_series_equal


@pytest.mark.skipif(
    sys.version_info < (3, 9) or sys.version_info >= (3, 12),
    reason="pandas doesn't support 3.8",
)
def test_scale_column_pandas() -> None:
    s = pd.Series([1, 2, 3], name="a")
    ser = s.__column_consortium_standard__()
    ser = ser - ser.mean()
    result = ser.column
    pd.testing.assert_series_equal(result, pd.Series([-1, 0, 1.0], name="a"))


def test_scale_column_polars() -> None:
    s = pl.Series("a", [1, 2, 3])
    ser = s.__column_consortium_standard__()
    ser = ser - ser.mean()
    result = pl.select(ser.column)["a"]
    assert_series_equal(result, pl.Series("a", [-1, 0, 1.0]))


def test_scale_column_polars_from_persisted_df() -> None:
    df = pl.DataFrame({"a": [1, 2, 3]})
    ser = df.__dataframe_consortium_standard__().col("a")
    ser = ser - ser.mean()
    result = pl.select(ser.persist().column)["a"]
    assert_series_equal(result, pl.Series("a", [-1, 0, 1.0]))
