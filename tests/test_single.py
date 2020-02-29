import pandas as pd
from barplots import barplots


def test_single_index():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv")
    barplots(
        df,
        "cell_line",
        path="{root}/{{feature}}.png".format(root=root),
        verbose=False
    )

    # df.cell_line = list(range(len(df)))

    # barplots(
    #     df,
    #     df.cell_line,
    #     path="{root}/{{feature}}.png".format(root=root),
    #     verbose=False
    # )
