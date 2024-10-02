from barplots.utils.bar_positions import bar_positions
import pandas as pd


def execute_test(df, ground_truth):
    df = df.groupby(["cell_line", "task", "balancing", "model"]).mean()

    for x1, x2 in zip(ground_truth, bar_positions(df, 0.5, 0.5)):
        assert x1 == x2[0]


def test_bar_positions():
    df1 = pd.read_csv("tests/test_case.csv")
    df1 = df1[df1.cell_line == "HelaS3"]
    df1 = df1[df1.balancing == "unbalanced"]
    df2 = df1[df1.model.str.contains("bayesian").values]
    df3 = df2[df2.model.str.contains("mlp").values]

    execute_test(
        df1,
        [
            0.25,
            0.75,
            1.25,
            1.75,
            3.25,
            3.75,
            4.25,
            4.75,
            6.25,
            6.75,
            7.25,
            7.75,
            9.25,
            9.75,
            10.25,
            10.75,
            12.25,
            12.75,
            13.25,
            13.75,
        ],
    )
    execute_test(df2, [0.25, 0.75, 2.25, 2.75, 4.25, 4.75, 6.25, 6.75, 8.25, 8.75])
    execute_test(df3, [0.25, 1.25, 2.25, 3.25, 4.25])
