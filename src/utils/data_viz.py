"""Pacote usado para gerar visualizações úteis para análises"""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from seaborn.axisgrid import FacetGrid


NPS_CATEGORY_PALETTE: dict[str, str] = {
    "Detrator": "#DC2626",
    "Neutro": "#F59E0B",
    "Promotor": "#16A34A",
}

def plot_comparative_histogram(
    df,
    value_col,
    group_col,
    bins=30,
    title=None,
    x_label=None,
    y_label="Densidade",
    kde=True,
    alpha=0.45,
    figsize=(10, 5)
):
    """
    Plota histogramas comparativos de uma variável numérica por grupo.

    Exemplo:
    plot_comparative_histogram(
        df,
        value_col="delivery_delay_days",
        group_col="classificacao",
        title="Distribuição de atraso por classificação NPS",
        x_label="Dias de atraso"
    )
    """

    plot_df = df[[value_col, group_col]].dropna().copy()

    fig, ax = plt.subplots(figsize=figsize)

    sns.histplot(
        data=plot_df,
        x=value_col,
        hue=group_col,
        bins=bins,
        stat="density",
        common_norm=False,
        kde=kde,
        element="step",
        fill=True,
        alpha=alpha,
        linewidth=1.4,
        ax=ax
    )

    ax.set_title(
        title or f"Distribuição de {value_col} por {group_col}",
        fontsize=15,
        fontweight="bold",
        pad=14
    )
    ax.set_xlabel(x_label or value_col, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.grid(axis="y", alpha=0.25)
    ax.grid(axis="x", alpha=0.08)

    plt.tight_layout()
    plt.show()


def plot_boxplot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    hue_col: str | None = None,
    title: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    legend_title: str | None = None,
    figsize: tuple[int, int] = (10, 5),
    palette: str | Mapping[str, str] | None = "Set2",
    order: list[str] | None = None,
    hue_order: list[str] | None = None,
    show_points: bool = False,
    point_alpha: float = 0.35,
    point_size: float = 3,
    rotate_xticks: int = 0,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plota um boxplot formatado para comparar uma variavel numerica por grupos."""
    columns = [x_col, y_col]
    if hue_col is not None:
        columns.append(hue_col)
    _validate_columns(df, columns)

    sns.set_theme(style="whitegrid", context="notebook")

    plot_df = df[columns].dropna().copy()

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    sns.boxplot(
        data=plot_df,
        x=x_col,
        y=y_col,
        hue=hue_col,
        order=order,
        hue_order=hue_order,
        palette=palette,
        width=0.65,
        linewidth=1.3,
        fliersize=3,
        ax=ax,
    )

    if show_points:
        sns.stripplot(
            data=plot_df,
            x=x_col,
            y=y_col,
            hue=hue_col,
            order=order,
            hue_order=hue_order,
            palette=palette,
            dodge=hue_col is not None,
            alpha=point_alpha,
            size=point_size,
            linewidth=0,
            ax=ax,
            legend=False,
        )

    ax.set_title(
        title or f"{_humanize_column_name(y_col)} por {_humanize_column_name(x_col)}",
        fontsize=15,
        fontweight="bold",
        loc="left",
        pad=14,
    )
    ax.set_xlabel(x_label or _humanize_column_name(x_col), fontsize=12, labelpad=9)
    ax.set_ylabel(y_label or _humanize_column_name(y_col), fontsize=12, labelpad=9)
    ax.grid(axis="y", alpha=0.25)
    ax.grid(axis="x", alpha=0.05)

    if rotate_xticks:
        ax.tick_params(axis="x", rotation=rotate_xticks)

    if hue_col is not None:
        _format_legend(
            ax,
            title=legend_title or _humanize_column_name(hue_col),
            loc="best",
        )
    elif ax.get_legend() is not None:
        ax.get_legend().remove()

    sns.despine(ax=ax, left=False, bottom=False)
    fig.tight_layout()

    return fig, ax


def plot_crosstab_heatmap(
    df: pd.DataFrame,
    row_col: str,
    col_col: str,
    normalize: str | None = None,
    title: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    colorbar_label: str | None = None,
    figsize: tuple[int, int] = (9, 5),
    cmap: str = "Blues",
    annot: bool = True,
    fmt: str | None = None,
    sort_index: bool = True,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plota um heatmap de tabela cruzada entre duas variaveis discretas."""
    _validate_columns(df, [row_col, col_col])

    if normalize not in {None, "index", "columns", "all"}:
        raise ValueError("normalize must be one of: None, 'index', 'columns', 'all'")

    sns.set_theme(style="whitegrid", context="notebook")

    crosstab_normalize = False if normalize is None else normalize

    heatmap_data = pd.crosstab(
        df[row_col],
        df[col_col],
        normalize=crosstab_normalize,
    )

    if normalize is not None:
        heatmap_data = heatmap_data * 100

    if sort_index:
        heatmap_data = heatmap_data.sort_index().sort_index(axis=1)

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    value_fmt = fmt
    if value_fmt is None:
        value_fmt = ".1f" if normalize is not None else "d"

    default_colorbar_label = "Percentual (%)" if normalize is not None else "Quantidade"

    sns.heatmap(
        heatmap_data,
        annot=annot,
        fmt=value_fmt,
        cmap=cmap,
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": colorbar_label or default_colorbar_label},
        ax=ax,
    )

    ax.set_title(
        title
        or f"{_humanize_column_name(row_col)} x {_humanize_column_name(col_col)}",
        fontsize=15,
        fontweight="bold",
        loc="left",
        pad=14,
    )
    ax.set_xlabel(x_label or _humanize_column_name(col_col), fontsize=12, labelpad=9)
    ax.set_ylabel(y_label or _humanize_column_name(row_col), fontsize=12, labelpad=9)

    fig.tight_layout()

    return fig, ax


def plot_faceted_regression(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    facet_col: str,
    hue_col: str | None = None,
    title: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    col_wrap: int = 3,
    height: float = 3.5,
    aspect: float = 1.2,
    scatter_alpha: float = 0.25,
    scatter_size: float = 25,
    line_color: str = "#DC2626",
    line_width: float = 2,
    palette: str | Mapping[str, str] | None = None,
    facet_order: list[str] | None = None,
    hue_order: list[str] | None = None,
) -> FacetGrid:
    """Plota relacao linear facetada para comparar associacoes entre grupos."""
    columns = [x_col, y_col, facet_col]
    if hue_col is not None:
        columns.append(hue_col)
    _validate_columns(df, columns)

    sns.set_theme(style="whitegrid", context="notebook")

    plot_df = df[columns].dropna().copy()

    grid = sns.lmplot(
        data=plot_df,
        x=x_col,
        y=y_col,
        col=facet_col,
        hue=hue_col,
        col_wrap=col_wrap,
        col_order=facet_order,
        hue_order=hue_order,
        height=height,
        aspect=aspect,
        palette=palette,
        scatter_kws={
            "alpha": scatter_alpha,
            "s": scatter_size,
        },
        line_kws={
            "color": line_color,
            "linewidth": line_width,
        },
    )

    grid.set_axis_labels(
        x_label or _humanize_column_name(x_col),
        y_label or _humanize_column_name(y_col),
    )
    grid.set_titles("{col_name}")

    if title is not None:
        grid.fig.suptitle(title, fontsize=15, fontweight="bold", y=1.03)

    grid.fig.tight_layout()

    return grid

def add_nps_category(
    df: pd.DataFrame,
    nps_col: str = "nps_score",
    category_col: str = "categoria_nps",
) -> pd.DataFrame:
    """Retorna uma cópia do df com as categorais de NPS de mercado"""
    _validate_columns(df, [nps_col])

    result = df.copy()
    result[category_col] = np.select(
        [result[nps_col] <= 6, result[nps_col] <= 8],
        ["Detrator", "Neutro"],
        default="Promotor",
    )
    return result


def plot_nps_relationship(
    df: pd.DataFrame,
    x_col: str,
    y_col: str = "nps_score",
    id_col: str = "order_id",
    title: str | None = None,
    x_label: str | None = None,
    y_label: str = "Nota NPS",
    mean_line_label: str | None = None,
    figsize: tuple[int, int] = (12, 7),
    palette: Mapping[str, str] | None = None,
    ax: Axes | None = None,
    show_mean_line: bool = True,
    show_correlation: bool = False,
    show_nps_bands: bool = True,
    correlation_label: str | None = None,
) -> tuple[Figure, Axes]:
    """Plota uma coluna numérica x NPS
    """
    _validate_columns(df, [x_col, y_col, id_col])

    sns.set_theme(style="whitegrid", context="talk")

    plot_df = add_nps_category(df, nps_col=y_col)
    category_col = "categoria_nps"
    color_palette = dict(palette or NPS_CATEGORY_PALETTE)

    summary = (
        plot_df.groupby(x_col, as_index=False)
        .agg(nps_medio=(y_col, "mean"), pedidos=(id_col, "count"))
        .sort_values(x_col)
    )

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    if show_nps_bands:
        _add_nps_bands(ax)

    sns.scatterplot(
        data=plot_df,
        x=x_col,
        y=y_col,
        hue=category_col,
        hue_order=["Detrator", "Neutro", "Promotor"],
        palette=color_palette,
        alpha=0.50,
        s=58,
        edgecolor="white",
        linewidth=0.45,
        ax=ax,
    )

    if show_mean_line:
        sns.lineplot(
            data=summary,
            x=x_col,
            y="nps_medio",
            color="#111827",
            marker="o",
            markersize=7,
            linewidth=2.8,
            label=mean_line_label or f"NPS medio por {x_col}",
            ax=ax,
        )

    chart_title = title or f"{_humanize_column_name(x_col)} vs. NPS"
    ax.set_title(chart_title, fontsize=20, fontweight="bold", loc="left", pad=18)
    ax.set_xlabel(x_label or _humanize_column_name(x_col), fontsize=13, labelpad=10)
    ax.set_ylabel(y_label, fontsize=13, labelpad=10)
    ax.set_ylim(-0.3, 10.3)
    ax.set_xlim(left=-0.4)
    ax.grid(axis="y", alpha=0.25)
    ax.grid(axis="x", alpha=0.10)

    if show_correlation:
        correlation = plot_df[x_col].corr(plot_df[y_col])
        _add_correlation_note(
            ax,
            correlation,
            label=correlation_label or f"Correlacao {x_col} x NPS",
        )

    _format_legend(ax)
    sns.despine(ax=ax, left=False, bottom=False)
    fig.tight_layout()

    return fig, ax


def _validate_columns(df: pd.DataFrame, columns: list[str]) -> None:
    missing_columns = [column for column in columns if column not in df.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing}")


def _humanize_column_name(column: str) -> str:
    return column.replace("_", " ").capitalize()


def _add_nps_bands(ax: Axes) -> None:
    ax.axhspan(0, 6, color=NPS_CATEGORY_PALETTE["Detrator"], alpha=0.06, zorder=0)
    ax.axhspan(6, 8, color=NPS_CATEGORY_PALETTE["Neutro"], alpha=0.06, zorder=0)
    ax.axhspan(8, 10, color=NPS_CATEGORY_PALETTE["Promotor"], alpha=0.06, zorder=0)
    ax.axhline(
        6,
        color=NPS_CATEGORY_PALETTE["Detrator"],
        linestyle="--",
        linewidth=1.2,
        alpha=0.75,
    )
    ax.axhline(
        8,
        color=NPS_CATEGORY_PALETTE["Promotor"],
        linestyle="--",
        linewidth=1.2,
        alpha=0.75,
    )


def _add_correlation_note(ax: Axes, correlation: float, label: str) -> None:
    ax.text(
        0.99,
        0.05,
        f"{label}: {correlation:.2f}",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=12,
        color="#374151",
        bbox={
            "boxstyle": "round,pad=0.45",
            "facecolor": "white",
            "edgecolor": "#D1D5DB",
            "alpha": 0.95,
        },
    )


def _format_legend(
    ax: Axes,
    title: str = "Categoria",
    loc: str = "upper right",
) -> None:
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles=handles,
        labels=labels,
        title=title,
        frameon=True,
        facecolor="white",
        edgecolor="#E5E7EB",
        loc=loc,
    )

__all__ = [
    "NPS_CATEGORY_PALETTE",
    "add_nps_category",
    "plot_nps_relationship",
    "plot_comparative_histogram",
    "plot_boxplot",
    "plot_crosstab_heatmap",
    "plot_faceted_regression",
]
