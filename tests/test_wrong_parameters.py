import pandas as pd
import pytest
from barplots import barplots

def test_wrong_parameters():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv")
    
    with pytest.raises(ValueError):
        barplots(
            df[df.cell_line == "CIAO"],
            ["cell_line","task","balancing","model"],
            orientation="pinco",
            path="{root}/{{feature}}.jpg".format(root=root)
        )

    with pytest.raises(ValueError):
        barplots(
            df,
            ["cell_line","task","balancing","model"],
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
