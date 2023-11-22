from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

import polars as pl

from dataframe_api_compat.polars_standard.column_object import Column
from dataframe_api_compat.polars_standard.dataframe_object import DataFrame

if TYPE_CHECKING:
    from dataframe_api.typing import DType
    from dataframe_api.typing import Scalar as ScalarT
else:
    ScalarT = object


class Scalar(ScalarT):
    def __init__(
        self,
        value: Any,
        api_version: str,
        df: DataFrame | None,
        *,
        is_persisted: bool = False,
    ) -> None:
        self._value = value
        self._api_version = api_version
        self._df = df
        self._is_persisted = is_persisted

    def _validate_other(self, other: Any) -> Any:
        if isinstance(other, (Column, DataFrame)):
            return NotImplemented
        if isinstance(other, Scalar):
            if id(self._df) != id(other._df):
                msg = "cannot compare columns/scalars from different dataframes"
                raise ValueError(
                    msg,
                )
            return other._value
        return other

    def _from_scalar(self, scalar: Scalar) -> Scalar:
        return Scalar(scalar, df=self._df, api_version=self._api_version)

    @property
    def dtype(self) -> DType:  # pragma: no cover  # todo
        return self._value.dtype  # type: ignore[no-any-return]

    @property
    def scalar(self) -> Any:  # pragma: no cover  # todo
        return self._value

    @property
    def parent_dataframe(self) -> Any:  # pragma: no cover  # todo
        return self._df

    def _materialise(self) -> Any:
        if not self._is_persisted:
            msg = "Can't call __bool__ on Scalar. Please use .persist() first."
            raise RuntimeError(msg)

        if self._df is None:
            value = pl.select(self._value).item()
        else:
            df = self._df.dataframe.collect().select(self._value)
            value = df.get_column(df.columns[0]).item()
        return value

    def persist(self) -> Scalar:
        if self._df is None:
            value = pl.select(self._value).item()
        else:
            df = self._df.dataframe.collect().select(self._value)
            value = df.get_column(df.columns[0]).item()
        return Scalar(
            value,
            df=self._df,
            api_version=self._api_version,
            is_persisted=True,
        )

    def __lt__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__lt__(other))

    def __le__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__le__(other))

    def __eq__(self, other: Any) -> Scalar:  # type: ignore[override]
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__eq__(other))

    def __ne__(self, other: Any) -> Scalar:  # type: ignore[override]
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__ne__(other))

    def __gt__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__gt__(other))

    def __ge__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__ge__(other))

    def __add__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__add__(other))

    def __radd__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__radd__(other))

    def __sub__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__sub__(other))

    def __rsub__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__rsub__(other))

    def __mul__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__mul__(other))

    def __rmul__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__rmul__(other))

    def __mod__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__mod__(other))

    def __rmod__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__rmod__(other))

    def __pow__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__pow__(other))

    def __rpow__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__rpow__(other))

    def __floordiv__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__floordiv__(other))

    def __rfloordiv__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__rfloordiv__(other))

    def __truediv__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__truediv__(other))

    def __rtruediv__(self, other: Any) -> Scalar:
        other = self._validate_other(other)
        if other is NotImplemented:
            return NotImplemented
        return self._from_scalar(self._value.__rtruediv__(other))

    def __neg__(self) -> Scalar:
        return self._from_scalar(self._value.__neg__())

    def __abs__(self) -> Scalar:
        return self._from_scalar(self._value.__abs__())

    def __bool__(self) -> bool:
        return self._materialise().__bool__()  # type: ignore[no-any-return]

    def __int__(self) -> int:
        return self._materialise().__int__()  # type: ignore[no-any-return]

    def __float__(self) -> float:
        return self._materialise().__float__()  # type: ignore[no-any-return]

    def __repr__(self) -> str:  # pragma: no cover
        header = f" Standard Scalar (api_version={self._api_version}) "
        length = len(header)
        return (
            "┌"
            + "─" * length
            + "┐\n"
            + f"|{header}|\n"
            + "| Add `.scalar` to see native output         |\n"
            + "└"
            + "─" * length
            + "┘\n"
        )
