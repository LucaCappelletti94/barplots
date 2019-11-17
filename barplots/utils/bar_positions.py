from typing import Generator
import pandas as pd
from .is_last import is_last
from .get_jumps import get_jumps


def bar_positions(df: pd.DataFrame, bar_width: float) -> Generator:
    """Returns a generator of bar positions.
        df: pd.DataFrame,
            Dataframe to iterate to extract the necessary data.
        bar_width:float,
            Width of any given bar.
    """
    old_index = tuple()
    bar_position = 0
    for i, (index, values) in enumerate(df.iterrows()):
        if not isinstance(index, (list, tuple)):
            index = (index,)

        if not is_last(df, i):
            bar_position += bar_width * sum(
                get_jumps(df, i, index, old_index)
            )
        else:
            bar_position += bar_width
        old_index = index

        if len(values) == 2:
            y, std = values
        elif len(values) == 1:
            y, std = values.values[0], 0

        yield (
            bar_position + bar_width / 2,
            y,
            std,
            index[-1]
        )