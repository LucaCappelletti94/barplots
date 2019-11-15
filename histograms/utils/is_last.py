import pandas as pd


def is_last(df: pd.DataFrame, row: int) -> bool:
    """Return boolean representing if given row is the last row.

    Parameters
    ----------
    df: pd.DataFrame,
        The dataframe to check against.
    row: int,
        The index of the row to consider.

    Returns
    -------
    A boolean representing if given row is the last one.
    """
    return row+1 == df.shape[0]
