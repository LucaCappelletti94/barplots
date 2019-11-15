from .bar_positions import bar_positions
import pandas as pd


def get_max_bar_lenght(
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
        y + std for _, y, std, _, _ in bar_positions(df, bar_width)
    )
