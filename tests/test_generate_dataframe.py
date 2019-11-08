from .utils import generate_dataframe
import pandas as pd
from pandas.testing import assert_frame_equal
import os
import pytest

def test_generate_dataframe():
    with pytest.raises(ValueError):
        generate_dataframe(rows=-1)
    with pytest.raises(ValueError):
        generate_dataframe(indices=-1)
    with pytest.raises(ValueError):
        generate_dataframe(columns=-1)
    with pytest.raises(ValueError):
        generate_dataframe(random_seed=-1)
    with pytest.raises(ValueError):
        generate_dataframe(include_bools=-1)
    with pytest.raises(ValueError):
        generate_dataframe(include_strings=-1)
    with pytest.raises(ValueError):
        generate_dataframe(include_timestamps=-1)

    generate_dataframe()