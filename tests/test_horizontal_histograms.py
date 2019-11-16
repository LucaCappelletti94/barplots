import pandas as pd
from histograms import histograms
import pytest
import shutil


def test_horizontal_histograms_with_legend():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    histograms(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_horizontal_with_legend.jpg".format(root=root),
        orientation="horizontal",
        show_legend=True
    )
    # shutil.rmtree(root)


def test_horizontal_histograms_without_legend():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    histograms(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_horizontal_without_legend.jpg".format(
            root=root),
        orientation="horizontal",
        show_legend=False
    )
    # shutil.rmtree(root)


def test_vertical_histograms_with_legend():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    histograms(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_vertical_with_legend.jpg".format(root=root),
        orientation="vertical",
        show_legend=True
    )
    # shutil.rmtree(root)


def test_vertical_histograms_without_legend():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    histograms(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_vertical_without_legend.jpg".format(
            root=root),
        orientation="vertical",
        show_legend=False
    )
    # shutil.rmtree(root)


def test_multiple_histograms_vertical():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    histograms(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_multiple_vertical_without_legend.jpg".format(
            root=root),
        orientation="vertical",
        show_legend=False,
        split_plots=True
    )
    # shutil.rmtree(root)

def test_multiple_histograms_horizontal():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    histograms(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_multiple_horizontal_without_legend.jpg".format(
            root=root),
        orientation="horizontal",
        show_legend=False,
        split_plots=True
    )
    # shutil.rmtree(root)

def test_multiple_histograms_vertical_with_legend():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    histograms(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_multiple_vertical_with_legend.jpg".format(
            root=root),
        orientation="vertical",
        show_legend=True,
        split_plots=True
    )
    # shutil.rmtree(root)

def test_multiple_histograms_horizontal_with_legend():
    root = "test_histograms"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    histograms(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_multiple_horizontal_with_legend.jpg".format(
            root=root),
        orientation="horizontal",
        show_legend=True,
        split_plots=True
    )
    # shutil.rmtree(root)
