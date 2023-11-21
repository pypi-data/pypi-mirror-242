from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl

from dataframe_api_compat.polars_standard.dataframe_object import DataFrame

if TYPE_CHECKING:
    from collections.abc import Sequence

    from dataframe_api import GroupBy as GroupByT
    from dataframe_api.groupby_object import Aggregation as AggregationT
    from dataframe_api.typing import NullType
    from dataframe_api.typing import Scalar
else:
    GroupByT = object


class GroupBy(GroupByT):
    def __init__(self, df: pl.LazyFrame, keys: Sequence[str], api_version: str) -> None:
        for key in keys:
            if key not in df.columns:
                msg = f"key {key} not present in DataFrame's columns"
                raise KeyError(msg)
        self.df = df
        self.keys = keys
        self._api_version = api_version
        self.group_by = (
            self.df.group_by if pl.__version__ < "0.19.0" else self.df.group_by
        )

    def size(self) -> DataFrame:
        result = self.group_by(self.keys).count().rename({"count": "size"})
        return DataFrame(result, api_version=self._api_version)

    def any(self, *, skip_nulls: bool | Scalar = True) -> DataFrame:
        grp = self.group_by(self.keys)
        if not all(
            self.df.schema[col] is pl.Boolean
            for col in self.df.columns
            if col not in self.keys
        ):
            msg = "Expected all boolean columns"
            raise TypeError(msg)
        result = grp.agg(pl.col("*").any())
        return DataFrame(result, api_version=self._api_version)

    def all(self, *, skip_nulls: bool | Scalar = True) -> DataFrame:
        grp = self.group_by(self.keys)
        if not all(
            self.df.schema[col] is pl.Boolean
            for col in self.df.columns
            if col not in self.keys
        ):
            msg = "Expected all boolean columns"
            raise TypeError(msg)
        result = grp.agg(pl.col("*").all())
        return DataFrame(result, api_version=self._api_version)

    def min(self, *, skip_nulls: bool | Scalar = True) -> DataFrame:
        result = self.group_by(self.keys).agg(pl.col("*").min())
        return DataFrame(result, api_version=self._api_version)

    def max(self, *, skip_nulls: bool | Scalar = True) -> DataFrame:
        result = self.group_by(self.keys).agg(pl.col("*").max())
        return DataFrame(result, api_version=self._api_version)

    def sum(self, *, skip_nulls: bool | Scalar = True) -> DataFrame:
        result = self.group_by(self.keys).agg(pl.col("*").sum())
        return DataFrame(result, api_version=self._api_version)

    def prod(self, *, skip_nulls: bool | Scalar = True) -> DataFrame:
        result = self.group_by(self.keys).agg(pl.col("*").product())
        return DataFrame(result, api_version=self._api_version)

    def median(self, *, skip_nulls: bool | Scalar = True) -> DataFrame:
        result = self.group_by(self.keys).agg(pl.col("*").median())
        return DataFrame(result, api_version=self._api_version)

    def mean(self, *, skip_nulls: bool | Scalar = True) -> DataFrame:
        result = self.group_by(self.keys).agg(pl.col("*").mean())
        return DataFrame(result, api_version=self._api_version)

    def std(
        self,
        *,
        correction: float | Scalar | NullType = 1.0,
        skip_nulls: bool | Scalar = True,
    ) -> DataFrame:
        result = self.group_by(self.keys).agg(pl.col("*").std())
        return DataFrame(result, api_version=self._api_version)

    def var(
        self,
        *,
        correction: float | Scalar | NullType = 1.0,
        skip_nulls: bool | Scalar = True,
    ) -> DataFrame:
        result = self.group_by(self.keys).agg(pl.col("*").var())
        return DataFrame(result, api_version=self._api_version)

    def aggregate(
        self,
        *aggregations: AggregationT,
    ) -> DataFrame:
        aggregations = validate_aggregations(*aggregations, keys=self.keys)
        return DataFrame(
            self.group_by(self.keys).agg(
                *[resolve_aggregation(aggregation) for aggregation in aggregations],
            ),
            api_version=self._api_version,
            is_persisted=False,
        )


def validate_aggregations(
    *aggregations: AggregationT,
    keys: Sequence[str],
) -> tuple[AggregationT, ...]:
    return tuple(
        aggregation
        if aggregation.column_name != "__placeholder__"  # type: ignore[attr-defined]
        else aggregation.replace(column_name=keys[0])  # type: ignore[attr-defined]
        for aggregation in aggregations
    )


def resolve_aggregation(aggregation: AggregationT) -> pl.Expr:
    return getattr(  # type: ignore[no-any-return]
        pl.col(aggregation.column_name),  # type: ignore[attr-defined]
        aggregation.aggregation,  # type: ignore[attr-defined]
    )().alias(
        aggregation.output_name,  # type: ignore[attr-defined]
    )
