import pandas as pd
import pytest
from barplots import barplots

def test_wrong_parameters():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case_1.csv", index_col=0)
    with pytest.raises(ValueError):
        barplots(
            df,
            ["dataset", "resource", "model"],
            orientation="pinco",
            path="{root}/{{feature}}.jpg".format(root=root)
        )

    with pytest.raises(ValueError):
        barplots(
            df,
            ["model"],
            path="{root}/{{feature}}.jpg".format(root=root),
            subplots=True
        )

    with pytest.raises(ValueError):
        barplots(
            df,
            ["model"],
            plots_per_row="pinco",
            path="{root}/{{feature}}.jpg".format(root=root),
            subplots=True
        )
