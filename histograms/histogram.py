import pandas as pd
from typing import List, Tuple, Dict, Union
from matplotlib.colors import TABLEAU_COLORS
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from .utils import get_axes, get_jumps, get_levels, is_last, plot_bar, \
    remove_duplicated_legend_labels, bar_positions,\
    save_picture, text_positions, plot_bars, plot_bar_labels, humanize_time_ticks

from humanize import naturaldelta
import os


def histogram(
    df: pd.DataFrame,
    bar_width: float = 0.3,
    height: float = None,
    dpi: int = 200,
    min_std: float = 0.01,
    show_legend: bool = True,
    legend_position: str = "best",
    data_label: str = None,
    title: str = None,
    path: str = None,
    colors: Dict[str, str] = None,
    alphas: Dict[str, float] = None,
    orientation: str = "vertical",
    subplots: bool = False,
    plots_per_row: Union[int, str] = "auto",
    humanize_time_features: bool = True,
    minor_rotation:float=0,
    major_rotation:float=0
) -> Tuple[Figure, Axes]:
    """Plot histogram corresponding to given dataframe, containing y value and optionally std.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to extrat data for plotting histogram.
    bar_width: float=0.3,
        Width of the bar of the histogram.
    height: float=None,
        Height of the histogram. By default golden ratio.
    dpi: int=100,
        DPI for plotting the histograms.
    min_std: float=0.01,
        Minimum standard deviation for showing error bars.
    legend_position: str="best",
        Legend position, by default "best".
    data_label: str=None,
        Histogram's data_label. None for not showing any data_label (default).
    title: str=None,
        Histogram's title. None for not showing any title (default).
    path: str=None,
        Path where to save the histogram. None for not saving it (default).
    colors: Dict[str]=None,
        Dict of colors to be used for innermost index of dataframe.
        By default None, using the default color tableau from matplotlib.
    colors: Dict[str]=None,
        Dict of alphas to be used for innermost index of dataframe.
        By default None, using the default alpha.
    orientation: str = "vertical",
        Orientation of the bars. Can either be "vertical" of "horizontal".

    Raises
    ------
    ValueError:
        If the given orientation is nor "vertical" nor "horizontal".
    ValueError:
        If the given plots_per_row is nor "auto" or a positive integer.
    ValueError:
        If subplots is True and less than a single index level is provided.

    Returns
    -------
    Tuple containing Figure and Axes of created histogram.
    """
    
    if orientation not in ("vertical", "horizontal"):
        raise ValueError("Given orientation \"{orientation}\" is not supported.".format(
            orientation=orientation
        ))

    if not isinstance(plots_per_row, int) and plots_per_row != "auto" or isinstance(plots_per_row, int) and plots_per_row<1:
        raise ValueError("Given plots_per_row \"{plots_per_row}\" is not 'auto' or a positive integer.".format(
            plots_per_row=plots_per_row
        ))

    vertical = orientation == "vertical"

    levels = get_levels(df)

    if len(levels) <= 1 and subplots:
        raise ValueError("Unable to split plots with only a single index level.")

    if colors is None:
        colors = dict(zip(levels[-1], TABLEAU_COLORS.keys()))
    if alphas is None:
        alphas = dict(zip(levels[-1], (0.75,)*len(levels[-1])))

    figure, axes = get_axes(
        df, bar_width, height, dpi, title, data_label, vertical, subplots, plots_per_row
    )

    for index, ax in zip(levels[0], axes):
        if subplots:
            sub_df = df.loc[index]
        else:
            sub_df = df

        plot_bars(ax, sub_df, bar_width, alphas, colors,
                vertical=vertical, min_std=min_std)

        plot_bar_labels(
            ax,
            figure,
            sub_df,
            vertical,
            len(levels) - int(show_legend) - int(subplots),
            bar_width,
            minor_rotation,
            major_rotation
        )

        if any(e is not None and "time" in e for e in (path, title)):
            humanize_time_ticks(ax, vertical)

        if show_legend:
            remove_duplicated_legend_labels(ax, legend_position)
        
    figure.tight_layout()

    if path is not None:
        save_picture(path, figure)

    return figure, axes
