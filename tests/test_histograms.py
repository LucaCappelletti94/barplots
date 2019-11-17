import pandas as pd
from barplots import barplots
import shutil


def test_horizontal_barplots():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case_1.csv", index_col=0)
    barplots(
        df,
        ["dataset", "resource", "model"],
        path="{root}/{{feature}}.jpg".format(root=root),
        orientation="horizontal"
    )
    shutil.rmtree(root)


def test_standard_barplots():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case_1.csv", index_col=0)
    barplots(df, ["dataset", "resource", "model"],
               path="{root}/{{feature}}.jpg".format(root=root))
    shutil.rmtree(root)


def test_single_index_barplots():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case_1.csv", index_col=0)
    barplots(df, ["dataset"],
               path="{root}/{{feature}}.jpg".format(root=root))
    shutil.rmtree(root)


def test_single_index_no_std_barplots():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case_1.csv", index_col=0)
    barplots(
        df,
        ["dataset"],
        show_standard_deviation=False,
        path="{root}/{{feature}}.jpg".format(root=root)
    )
    shutil.rmtree(root)


