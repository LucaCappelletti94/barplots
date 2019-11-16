import pandas as pd
import pytest
from histograms import histograms

def test_wrong_parameters():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    with pytest.raises(ValueError):
        histograms(
            df,
            ["dataset", "resource", "model"],
            orientation="pinco",
            path="{root}/{{feature}}.jpg".format(root=root)
        )

    with pytest.raises(ValueError):
        histograms(
            df,
            ["model"],
            path="{root}/{{feature}}.jpg".format(root=root),
            subplots=True
        )

    with pytest.raises(ValueError):
        histograms(
            df,
            ["model"],
            plots_per_row="pinco",
            path="{root}/{{feature}}.jpg".format(root=root),
            subplots=True
        )
