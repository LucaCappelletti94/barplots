import pandas as pd
from histograms import histograms
import pytest
import shutil


def test_horizontal_histograms():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    histograms(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}.jpg".format(root=root),
        orientation="horizontal",
        show_bar_labels=True,
        legend_position=None
    )
    #shutil.rmtree(root)