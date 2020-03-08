import pandas as pd
from typing import List, Any
from pandas import MultiIndex


def get_levels(df: pd.DataFrame) -> List[List[Any]]:
    """Return normalized list of dataframe index levels.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to extract index levels.

    Returns
    -------
    List of lists of unique indices.
    """
    if isinstance(df.index, MultiIndex):
        return [
            list(e) for e in df.index.levels
        ]
    else:
        return [df.index.unique().tolist()]
