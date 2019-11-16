import pandas as pd
from barplots import barplots
import pytest
import shutil


def test_horizontal_barplots_with_legend():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    barplots(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_horizontal_with_legend.jpg".format(root=root),
        orientation="horizontal",
        show_legend=True
    )
    # shutil.rmtree(root)


def test_horizontal_barplots_without_legend():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    barplots(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_horizontal_without_legend.jpg".format(
            root=root),
        orientation="horizontal",
        show_legend=False
    )
    # shutil.rmtree(root)


def test_vertical_barplots_with_legend():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    barplots(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_vertical_with_legend.jpg".format(root=root),
        orientation="vertical",
        show_legend=True
    )
    # shutil.rmtree(root)


def test_vertical_barplots_without_legend():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    barplots(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_vertical_without_legend.jpg".format(
            root=root),
        orientation="vertical",
        show_legend=False
    )
    # shutil.rmtree(root)


def test_multiple_barplots_vertical():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    barplots(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_multiple_vertical_without_legend.jpg".format(
            root=root),
        orientation="vertical",
        show_legend=False,
        subplots=True
    )
    # shutil.rmtree(root)

def test_multiple_barplots_horizontal():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    barplots(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_multiple_horizontal_without_legend.jpg".format(
            root=root),
        orientation="horizontal",
        show_legend=False,
        subplots=True
    )
    # shutil.rmtree(root)

def test_multiple_barplots_vertical_with_legend():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    barplots(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_multiple_vertical_with_legend.jpg".format(
            root=root),
        orientation="vertical",
        show_legend=True,
        subplots=True
    )
    # shutil.rmtree(root)

def test_multiple_barplots_horizontal_with_legend():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    index = ["dataset", "resource", "model"]
    barplots(
        df[index+["test_auroc"]],
        index,
        path="{root}/{{feature}}_multiple_horizontal_with_legend.jpg".format(
            root=root),
        orientation="horizontal",
        show_legend=True,
        subplots=True
    )
    # shutil.rmtree(root)
