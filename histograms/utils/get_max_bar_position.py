import pandas as pd
from .bar_positions import bar_positions


def get_max_bar_position(
    df: pd.DataFrame,
    bar_width: float
) -> float:
    """Return maximum bar size, including std.

    Parameters
    ----------
    df: pd.DataFrame,
        The dataframe from where to extract the data.
    bar_width: float,
        The width of the bars, used also for spacing
    """
    return max(
        x for x, _, _, _, _ in bar_positions(df, bar_width)
    ) + bar_width/2
