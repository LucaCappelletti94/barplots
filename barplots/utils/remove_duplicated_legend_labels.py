from matplotlib.axes import Axes
from sanitize_ml_labels import sanitize_ml_labels
from typing import Dict, List, Optional
import math
from matplotlib.patches import FancyBboxPatch


def remove_duplicated_legend_labels(
    axes: Axes,
    legend_position: str,
    legend_title: str,
    legend_marker_style: str,
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
    legend_marker_style: str
        Marker style to use for the legend.
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
    mean_label_length = sum(
        len(label) for label in by_label.keys()
    ) / len(by_label) + length__of_padding

    ncol = math.ceil(len(legend_title) /
                     mean_label_length) if ncol is None else ncol

    legend = axes.legend(
        handles=[
            FancyBboxPatch(
                (0, 0),
                width=legend_entries_size,
                height=legend_entries_size,
                linestyle='none',
                label=label,
                capstyle="round",
                boxstyle="round,pad=-0.0040,rounding_size=0.015",
                ec="none",
                mutation_aspect=4,
                facecolor=handler.patches[0].get_facecolor(),
                hatch=handler.patches[0].get_hatch(),
            )
            for handler, label in zip(
                by_label.values(),
                sanitize_ml_labels(
                    by_label.keys(),
                    custom_defaults=custom_defaults
                )
            )
        ],
        ncol=ncol,
        handletextpad=0,
        columnspacing=0,
        prop={'size': legend_entries_size},
        loc=legend_position
    )
    if show_legend_title:
        legend.set_title(
            sanitize_ml_labels(legend_title, custom_defaults=custom_defaults),
            prop=dict(weight='bold', size=legend_title_size)
        )
