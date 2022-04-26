import pandas as pd
from .bar_positions import bar_positions
from typing import Tuple

def get_max_bar_length(
    df: pd.DataFrame,
    bar_width: float,
    space_width: float
) -> Tuple[float, float]:
    """Return Tuple containing maximum and minimum bar length, including std.

    These values could also be negative.

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe from where to extract the data.
    bar_width: float
        The width of the bars, used also for spacing
    space_width: float
        Width of spaces between spaces.
    """
    return max(
        y+std for _, y, std, _ in bar_positions(df, bar_width, space_width)
    ), min(
        y-std for _, y, std, _ in bar_positions(df, bar_width, space_width)
    )
