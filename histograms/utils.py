import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Any, Union, Tuple
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from pandas.core.index import MultiIndex
from scipy.constants import golden_ratio

import pandas as pd
from typing import Dict
from matplotlib.axes import Axes

import pandas as pd
from typing import Generator
from scipy.constants import golden_ratio


def bar_positions(df: pd.DataFrame, bar_width: float) -> Generator:
    """Returns a generator of bar positions.
        df: pd.DataFrame,
            Dataframe to iterate to extract the necessary data.
        bar_width:float,
            Width of any given bar.
    """
    old_index = tuple()
    bar_position = 0
    for i, (index, values) in enumerate(df.iterrows()):
        if not isinstance(index, (list, tuple)):
            index = (index,)

        if not is_last(df, i):
            bar_position += bar_width * sum(
                get_jumps(df, i, index, old_index)
            )
        else:
            bar_position += bar_width
        old_index = index

        if len(values) == 2:
            y, std = values
        elif len(values) == 1:
            y, std = values.values[0], 0

        yield (
            bar_position + bar_width / 2,
            y,
            std,
            sanitize_name(index[-1]),
            index[-1]
        )


def get_max_bar_lenght(
    df: pd.DataFrame,
    bar_width: float
) -> float:
    """Return maximum bar size, including std.

    Parameters
    ----------
    df: pd.DataFrame,
        The dataframe from where to extract the data.
    bar_width: float,
        The width of the bars, used also for spacing
    """
    return max(
        y + std for _, y, std, _, _ in bar_positions(df, bar_width)
    )


def get_max_bar_position(
    df: pd.DataFrame,
    bar_width: float
) -> float:
    """Return maximum bar size, including std.

    Parameters
    ----------
    df: pd.DataFrame,
        The dataframe from where to extract the data.
    bar_width: float,
        The width of the bars, used also for spacing
    """
    return max(
        x for x, _, _, _, _ in bar_positions(df, bar_width)
    ) + bar_width/2


def swap(*args: List, flag: bool) -> List:
    """If the given flag is true returns """
    return args if flag else reversed(args)


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
    if not isinstance(index, (tuple, list)):
        return tuple(True)
    if not old_index:
        return [False]*len(index)
    return [
        new != old or is_last(df, row)
        for new, old in zip(index, old_index)
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
        Legend position.
    """
    handles, labels = figure.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    axes.legend(by_label.values(), by_label.keys(), loc=legend_position)


def plot_bar(
    axes: Axes,
    x: float,
    y: float,
    std: float,
    min_std: float,
    bar_width: float,
    vertical: bool,
    **kwargs
):
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
    vertical: bool,
        Whetever to build the axis to show the bars as vertical or as horizontal.
    """
    if vertical:
        axes.bar(
            x=x,
            height=y+1,
            width=bar_width,
            **({"yerr": std} if std > min_std else {}),
            capsize=5,
            **kwargs
        )
    else:
        axes.barh(
            y=x,
            width=y,
            height=bar_width,
            **({"xerr": std} if std > min_std else {}),
            capsize=5,
            **kwargs
        )


def plot_text(axes: Axes, x: float, y: float, text: str, vertical: bool):
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
    vertical: bool,
        Whetever to build the axis to show the bars as vertical or as horizontal.
    """
    if vertical:
        axes.text(
            x=x,
            y=y,
            s=sanitize_name(text),
            horizontalalignment='center',
            verticalalignment='top',
            transform=axes.transAxes
        )
    else:
        #axes.scatter(y, x, s=100, color="tab:red")
        trans = axes.get_transform()
        axes.annotate(
            s=sanitize_name(text),
            xy=(y, x),
            # xycoords=trans,
            annotation_clip=False
            # transform=axes.transAxes
        )


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
