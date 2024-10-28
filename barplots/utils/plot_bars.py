"""Plot bars for given dataframe at given intervals."""

from typing import Dict, Optional
import pandas as pd
from matplotlib.axes import Axes
from barplots.utils.plot_bar import plot_bar
from barplots.utils.bar_positions import bar_positions
from barplots.utils.get_best_match import get_best_match


def plot_bars(
    axes: Axes,
    df: pd.DataFrame,
    bar_width: float,
    space_width: float,
    alphas: Dict[str, float],
    infer_alphas: bool,
    colors: Dict[str, str],
    infer_colors: bool,
    edgecolors: Optional[Dict[str, str]],
    infer_edgecolors: bool,
    hatch: Optional[Dict[str, str]],
    infer_hatch: bool,
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
    alphas: Dict[str, float],
        Dictionary of alphas to be used.
    infer_alphas: bool,
        Whetever to infer alphas or not.
    colors: Dict[str, str],
        Dictionary of colors to be used.
    infer_colors: bool,
        Whetever to infer colors or not.
    edgecolors: Optional[Dict[str, str]],
        Dictionary of edgecolors to be used.
    infer_edgecolors: bool,
        Whetever to infer edgecolors or not.
    hatch: Optional[Dict[str, str]]
        Dict of hatch, i.e. patterns for the bars, to be used for innermost index of dataframe.
    infer_hatch: bool,
        Whetever to infer hatch or not.
    kwargs: Dict,
        Parameters to be passed directly to the plot_bar method
    """
    for x, y, std, index in bar_positions(df, bar_width, space_width):
        plot_bar(
            axes=axes,
            x=x,
            y=y,
            std=std,
            bar_width=bar_width,
            alpha=(
                alphas[index[-1]]
                if index[-1] in alphas
<<<<<<< HEAD
                else (
                    get_best_match(alphas, (top_index, *index))
                    if infer_alphas
                    else None
                )
=======
                else get_best_match(alphas, (top_index, *index))
>>>>>>> 6fc1cff (Working on MyPy support)
            ),
            color=(
                colors[index[-1]]
                if index[-1] in colors
<<<<<<< HEAD
                else (
                    get_best_match(colors, (top_index, *index))
                    if infer_colors
                    else None
                )
            ),
            edgecolor=(
                None
                if edgecolors is None
                else (
                    edgecolors[index[-1]]
                    if index[-1] in edgecolors
                    else (
                        get_best_match(edgecolors, (top_index, *index))
                        if infer_edgecolors
                        else None
                    )
                )
=======
                else get_best_match(colors, (top_index, *index))
>>>>>>> 6fc1cff (Working on MyPy support)
            ),
            hatch=(
                None
                if hatch is None
                else (
                    hatch[index[-1]]
                    if index[-1] in hatch
<<<<<<< HEAD
                    else (
                        get_best_match(hatch, (top_index, *index))
                        if infer_hatch
                        else None
                    )
=======
                    else get_best_match(hatch, (top_index, *index))
>>>>>>> 6fc1cff (Working on MyPy support)
                )
            ),
            label=index[-1],
            **kwargs
        )
