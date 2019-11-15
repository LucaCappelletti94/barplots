from matplotlib.figure import Figure
from matplotlib.axes import Axes
import pandas as pd
from .get_max_bar_position import get_max_bar_position
from typing import Tuple
import matplotlib.pyplot as plt
from scipy.constants import golden_ratio
from typing import List

def swap(*args: List, flag: bool) -> List:
    """If the given flag is true returns """
    return args if flag else reversed(args)


def get_axes(df: pd.DataFrame, bar_width: float, height: float, dpi: int, title: str, y_label: str, vertical: bool) -> Tuple[Figure, Axes]:
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
    side = get_max_bar_position(df, bar_width)
    if height is None:
        height = side/(golden_ratio**2)
    width, height = swap(side, height, flag=vertical)
    fig, axes = plt.subplots(figsize=(width, height), dpi=dpi)

    if vertical:
        axes.set_xlim(0, side)
        axes.set_ylim(0)
        axes.set_xticks([])
        axes.yaxis.grid(True, which="both")
        if y_label is not None:
            axes.set_ylabel(y_label)
    else:
        axes.set_ylim(0, side)
        axes.set_xlim(0)
        axes.set_yticks([])
        axes.xaxis.grid(True, which="both")
        if y_label is not None:
            axes.set_xlabel(y_label)

    if title is not None:
        axes.set_title(title)
    return fig, axes
