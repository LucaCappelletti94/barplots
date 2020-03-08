from barplots.utils.text_positions import text_positions
from barplots import barplot
import pandas as pd


def test_text_positions():
    df1 = pd.read_csv("tests/test_case.csv")
    df1 = df1[df1.cell_line == "HelaS3"]
    df1 = df1[df1.balancing == "unbalanced"]
    df2 = df1[df1.model.str.contains("bayesian").values]
    df3 = df2[df2.model.str.contains("mlp").values]

    # execute_test(df1, [0.25, 0.75, 1.25, 1.75, 3.25, 3.75, 4.25, 4.75, 6.25,
    #                    6.75, 7.25, 7.75, 9.25, 9.75, 10.25, 10.75, 12.25, 12.75, 13.25, 13.75])
    # execute_test(df2, [0.25, 0.75, 2.25, 2.75, 4.25,
    #                    4.75, 6.25, 6.75, 8.25, 8.75])
    # execute_test(df3, [0.25, 1.25, 2.25, 3.25, 4.25])

    custom_defaults = {
        "P": "promoters",
        "E": "enhancers",
        "A": "active ",
        "I": "inactive ",
        "+": " and ",
        "": "anything",
        "Validation": "val",
        "Un": "unbalanced"
    }

    df1 = df1.groupby(["cell_line", "task", "balancing", "model"]).mean()
    df2 = df2.groupby(["cell_line", "task", "balancing", "model"]).mean()
    df3 = df3.groupby(["cell_line", "task", "balancing", "model"]).mean()

    # print(list(text_positions(df3, 0.5, 2)))
    barplot(df1, 0.5, height=4, path="test1.png", custom_defaults=custom_defaults, show_legend=False)
    barplot(df2, 0.5, height=4, path="test2.png", custom_defaults=custom_defaults)
    barplot(df3, 0.5, height=4, path="test3.png", custom_defaults=custom_defaults)