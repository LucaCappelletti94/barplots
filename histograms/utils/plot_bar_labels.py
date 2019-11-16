from matplotlib.axes import Axes
from matplotlib.figure import Figure
from .text_positions import text_positions
import pandas as pd


def plot_bar_labels(axes:Axes, figure:Figure, df:pd.DataFrame, vertical:bool, levels:int, bar_width:float):
    other_positions = set()
    for level in reversed(range(max(levels-2, 0), levels)):
        positions, labels = zip(*text_positions(df, bar_width, level))
        positions = [
            round(pos, 5) for pos in positions
        ]
        positions = [
            position + 0.00014 if position in other_positions else position
            for position in positions
        ]
        other_positions |= set(positions)
        minor = level == levels-1
        if vertical:
            axes.set_xticks(positions, minor=minor)
            labels = axes.set_xticklabels(labels, minor=minor)
            if minor:
                axes.tick_params(
                    axis='x',
                    which='major',
                    direction='out',
                    length=max(
                        label.get_window_extent(figure.canvas.get_renderer()).height
                        for label in labels
                    )/2,
                    width=0
                )
        else:
            axes.set_yticks(positions, minor=minor)
            labels = axes.set_yticklabels(labels, minor=minor)
            if minor:
                axes.tick_params(
                    axis='y',
                    which='major',
                    direction='out',
                    length=max(
                        label.get_window_extent(figure.canvas.get_renderer()).width
                        for label in labels
                    )/2,
                    width=0
                )
