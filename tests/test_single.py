import pandas as pd
from barplots import barplots
import matplotlib.pyplot as plt


def test_single_index():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv")
    barplots(
        df, "cell_line", path="{root}/{{feature}}.png".format(root=root), verbose=False
    )
    plt.close()
