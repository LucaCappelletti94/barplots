from humanize import naturaldelta
from matplotlib.axes import Axes


def humanize_time_ticks(axes: Axes, vertical: bool):
    if vertical:
        axes.set_yticklabels([
            naturaldelta(y) for y in axes.get_yticks()
        ])
    else:
        axes.set_xticklabels([
            naturaldelta(x) for x in axes.get_xticks()
        ])
