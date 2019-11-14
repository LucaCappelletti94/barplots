import pandas as pd
from .utils import plot_bar, sanitize_name, bar_positions
from typing import Dict
from matplotlib.axes import Axes

def plot_bars(
    axes:Axes, 
    df: pd.DataFrame,
    bar_width: float,
    alphas:Dict[str, float],
    colors:Dict[str, str],
    **kwargs:Dict
):
    """Plot bars for given dataframe at given intervals.
    
    Parameters
    ----------
    axes:Axes,
        The axes where to plot the bars.
    df: pd.DataFrame,
        The dataframe from where to extract the data.
    bar_width: float,
        The width of the bars, used also for spacing
    alphas:Dict[str, float],
        Dictionary of alphas to be used.
    colors:Dict[str, str],
        Dictionary of colors to be used.
    kwargs:Dict,
        Parameters to be passed directly to the plot_bar method
    """
    for x, y, std, label, index in bar_positions(df, bar_width):
        plot_bar(
            axes=axes,
            x=x,
            y=y,
            std=std,
            bar_width=bar_width,
            alpha=alphas[index],
            color=colors[index],
            label=label,
            **kwargs
        )
