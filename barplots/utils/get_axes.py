"""Function to setup axes for barplot plotting."""

from typing import Tuple, Dict, List
from math import ceil
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import golden_ratio
from sanitize_ml_labels import sanitize_ml_labels
from barplots.utils.get_best_match import get_best_match
from barplots.utils.get_max_bar_position import get_max_bar_position


def swap(*args: List, flag: bool) -> List:
    """If the given flag is true returns"""
    return args if flag else reversed(args)


def get_axes(
    df: pd.DataFrame,
    bar_width: float,
    space_width: float,
    height: float,
    dpi: int,
    title: str,
    data_label: str,
    vertical: bool,
    subplots: bool,
    titles: List[str],
    plots_per_row: int,
    custom_defaults: Dict[str, List[str]],
    expected_levels: int,
    scale: str,
    facecolors: Dict[str, str],
    show_title: bool,
    show_column_name: bool,
) -> Tuple[Figure, Axes]:
    """Setup axes for barplot plotting.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to obtain the curresponding barplot width.
    bar_width: float,
        Width of bars in considered barplot.
    space_width: float,
        Width of spaces between spaces.
    height: float,
        Height of considered barplot.
    dpi: int,
        DPI for rendered images.
    title: str,
        Title of the considered barplot.
    data_label: str,
        barplot's data_label. None for not showing any data_label (default).
    vertical: bool,
        Whetever to build the axis to show the bars as vertical or as horizontal.
    expected_levels: int,
        Number of levels to expect to plot as labels.
    scale: str,
        Scale to use for the barplots.
        Can either be "linear" or "log".
    facecolors: Dict[str, str],
        Colors for the background.
    show_title: str = True,
        Whetever to show or not the barplot title.
    show_column_name: bool = True
        Whether to show the metric name.

    Returns
    -----------
    Tuple containing new figure and axis.
    """
    if subplots:
        side = max(
            get_max_bar_position(df.loc[index], bar_width, space_width)
            for index in df.index.levels[0]
        )
    else:
        side = get_max_bar_position(df, bar_width, space_width)

    if height is None:
        exponent = 1 if subplots or expected_levels > 1 else 1.5
        height = side / (golden_ratio**exponent)

    if subplots:
        nrows = ceil(df.index.levels[0].size / plots_per_row)
    else:
        nrows = plots_per_row = 1

    width, height = swap(side, height, flag=vertical)
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=plots_per_row,
        figsize=(width * plots_per_row, height * nrows),
        dpi=dpi,
    )
    fig.patch.set_facecolor("white")

    if isinstance(axes, Axes):
        axes = np.array([axes])

    axes = axes.flatten()

    for subtitle, ax in zip(titles, axes):
        ax.set_facecolor(get_best_match(facecolors, subtitle))
        if vertical:
            ax.set_yscale(scale)
            ax.set_xlim(0, side)
            ax.set_xticks([])
            ax.yaxis.grid(True, which="both")
            if data_label is not None and show_column_name:
                ax.set_ylabel(
                    sanitize_ml_labels(data_label, custom_defaults=custom_defaults)
                )
        else:
            ax.set_xscale(scale)
            ax.set_ylim(0, side)
            ax.set_yticks([])
            ax.xaxis.grid(True, which="both")
            if data_label is not None and show_column_name:
                ax.set_xlabel(
                    sanitize_ml_labels(data_label, custom_defaults=custom_defaults)
                )
        if show_title:
            ax.set_title(sanitize_ml_labels(subtitle, custom_defaults=custom_defaults))

    for ax in axes[len(titles) :]:
        ax.grid(False)
        ax.axis("off")

    if title is not None and len(axes) == 1 and show_title:
        axes[0].set_title(sanitize_ml_labels(title, custom_defaults=custom_defaults))

    return fig, axes
