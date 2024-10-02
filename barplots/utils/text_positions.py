from typing import Generator
import pandas as pd
from barplots.utils.get_jumps import get_jumps
from barplots.utils.bar_positions import bar_positions


def text_positions(
    df: pd.DataFrame, bar_width: float, space_width: float, index_level: int
) -> Generator:
    positions = bar_positions(df, bar_width, space_width)
    old_index = None
    previous_jump_position = 0
    last_position = 0

    for (index, _), position in zip(df.iterrows(), positions):
        if not isinstance(index, (list, tuple)):
            index = (index,)
        jumps = get_jumps(index, old_index)
        if jumps[index_level] and old_index is not None:
            yield (previous_jump_position + last_position) / 2, old_index[index_level]
            previous_jump_position = position[0] - bar_width / 2

        last_position = position[0] + bar_width / 2
        old_index = index
    yield (previous_jump_position + last_position) / 2, old_index[index_level]
