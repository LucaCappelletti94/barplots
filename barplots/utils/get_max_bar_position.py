"""Function to get the maximum bar position."""

import pandas as pd
from barplots.utils.bar_positions import bar_positions


def get_max_bar_position(
    df: pd.DataFrame, bar_width: float, space_width: float
) -> float:
    """Return maximum bar position.

    Parameters
    ----------
    df: pd.DataFrame,
        The dataframe from where to extract the data.
    bar_width: float,
        The width of the bars, used also for spacing.
    space_width: float,
            Width of spaces between spaces.
    """
    return (
        max(x for x, _, _, _ in bar_positions(df, bar_width, space_width))
        + bar_width / 2
    )
