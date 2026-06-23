"""Funcoes auxiliares para análise exploratoria de dados."""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


def summarize_numeric(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    percentiles: list[float] | None = None,
    round_digits: int = 2,
) -> pd.DataFrame:
    """Resume colunas numericas com estatisticas descritivas."""
    selected_columns = _resolve_numeric_columns(df, columns)
    if percentiles is None:
        percentiles = [0.25, 0.5, 0.75]

    summary = df[selected_columns].describe(percentiles=percentiles).T
    summary["missing"] = df[selected_columns].isna().sum()
    summary["missing_pct"] = df[selected_columns].isna().mean() * 100
    summary["unique"] = df[selected_columns].nunique(dropna=True)
    summary["skew"] = df[selected_columns].skew(numeric_only=True)

    return summary.round(round_digits)


def summarize_categorical(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    top_n: int = 10,
    include_na: bool = False,
    round_digits: int = 2,
) -> pd.DataFrame:
    """Resume colunas categoricas com frequencias absolutas e percentuais."""
    selected_columns = _resolve_categorical_columns(df, columns)
    summaries = []

    for column in selected_columns:
        counts = df[column].value_counts(dropna=not include_na).head(top_n)
        percentages = df[column].value_counts(
            normalize=True,
            dropna=not include_na,
        ).head(top_n) * 100

        column_summary = pd.DataFrame(
            {
                "column": column,
                "value": counts.index.astype(str),
                "count": counts.values,
                "percentage": percentages.values,
            }
        )
        summaries.append(column_summary)

    if not summaries:
        return pd.DataFrame(columns=["column", "value", "count", "percentage"])

    return pd.concat(summaries, ignore_index=True).round(round_digits)


def compare_groups(
    df: pd.DataFrame,
    group_col: str | list[str],
    value_col: str,
    round_digits: int = 2,
) -> pd.DataFrame:
    """Compara uma variavel numerica entre grupos."""
    group_columns = _as_list(group_col)
    _validate_columns(df, [*group_columns, value_col])

    summary = (
        df.groupby(group_columns, dropna=False)[value_col]
        .agg(
            count="count",
            mean="mean",
            median="median",
            std="std",
            min="min",
            q1=lambda series: series.quantile(0.25),
            q3=lambda series: series.quantile(0.75),
            max="max",
        )
        .reset_index()
    )

    return summary.round(round_digits)


def correlation_summary(
    df: pd.DataFrame,
    target_col: str,
    columns: list[str] | None = None,
    method: str = "pearson",
    min_abs_corr: float = 0,
    round_digits: int = 3,
) -> pd.DataFrame:
    """Calcula correlacoes numericas com uma variavel alvo."""
    selected_columns = _resolve_numeric_columns(df, columns)
    _validate_columns(df, [target_col])

    if target_col not in selected_columns:
        selected_columns.append(target_col)

    correlations = (
        df[selected_columns]
        .corr(method=method)[target_col]
        .drop(labels=[target_col])
        .dropna()
        .rename("correlation")
        .reset_index()
        .rename(columns={"index": "column"})
    )
    correlations["abs_correlation"] = correlations["correlation"].abs()
    correlations = correlations[correlations["abs_correlation"] >= min_abs_corr]
    correlations = correlations.sort_values("abs_correlation", ascending=False)

    return correlations.round(round_digits).reset_index(drop=True)


def group_difference_summary(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    reference_group: object | None = None,
    round_digits: int = 2,
) -> pd.DataFrame:
    """Calcula diferencas de media e mediana entre grupos e um grupo referencia."""
    _validate_columns(df, [group_col, value_col])

    summary = compare_groups(
        df=df,
        group_col=group_col,
        value_col=value_col,
        round_digits=10,
    )

    if summary.empty:
        return summary

    if reference_group is None:
        reference_row = summary.sort_values(group_col).iloc[0]
    else:
        reference_match = summary[summary[group_col] == reference_group]
        if reference_match.empty:
            raise ValueError(f"Reference group not found: {reference_group}")
        reference_row = reference_match.iloc[0]

    reference_mean = reference_row["mean"]
    reference_median = reference_row["median"]

    summary["reference_group"] = reference_row[group_col]
    summary["mean_diff"] = summary["mean"] - reference_mean
    summary["median_diff"] = summary["median"] - reference_median
    summary["mean_diff_pct"] = _safe_pct_diff(summary["mean"], reference_mean)
    summary["median_diff_pct"] = _safe_pct_diff(summary["median"], reference_median)

    return summary.round(round_digits)


def simple_linear_regression_summary(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    round_digits: int = 4,
) -> dict[str, float]:
    """Ajusta uma regressao linear simples e retorna os principais resultados."""
    _validate_columns(df, [x_col, y_col])

    model_df = df[[x_col, y_col]].dropna().copy()
    if model_df.empty:
        raise ValueError("Sem linhas disp. para reg")

    x = sm.add_constant(model_df[x_col])
    y = model_df[y_col]
    model = sm.OLS(y, x).fit()
    conf_int = model.conf_int().loc[x_col]

    return {
        "n_obs": int(model.nobs),
        "intercept": _round_float(model.params["const"], round_digits),
        "coefficient": _round_float(model.params[x_col], round_digits),
        "r_squared": _round_float(model.rsquared, round_digits),
        "adj_r_squared": _round_float(model.rsquared_adj, round_digits),
        "p_value": _round_float(model.pvalues[x_col], round_digits),
        "coef_ci_lower": _round_float(conf_int.iloc[0], round_digits),
        "coef_ci_upper": _round_float(conf_int.iloc[1], round_digits),
    }


def _validate_columns(df: pd.DataFrame, columns: list[str]) -> None:
    missing_columns = [column for column in columns if column not in df.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing}")


def _resolve_numeric_columns(
    df: pd.DataFrame,
    columns: list[str] | None,
) -> list[str]:
    if columns is None:
        return df.select_dtypes(include=np.number).columns.tolist()

    _validate_columns(df, columns)
    non_numeric = [column for column in columns if not pd.api.types.is_numeric_dtype(df[column])]
    if non_numeric:
        missing = ", ".join(non_numeric)
        raise ValueError(f"Columns must be numeric: {missing}")

    return list(columns)


def _resolve_categorical_columns(
    df: pd.DataFrame,
    columns: list[str] | None,
) -> list[str]:
    if columns is None:
        return df.select_dtypes(exclude=np.number).columns.tolist()

    _validate_columns(df, columns)
    return list(columns)


def _as_list(value: str | list[str]) -> list[str]:
    if isinstance(value, list):
        return value
    return [value]


def _safe_pct_diff(values: pd.Series, reference: float) -> pd.Series:
    if reference == 0:
        return pd.Series(np.nan, index=values.index)
    return ((values - reference) / abs(reference)) * 100


def _round_float(value: float, round_digits: int) -> float:
    return float(round(value, round_digits))


__all__ = [
    "summarize_numeric",
    "summarize_categorical",
    "compare_groups",
    "correlation_summary",
    "group_difference_summary",
    "simple_linear_regression_summary",
]
