from typing import Union, List, Any


def get_jumps(index: Union[List, Any], old_index: Union[List, Any]) -> List[bool]:
    """Return list representing the detected jumps from given index and old_index.

    Parameters
    ----------
    index:Union[List, Any],
        List of indices of index curresponding to given row number.
    old_index:Union[List, Any],
        Old index.

    Returns
    -------
    Returns list of boolean representing if for given index level a jump has been detected.
    """
    if not old_index:
        return [False] * len(index)

    previous = False
    jumps = []
    for new, old in zip(index, old_index):
        jumps.append(new != old or previous)
        previous = new != old
    return jumps
