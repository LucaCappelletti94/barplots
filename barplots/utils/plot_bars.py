import pandas as pd
from typing import Dict
from matplotlib.axes import Axes
from .plot_bar import plot_bar
from .bar_positions import bar_positions
import re


def get_best_match(mapping, index):
    compiled_keys = {
        key: (re.compile(key),) if isinstance(key, str) else [
            re.compile(k) for k in key
        ]
        for key in mapping
    }
    scores = {
        key: sum(
            len(match)
            for pattern in compiled_keys[key]
            for level in index
            for match in pattern.findall(level)
        )
        for key in mapping
    }
    return mapping[max(scores.keys(), key=(lambda key: scores[key]))]


def plot_bars(
    axes: Axes,
    df: pd.DataFrame,
    bar_width: float,
    space_width: float,
    alphas: Dict[str, float],
    colors: Dict[str, str],
    top_index: str,
    **kwargs: Dict
):
    """Plot bars for given dataframe at given intervals.

    Parameters
    ----------
    axes:Axes,
        The axes where to plot the bars.
    df: pd.DataFrame,
        The dataframe from where to extract the data.
    bar_width: float,
        The width of the bars, used also for spacing.
    space_width: float,
        Width of spaces between spaces.
    alphas:Dict[str, float],
        Dictionary of alphas to be used.
    colors:Dict[str, str],
        Dictionary of colors to be used.
    kwargs:Dict,
        Parameters to be passed directly to the plot_bar method
    """
    for x, y, std, index in bar_positions(df, bar_width, space_width):
        plot_bar(
            axes=axes,
            x=x,
            y=y,
            std=std,
            bar_width=bar_width,
            alpha=get_best_match(alphas, (top_index, *index)),
            color=get_best_match(colors, (top_index, *index)),
            label=index[-1],
            **kwargs
        )
