# import pandas as pd
# from matplotlib.axes import Axes
# from .get_bars_ticks_labels import get_bars_ticks_labels

# def add_bars_ticks_labels(
#     axes:Axes,
#     df:pd.DataFrame,
#     bar_width:float,
#     vertical:bool
# ):
#     """Draw bar tiks labels from given dataframe."""
#     positions, labels = get_bars_ticks_labels(df, bar_width)
#     if vertical:
#         axes.set_xticks(positions)
#         axes.set_xticklabels(labels)
#     else:
#         axes.set_yticks(positions)
#         axes.set_yticklabels(labels)
#         axes.set_yticks([0.5], minor=True)
#         axes.set_yticklabels(["KEBAB"], minor=True)

#         axes.tick_params(axis='y', which='minor', direction='out', length=100, width=0)
#         axes.tick_params(axis='y', which='major', bottom='off', top='off')