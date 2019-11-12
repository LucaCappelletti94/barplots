import pandas as pd
from typing import List, Tuple
from matplotlib.colors import TABLEAU_COLORS
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from .utils import get_axes, get_jumps, get_levels, is_last, plot_text, plot_bar, remove_duplicated_legend_labels, sanitize_name
from humanize import naturaldelta
import os


def histogram(
    df: pd.DataFrame,
    bar_width: float = 0.3,
    height: float = None,
    dpi: int = 200,
    min_std: float = 0.01,
    legend_position: str = "best",
    y_label: str = None,
    title: str = None,
    path: str = None,
    colors: List[str] = None,
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
        Legend position, by default "best". Use None for hiding legend.
    y_label: str=None,
        Histogram's y_label. None for not showing any y_label (default).
    title: str=None,
        Histogram's title. None for not showing any title (default).
    path: str=None,
        Path where to save the histogram. None for not saving it (default).
    colors: List[str]=None,
        List of colors to be used for innermost index of dataframe.
        By default None, using the default color tableau from matplotlib.
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
        colors = list(TABLEAU_COLORS.keys())
    figure, axes, width = get_axes(
        df, bar_width, height, dpi, title, y_label, vertical)

    labels_offsets = {}
    old_index = []
    bar_position = 0
    max_bar_lenght = 0
    bars_positions = []
    bars_labels = []
    for i, (index, values) in enumerate(df.iterrows()):
        if not isinstance(index, (list, tuple)):
            index = (index,)
        jumps = get_jumps(df, i, index, old_index)
        old_bar_position = bar_position
        for j, value in enumerate(jumps):
            if value:
                text_position = old_bar_position
                if j in labels_offsets:
                    text_position += labels_offsets[j]
                if is_last(df, i):
                    text_position += bar_width
                else:
                    bar_position += bar_width
                plot_text(axes, text_position/2, j - len(jumps),
                          old_index[j], width, vertical)
        old_index = index
        for j, value in enumerate(jumps):
            if value:
                labels_offsets[j] = bar_position
        color = colors[levels[-1].index(index[-1])]
        label = index[-1]
        if len(values) == 2:
            bar_lenght, std = values
        elif len(values) == 1:
            bar_lenght, std = values.values[0], 0
        max_bar_lenght = max(max_bar_lenght, bar_lenght+std)
        current_bar_position = bar_position + bar_width/2
        bars_positions.append(current_bar_position)
        bars_labels.append(sanitize_name(label))
        plot_bar(axes, current_bar_position, bar_lenght, std,
                 min_std, bar_width, color, label, vertical)
        bar_position += bar_width

    remove_duplicated_legend_labels(figure, axes, legend_position)
    if vertical:
        axes.set_ylim(0, max_bar_lenght*1.01)
    else:
        axes.set_xlim(0, max_bar_lenght*1.01)
    if vertical:
        if any(e is not None and "time" in e for e in (path, title)):
            axes.set_yticklabels([
                naturaldelta(y) for y in axes.get_yticks()
            ])
        if show_bar_labels:
            axes.set_xticks(bars_positions)
            axes.set_xticklabels(bars_labels)
    else:
        if any(e is not None and "time" in e for e in (path, title)):
            axes.set_xticklabels([
                naturaldelta(x) for x in axes.get_xticks()
            ])
        if show_bar_labels:
            axes.set_yticks(bars_positions)
            axes.set_yticklabels(bars_labels)
    figure.tight_layout()
    if path is not None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        figure.savefig(path, bbox_inches='tight')
    return figure, axes
