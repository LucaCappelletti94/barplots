import pandas as pd
from .bar_positions import bar_positions
from typing import Tuple

def get_max_bar_lenght(
    df: pd.DataFrame,
    bar_width: float
) -> Tuple[float, float]:
    """Return Tuple containing maximum and minimum bar lenght, including std.

    These values could also be negative.

    Parameters
    ----------
    df: pd.DataFrame,
        The dataframe from where to extract the data.
    bar_width: float,
        The width of the bars, used also for spacing
    """
    return max(
        y+std for _, y, std, _ in bar_positions(df, bar_width)
    ), min(
        y-std for _, y, std, _ in bar_positions(df, bar_width)
    )
