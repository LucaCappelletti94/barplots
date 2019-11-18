from matplotlib.axes import Axes
from matplotlib.figure import Figure
from .text_positions import text_positions
import pandas as pd
from typing import Dict, List
from .get_max_bar_position import get_max_bar_position
from sanitize_ml_labels import sanitize_ml_labels


def plot_bar_labels(
    axes: Axes,
    figure: Figure,
    df: pd.DataFrame,
    vertical: bool,
    levels: int,
    bar_width: float,
    minor_rotation: float,
    major_rotation: float,
    custom_defaults: Dict[str, List[str]]
):
    other_positions = set()
    width = get_max_bar_position(df, bar_width)
    for level in reversed(range(max(levels-2, 0), levels)):
        positions, labels = zip(*text_positions(df, bar_width, level))
        labels = sanitize_ml_labels(labels, custom_defaults=custom_defaults)
        positions = [
            round(pos, 5) for pos in positions
        ]
        positions = [
            position + width*0.0002 if position in other_positions else position
            for position in positions
        ]
        other_positions |= set(positions)
        minor = level == levels-1
        if vertical:
            axes.set_xticks(positions, minor=minor)
            labels = axes.set_xticklabels(labels, minor=minor, ha="center")
            if minor:
                axes.tick_params(
                    axis='x',
                    which='minor',
                    labelrotation=minor_rotation
                )
                axes.tick_params(
                    axis='x',
                    which='major',
                    direction='out',
                    length=max(
                        label.get_window_extent(
                            figure.canvas.get_renderer()).height
                        for label in labels
                    )/2,
                    width=0,
                    labelrotation=major_rotation
                )
        else:
            axes.set_yticks(positions, minor=minor)
            labels = axes.set_yticklabels(labels, minor=minor, va="center")
            if minor:
                axes.tick_params(
                    axis='y',
                    which='minor',
                    labelrotation=minor_rotation
                )
                axes.tick_params(
                    axis='y',
                    which='major',
                    direction='out',
                    length=max(
                        label.get_window_extent(
                            figure.canvas.get_renderer()).width
                        for label in labels
                    )/2,
                    width=0,
                    labelrotation=major_rotation
                )
