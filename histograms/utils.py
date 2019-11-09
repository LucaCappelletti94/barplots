import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Any, Union, Tuple
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from pandas.core.index import MultiIndex
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