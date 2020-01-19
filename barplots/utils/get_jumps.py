import pandas as pd
from typing import Union, List, Any
from .is_last import is_last


def get_jumps(df: pd.DataFrame, row: int, index: Union[List, Any], old_index: Union[List, Any]) -> List[bool]:
    """Return list representing the detected jumps from given index and old_index.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to detect index jumps.
    row: int,
        Current row number.
    index:Union[List, Any],
        List of indices of index curresponding to given row number.
    old_index:Union[List, Any],
        Old index.

    Returns
    -------
    Returns list of boolean representing if for given index level a jump has been detected.
    """
    if not old_index:
        return [False]*len(index)

    previous = False
    jumps = []
    for new, old in zip(index, old_index):
        jumps.append(
            new != old or previous
        )
        previous = new != old
    return jumps
