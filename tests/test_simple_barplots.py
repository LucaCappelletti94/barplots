import pandas as pd
from barplots import barplots
import matplotlib.pyplot as plt


def test_simple_barplots():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv")

    custom_defaults = {
        "P": "promoters",
        "E": "enhancers",
        "A": "active ",
        "I": "inactive ",
        "+": " and ",
        "": "anything",
        "Validation": "val",
    }

    barplots(
        df,
        ["cell_line", "task", "model"],
        path="{root}/{{feature}}.png".format(root=root),
        orientation="horizontal",
        verbose=False,
        custom_defaults=custom_defaults,
        subplots=True,
        space_width=1,
    )
    plt.close()
