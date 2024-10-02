"""Utility dispatch function to plot bar with given properties."""

from matplotlib.axes import Axes


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
            height=y,
            width=bar_width,
            **({"yerr": std} if std > min_std else {}),
            capsize=7 * bar_width / 0.3,
            **kwargs
        )
    else:
        axes.barh(
            y=x,
            width=y,
            height=bar_width,
            **({"xerr": std} if std > min_std else {}),
            capsize=7 * bar_width / 0.3,
            **kwargs
        )
