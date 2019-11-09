import pandas as pd
from typing import List, Tuple
from matplotlib.colors import TABLEAU_COLORS
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from .utils import get_axes, get_jumps, get_levels, is_last, plot_text, plot_bar, remove_duplicated_legend_labels
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
    colors: List[str] = None
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

    Returns
    -------
    Tuple containing Figure and Axes of created histogram.
    """
    levels = get_levels(df)
    if colors is None:
        colors = list(TABLEAU_COLORS.keys())
    figure, axes, width = get_axes(df, bar_width, height, dpi, title, y_label)

    labels_offsets = {}
    old_index = []
    x = 0
    max_y = 0
    for i, (index, values) in enumerate(df.iterrows()):
        if not isinstance(index, (list, tuple)):
            index = (index,)
        jumps = get_jumps(df, i, index, old_index)
        old_x = x
        for j, value in enumerate(jumps):
            if value:
                text_x = old_x
                if j in labels_offsets:
                    text_x += labels_offsets[j]
                if is_last(df, i):
                    text_x += bar_width
                else:
                    x += bar_width
                plot_text(axes, text_x/2, j - len(jumps), old_index[j], width)
        old_index = index
        for j, value in enumerate(jumps):
            if value:
                labels_offsets[j] = x
        color = colors[levels[-1].index(index[-1])]
        label = index[-1]
        if len(values) == 2:
            y, std = values
        elif len(values) == 1:
            y, std = values.values[0], 0
        max_y = max(max_y, y+std)
        plot_bar(axes, x, y, std, min_std, bar_width, color, label)
        x += bar_width

    remove_duplicated_legend_labels(figure, axes, legend_position)
    axes.set_ylim(0, max_y*1.01)
    if any(e is not None and "time" in e for e in (path, title)):
        axes.set_yticklabels([
            naturaldelta(y) for y in axes.get_yticks()
        ])
    if path is not None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        figure.savefig(path, bbox_inches='tight')
    figure.tight_layout()
    return figure, axes
