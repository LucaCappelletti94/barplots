from matplotlib.figure import Figure
from matplotlib.axes import Axes
import pandas as pd
import numpy as np
from .get_max_bar_position import get_max_bar_position
from typing import Tuple
import matplotlib.pyplot as plt
from scipy.constants import golden_ratio
from typing import List, Union
from math import ceil


def swap(*args: List, flag: bool) -> List:
    """If the given flag is true returns """
    return args if flag else reversed(args)


def get_axes(
    df: pd.DataFrame,
    bar_width: float,
    height: float,
    dpi: int,
    title: str,
    y_label: str,
    vertical: bool,
    split_plots: bool,
    plots_per_row: Union[int, str]
) -> Tuple[Figure, Axes]:
    """Setup axes for histogram plotting.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to obtain the curresponding histogram width.
    bar_width: float,
        Width of bars in considered histogram.
    height: float,
        Height of considered histogram.
    dpi: int,
        DPI for rendered images.
    title: str,
        Title of the considered histogram.
    y_label: str,
        Histogram's y_label. None for not showing any y_label (default).
    vertical: bool,
        Whetever to build the axis to show the bars as vertical or as horizontal.

    Returns
    -----------
    Tuple containing new figure and axis.
    """
    if split_plots:
        side = max(
            get_max_bar_position(df.loc[index], bar_width)
            for index in df.index.levels[0]
        )
    else:
        side = get_max_bar_position(df, bar_width)

    if height is None:
        height = side/(golden_ratio**(2-int(split_plots)))

    if plots_per_row == "auto":
        plots_per_row = 2 if vertical else 4
        plots_per_row = min(df.index.levels[0].size, plots_per_row)

    if split_plots:
        nrows = ceil(df.index.levels[0].size/plots_per_row)
    else:
        nrows = plots_per_row = 1

    width, height = swap(side, height, flag=vertical)
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=plots_per_row,
        figsize=(width*plots_per_row, height*nrows),
        dpi=dpi
    )

    if isinstance(axes, Axes):
        axes = np.array([axes])

    for subtitle, ax in zip(df.index.levels[0], axes.flatten()):
        if vertical:
            ax.set_xlim(0, side)
            ax.set_ylim(0)
            ax.set_xticks([])
            ax.yaxis.grid(True, which="both")
            if y_label is not None:
                ax.set_ylabel(y_label)
        else:
            ax.set_ylim(0, side)
            ax.set_xlim(0)
            ax.set_yticks([])
            ax.xaxis.grid(True, which="both")
            if y_label is not None:
                ax.set_xlabel(y_label)

        ax.set_title(subtitle)

    for ax in axes.flatten()[df.index.levels[0].size:]:
        ax.grid(False)
        ax.axis('off')

    if title is not None and len(axes) == 1:
        axes[0].set_title(title)

    return fig, axes.flatten()
