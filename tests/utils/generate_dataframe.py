import pandas as pd
import numpy as np


def generate_dataframe(
    rows: int = 100,
    columns: int = 10,
    indices: int = 3,
    include_timestamps: bool = True,
    include_strings: bool = True,
    include_bools: bool = True,
    random_seed: int = 42
) -> pd.DataFrame:
    """Return a random multi-index dataframe.

    Parameters
    --------------------------------
    rows: int = 100,
        Number of rows to generate.
    columns: int = 10,
        Number of columns to generate.
    indices: int = 3,
        Number of multi-index to generate.
    include_timestamps: bool = True,
        Whetever to include also columns including random timestamp.
    include_strings: bool = True,
        Whetever to include also columns including random strings.
    include_bools: bool = True,
        Whetever to include also columns including random booleans.
    random_seed: int = 42,
        Random seed to use for generating the values.

    Raises
    ---------------------------------
    ValueError,
        If rows is a non strictly positive integer.
    ValueError,
        If columns is a non strictly positive integer.
    ValueError,
        If indices is a non strictly positive integer.
    ValueError,
        If random_seed is a non strictly positive integer.
    ValueError,
        If include_timestamps is not a bool.
    ValueError,
        If include_strings is not a bool.
    ValueError,
        If include_bools is not a bool.

    Returns
    ---------------------------------
    The generated random dataframe.
    """
    ints = {
        "rows": rows,
        "columns": columns,
        "indices": indices,
        "random_seed": random_seed
    }
    for name, var in ints.items():
        if not isinstance(var, int) or var <= 0:
            raise ValueError("Given {name} is not a strictly positive integer".format(
                name=name
            ))

    np.random.seed(random_seed)

    bools = {
        "include_timestamps":include_timestamps,
        "include_strings":include_strings,
        "include_bools":include_bools
    }
    for name, var in bools.items():
        if not isinstance(var, bool):
            raise ValueError("Given {name} is not a bool".format(
                name=name
            ))
    cols = columns + indices - sum(bools.values())
    features = [
        "Feature {i}".format(i=i)
        for i in range(cols)
    ]
    df = pd.DataFrame(
        np.random.randint(0, 5, size=(rows, cols)),
        columns=features
    ).set_index(features[:indices])
    if include_timestamps:
        df["Time feature"] = np.random.randint(0, 10000000, size=rows)
    if include_strings:
        df["String feature"] = "This is a totally random string."
    if include_bools:
        df["Bool feature"] = np.random.randint(
            0, 10000000, size=rows).astype(bool)
    return df
