import pandas as pd
from typing import Dict
from matplotlib.axes import Axes
from .plot_bar import plot_bar
from .bar_positions import bar_positions
from .get_best_match import get_best_match


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
            alpha=alphas[index[-1]],#get_best_match(alphas, (top_index, *index)),
            color=colors[index[-1]],#get_best_match(colors, (top_index, *index)),
            label=index[-1],
            **kwargs
        )
