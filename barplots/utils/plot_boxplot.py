from matplotlib.axis import Axis
import numpy as np


def plot_boxplot(
    axes: Axis,
    data: np.ndarray,
    x: float,
    y: float,
    boxplot_width: float,
    vertical: bool,
    **kwargs
):
    """Plot boxplot with given properties.

    Parameters
    ----------
    axes: Axes,
        Axes object where to plot the boxplot.
    x: float,
        Position for the left size of the boxplot.
    y: float,
        Height of the considered boxplot.
    boxplot_width: float,
        Width of the boxplot.
    vertical: bool,
        Whetever to build the axis to show the boxplots as vertical or as horizontal.
    """
    assert isinstance(x, float)
    assert isinstance(y, float)
    assert isinstance(data, np.ndarray)
    assert np.isfinite(data).all()
    assert isinstance(boxplot_width, float)
    assert isinstance(vertical, bool)

    if vertical:
        axes.boxplot(
            x=data,
            notch=True,
            positions=[x],
            widths=boxplot_width,
            capsize=7 * boxplot_width / 0.3,
            **kwargs
        )
    else:
        raise NotImplementedError("POI FAREMO")
        # axes.boxplot(
        #     y=x,
        #     notch=True,
        #     vert=False,
        #     positions=[x],
        #     widths=y,
        #     height=boxplot_width,
        #     **({"xerr": std} if std > min_std else {}),
        #     capsize=7 * boxplot_width / 0.3,
        #     **kwargs
        # )
