import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.colors import TABLEAU_COLORS
from tqdm.auto import tqdm
from typing import List, Any, Union, Tuple, Dict
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from pandas.core.index import MultiIndex
from multiprocessing import Pool, cpu_count
from humanize import naturaldelta
from scipy.constants import golden_ratio


def is_last(df: pd.DataFrame, row: int) -> bool:
    """Return boolean representing if given row is the last row.

    Parameters
    ----------
    df: pd.DataFrame,
        The dataframe to check against.
    row: int,
        The index of the row to consider.

    Returns
    -------
    A boolean representing if given row is the last one.
    """
    return row+1 == df.shape[0]


def sanitize_name(name: str) -> str:
    """Return sanitized name.

    Parameters
    ----------
    name: str,
        The name to be sanitize.

    Returns
    -------
    The sanitized name.    
    """
    return str(name).replace("_", " ")


def histogram_width(df: pd.DataFrame, bar_width: float) -> float:
    """Return histogram width for given dataframe and bar width.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to obtain the curresponding histogram width.
    bar_width: float,
        Width of bars in considered histogram.

    Returns
    -------
    Return float representing histogram total width.
    """
    old_index = None
    width = bar_width*df.shape[0]
    for row, index in enumerate(df.index):
        if not is_last(df, row):
            width += sum(get_jumps(df, row, index, old_index))*bar_width
        old_index = index
    return width


def get_jumps(df: pd.DataFrame, row: int, index: Union[List, Any], old_index: Union[List, Any]) -> List[bool]:
    """Return list representing the detected jumps from given index and old_index.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to detect index jumps.
    row: int,
        Current row number.
    index:Union[List, Any],
        List of indices of index curresponding to given row number.
    old_index:Union[List, Any],
        Old index.

    Returns
    -------
    Returns list of boolean representing if for given index level a jump has been detected.
    """
    if not isinstance(index, (tuple, list)) or not old_index:
        return tuple()
    return [
        new != old or is_last(df, row)
        for new, old in zip(index[:-1], old_index)
    ]


def remove_duplicated_legend_labels(figure: Figure, axes: Axes, legend_position: str):
    """Remove duplicated labels from the plot legend.

    Parameters
    ----------
    figure:Figure,
        Figure containing the labels.
    axes: Axes,
        Axes where to show the labels.
    legend_position: str,
        Legend position, by default "best". Use None for hiding legend.
    """
    handles, labels = figure.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    if legend_position is not None:
        axes.legend(by_label.values(), by_label.keys(), loc=legend_position)


def plot_bar(axes: Axes, x: float, y: float, std: float, min_std: float, bar_width: float, color: str, label: str):
    """Plot bar with given properties.

    Parameters
    ----------
    axes: Axes,
        Axes object where to plot the bar.
    x: float,
        Position for the left size of the bar.
    y: float,
        Height of the considered bar.
    std: float,
        Standard deviation to plot on top.
    min_std: float,
        Minimum standard deviation to be shown.
    bar_width: float,
        Width of the bar.
    color: str,
        Color of the bar.
    label: str,
        Label of the bar.
    """
    axes.bar(
        x + bar_width/2,
        y+1,
        bottom=-1,
        **({"yerr": std} if std > min_std else {}),
        color=color,
        error_kw={
            "ecolor": "black",
            "alpha": 0.75
        },
        width=bar_width,
        capsize=5,
        alpha=0.75,
        label=sanitize_name(label)
    )


def plot_text(axes: Axes, x: float, y: float, text: str, width: float):
    """Plot text with given properties.

    Parameters
    ----------
    axes: Axes,
        Axes object where to plot the text.
    x: float,
        Center coordinate for the text horizzontal axes.
    y: float,
        Center coordinate for the text vertical axes.
    text: str,
        Text to be shown.
    width: float,
        Total width of the histogram for normalizing the X position
    """
    axes.text(
        x/(width),
        y/15,
        sanitize_name(text),
        horizontalalignment='center',
        verticalalignment='center',
        transform=axes.transAxes
    )


def get_axes(df: pd.DataFrame, bar_width: float, height: float, dpi: int, title: str, y_label: str) -> Tuple[Figure, Axes]:
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

    Returns
    -----------
    """
    width = histogram_width(df, bar_width)
    if height is None:
        height = width/(golden_ratio**2)
    fig, axes = plt.subplots(figsize=(width, height), dpi=dpi)
    axes.set_xlim(0, width)
    axes.set_ylim(0)
    axes.set_xticks([])
    axes.yaxis.grid(True, which="both")
    if title is not None:
        axes.set_title(title)
    if y_label is not None:
        axes.set_ylabel(y_label)
    return fig, axes, width


def get_levels(df: pd.DataFrame) -> List[List[Any]]:
    """Return normalized list of dataframe index levels.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to extract index levels.

    Returns
    -------
    List of lists of unique indices.
    """
    if isinstance(df.index, MultiIndex):
        return [
            list(e) for e in df.index.levels
        ]
    else:
        return [df.index.unique().tolist()]


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
            y, std = values, 0
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


def _histogram(kwargs):
    histogram(**kwargs)


def histograms(
    df: pd.DataFrame,
    indices: List,
    show_standard_deviation: bool = True,
    title: str = "{feature}",
    y_label: str = "{feature}",
    path: str = "histograms/{feature}.jpg",
    **histogram_kwargs: Dict
):
    """
    Plot histograms corresponding to given dataframe,
    grouping by mean and if required also standard deviation.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to extrat data for plotting histogram.
    indices: List,
        List of indices over to run group by.
    show_standard_deviation:bool=True,
        Whetever to show or not the standard deviation. By default True.
    histogram_kwargs:Dict,
        Kwargs parameters to pass to the histogram method.
    """
    groupby = df.groupby(indices).agg(
        ("mean",)+(("std",) if show_standard_deviation else tuple())
    ).sort_index()
    tasks = [
        {
            "df": groupby[feature],
            "title":title.format(feature=feature.replace("_", " ")),
            "y_label":title.format(feature=feature.replace("_", " ")),
            "path":path.format(feature=feature),
            **histogram_kwargs
        } for feature in groupby.columns.levels[0]
    ]
    with Pool(cpu_count()) as p:
        list(tqdm(
            p.imap(_histogram, tasks),
            desc="Rendering histograms",
            total=len(tasks),
            dynamic_ncols=True
        ))
        p.close()
        p.join()
