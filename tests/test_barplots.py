import pandas as pd
from barplots import barplots
import os
import itertools
from tqdm.auto import tqdm
import matplotlib.pyplot as plt


def test_barplots():
    df1 = pd.read_csv("tests/test_case.csv")
    df2 = df1[df1.model.str.contains("bayesian")]
    fuzzy_args = {
        "df": [(1, df1), (2, df2)],
        "groupby": [["cell_line", "task", "model"]],
        "show_legend": [True, False],
        "orientation": ["horizontal", "vertical"],
        "major_rotation": [0, 90],
        "minor_rotation": [0, 90],
        "plots_per_row": [3, "auto"],
        "unique_minor_labels": [True, False],
        "unique_major_labels": [True, False],
        "unique_data_label": [False, True],
        "subplots": [True, False],
    }

    custom_defaults = {
        "P": "promoters",
        "E": "enhancers",
        "A": "active ",
        "I": "inactive ",
        "+": " and ",
        "": "anything",
        "Validation": "val",
    }

    arguments = list(itertools.product(*list(fuzzy_args.values())))
    for arg in tqdm(arguments, desc="Running test suite"):
        kwargs = dict(zip(fuzzy_args.keys(), arg))
        path = "examples/{i}/{orientation}".format(
            i=kwargs["df"][0], orientation=kwargs["orientation"]
        )

        os.makedirs(os.path.dirname(path), exist_ok=True)

        if kwargs["show_legend"]:
            path += "_legend"

        if kwargs["subplots"]:
            path += "_subplots"
        else:
            kwargs["groupby"] = kwargs["groupby"][1:]

        if kwargs["show_legend"] and kwargs["major_rotation"]:
            continue

        if (
            kwargs["show_legend"]
            and kwargs["orientation"] == "horizontal"
            and not kwargs["minor_rotation"]
        ):
            continue

        if (
            kwargs["show_legend"]
            and kwargs["orientation"] == "vertical"
            and kwargs["minor_rotation"]
        ):
            continue

        if (
            not kwargs["show_legend"]
            and kwargs["orientation"] == "vertical"
            and not kwargs["minor_rotation"]
        ):
            continue

        if (
            not kwargs["show_legend"]
            and kwargs["orientation"] == "horizontal"
            and kwargs["minor_rotation"]
        ):
            continue

        if (
            not kwargs["show_legend"]
            and kwargs["orientation"] == "vertical"
            and kwargs["major_rotation"]
        ):
            continue

        if (
            not (kwargs["minor_rotation"] or kwargs["major_rotation"])
            and kwargs["orientation"] == "horizontal"
        ):
            continue

        if (kwargs["show_legend"] or not kwargs["subplots"]) and (
            kwargs["unique_data_label"]
            or kwargs["unique_minor_labels"]
            or kwargs["unique_major_labels"]
        ):
            continue

        if kwargs["major_rotation"]:
            path += "_major_rotation"

        if kwargs["minor_rotation"]:
            path += "_minor_rotation"

        if kwargs["unique_minor_labels"]:
            path += "_unique_minor_labels"

        if kwargs["unique_major_labels"]:
            path += "_unique_major_labels"

        path += "_{feature}.png"

        kwargs["df"] = kwargs["df"][1]

        barplots(**kwargs, path=path, custom_defaults=custom_defaults, verbose=False)
        plt.close()


def test_single_index():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv")
    barplots(
        df,
        ["cell_line"],
        path="{root}/{{feature}}.png".format(root=root),
        verbose=False,
    )
    plt.close()
