"""Remove duplicated labels from the plot legend."""

from typing import Dict, List, Optional
import math
from matplotlib.axes import Axes
from matplotlib.patches import Patch
from sanitize_ml_labels import sanitize_ml_labels


def remove_duplicated_legend_labels(
    axes: Axes,
    legend_position: str,
    legend_title: str,
    legend_entries_size: float,
    legend_title_size: float,
    show_legend_title: bool,
    custom_defaults: Dict[str, List[str]],
    ncol: Optional[int] = None,
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
    legend_entries_size: float
        Size for the legend entries font.
    legend_title_size: float
        Size for the legend title font.
    show_legend_title: bool
        Whether to show the legend title.
    custom_defaults: Dict[str, List[str]]
        The defaults for normalizing the provided keys.
    ncol: Optional[int] = None
        The number of columns to show in the barplot.
    """
    handles, labels = axes.get_legend_handles_labels()

    by_label = dict(zip(labels, handles))
    length__of_padding = 6
    mean_label_length = (
        sum(len(label) for label in by_label.keys()) / len(by_label)
        + length__of_padding
    )

    ncol = math.ceil(len(legend_title) / mean_label_length) if ncol is None else ncol

    legend = axes.legend(
        handles=[
            Patch(
                linestyle="none",
                label=label,
                linewidth=legend_entries_size,
                facecolor=handler.patches[0].get_facecolor(),
                hatch=handler.patches[0].get_hatch(),
            )
            for handler, label in zip(
                by_label.values(),
                sanitize_ml_labels(by_label.keys(), custom_defaults=custom_defaults),
            )
        ],
        ncol=ncol,
        handletextpad=0.1,
        columnspacing=0.1,
        handlelength=0.7,
        prop={"size": legend_entries_size},
        loc=legend_position,
    )
    if show_legend_title:
        legend.set_title(
            sanitize_ml_labels(legend_title, custom_defaults=custom_defaults),
            prop={"weight": "bold", "size": legend_title_size},
        )
