"""Submodule with utilities for plotting barplots."""
from .save_picture import save_picture
from .get_axes import get_axes
from .text_positions import text_positions
from .plot_bars import plot_bars
from .get_levels import get_levels
from .remove_duplicated_legend_labels import remove_duplicated_legend_labels
from .plot_bar_labels import plot_bar_labels
from .get_max_bar_length import get_max_bar_length


__all__ = [
    "save_picture",
    "get_axes",
    "text_positions",
    "plot_bars",
    "get_levels",
    "remove_duplicated_legend_labels",
    "plot_bar_labels",
    "get_max_bar_length"
]