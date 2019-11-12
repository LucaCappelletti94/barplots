import pandas as pd
from histograms import histograms
import pytest
import shutil


def test_horizontal_histograms():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    histograms(
        df,
        ["dataset", "resource", "model"],
        path="{root}/{{feature}}.jpg".format(root=root),
        orientation="horizontal"
    )
    shutil.rmtree(root)


def test_standard_histograms():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    histograms(df, ["dataset", "resource", "model"],
               path="{root}/{{feature}}.jpg".format(root=root))
    shutil.rmtree(root)


def test_single_index_histograms():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    histograms(df, ["dataset"],
               path="{root}/{{feature}}.jpg".format(root=root))
    shutil.rmtree(root)


def test_single_index_no_std_histograms():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    histograms(
        df,
        ["dataset"],
        show_standard_deviation=False,
        path="{root}/{{feature}}.jpg".format(root=root)
    )
    shutil.rmtree(root)


def test_wrong_orientation():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    with pytest.raises(ValueError):
        histograms(
            df,
            ["dataset", "resource", "model"],
            orientation="pinco",
            path="{root}/{{feature}}.jpg".format(root=root)
        )
