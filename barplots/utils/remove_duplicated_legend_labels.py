from matplotlib.axes import Axes
from sanitize_ml_labels import sanitize_ml_labels
from typing import Dict, List


def remove_duplicated_legend_labels(
    axes: Axes,
    legend_position: str,
    legend_title: str,
    custom_defaults: Dict[str, List[str]]
):
    """Remove duplicated labels from the plot legend.

    Parameters
    ----------
    axes: Axes
        Axes where to show the labels.
    legend_position: str
        Legend position.
    legend_title: str
        Title for the legend.
    custom_defaults: Dict[str, List[str]]
        The defaults for normalizing the provided keys.
    """
    handles, labels = axes.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    axes.legend(
        by_label.values(),
        sanitize_ml_labels(
            by_label.keys(),
            custom_defaults=custom_defaults
        ),
        title=sanitize_ml_labels(legend_title, custom_defaults=custom_defaults),
        loc=legend_position
    )
