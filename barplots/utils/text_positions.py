import pandas as pd
from typing import Generator
from .is_last import is_last
from .get_jumps import get_jumps


def text_positions(df: pd.DataFrame, bar_width: float, index_level: int) -> Generator:
    labels_offsets = {}
    old_index = tuple()
    bar_position = 0
    for i, (index, _) in enumerate(df.iterrows()):
        if isinstance(index, str):
            index = (index,)
        try:
            iter(index)
        except TypeError:
            index = (index,)
        jumps = get_jumps(df, i, index, old_index)
        if not old_index:
            old_index = index
        old_bar_position = bar_position
        for j, value in enumerate(jumps):
            if value:
                text_position = old_bar_position
                if j in labels_offsets:
                    text_position += labels_offsets[j]
                if is_last(df, i):
                    if j != len(jumps)-1:
                        text_position += bar_width
                else:
                    bar_position += bar_width
                if j == index_level:
                    yield text_position/2 + bar_width/2, old_index[j]
        if j == index_level and j == len(jumps)-1 and is_last(df, i):
            yield text_position/2 + bar_width*1.5, index[j]
        old_index = index
        for j, value in enumerate(jumps):
            if value:
                labels_offsets[j] = bar_position
