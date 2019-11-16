from matplotlib.figure import Figure
from matplotlib.axes import Axes


def remove_duplicated_legend_labels(axes: Axes, legend_position: str):
    """Remove duplicated labels from the plot legend.

    Parameters
    ----------
    axes: Axes,
        Axes where to show the labels.
    legend_position: str,
        Legend position.
    """
    handles, labels = axes.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    axes.legend(by_label.values(), by_label.keys(), loc=legend_position)