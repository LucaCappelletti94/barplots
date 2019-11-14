import pandas as pd
from typing import List, Tuple, Dict
from matplotlib.colors import TABLEAU_COLORS
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from .utils import get_axes, get_jumps, get_levels, is_last, plot_text, plot_bar, remove_duplicated_legend_labels, sanitize_name, bar_positions
from humanize import naturaldelta
import os
from .text_positions import text_positions
from .plot_bars import plot_bars


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
    show_bar_labels: bool = False
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
    show_bar_labels: bool = False,
        Whetever to show or not the x ticks bar labels.

    Raises
    ------
    ValueError:
        If the given orientation is nor "vertical" nor "horizontal".

    Returns
    -------
    Tuple containing Figure and Axes of created histogram.
    """

    if orientation not in ("vertical", "horizontal"):
        raise ValueError("Given orientation \"{orientation}\" is not supported.".format(
            orientation=orientation
        ))

    vertical = orientation is "vertical"

    levels = get_levels(df)

    if colors is None:
        colors = dict(zip(levels[-1], TABLEAU_COLORS.keys()))
    if alphas is None:
        alphas = dict(zip(levels[-1], (0.75,)*len(levels[-1])))

    figure, axes = get_axes(
        df, bar_width, height, dpi, title, data_label, vertical
    )

    plot_bars(axes, df, bar_width, alphas, colors,
              vertical=vertical, min_std=min_std)

    # max_bar_lenght = get_max_bar_lenght(df, bar_width)
    # if vertical:
    #     axes.set_ylim(0, max_bar_lenght*1.01)
    # else:
    #     axes.set_xlim(0, max_bar_lenght*1.01)

    # if vertical:
    #     if any(e is not None and "time" in e for e in (path, title)):
    #         axes.set_yticklabels([
    #             naturaldelta(y) for y in axes.get_yticks()
    #         ])
    # else:
    #     if any(e is not None and "time" in e for e in (path, title)):
    #         axes.set_xticklabels([
    #             naturaldelta(x) for x in axes.get_xticks()
    #         ])

    n = len(levels) - int(show_legend)
    other_positions = set()
    for i in reversed(range(n-2, n)):
        positions, labels = zip(*text_positions(df, bar_width, i))
        positions = [
            round(pos, 4) for pos in positions
        ]
        positions = [
            position + 0.001 if position in other_positions else position 
            for position in positions
        ]
        other_positions |= set(positions)
        minor = i == n-1
        axes.set_yticks(positions, minor=minor)
        labels = axes.set_yticklabels(labels, minor=minor)
        if minor:
            labels_offset = max(
                label.get_window_extent(figure.canvas.get_renderer()).width
                for label in labels
            )/2.25

    axes.tick_params(axis='y', which='major', direction='out', length=labels_offset, width=0)

    if show_legend:
        remove_duplicated_legend_labels(figure, axes, legend_position)
    figure.tight_layout()
    if path is not None:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        figure.savefig(path, bbox_inches='tight')
    return figure, axes
