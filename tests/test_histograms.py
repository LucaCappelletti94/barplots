import pandas as pd
from barplots import barplots
import itertools
from tqdm.auto import tqdm


def test_histograms():
    fuzzy_args = {
        "df": [
            pd.read_csv("tests/test_case.csv")
        ],
        "groupby": [
            ["cell_line", "task", "model"]
        ],
        "show_legend": [
            True, False
        ],
        "orientation": [
            "horizontal", "vertical"
        ],
        "major_rotation": [
            0, 90
        ],
        "minor_rotation": [
            0, 90
        ],
        "subplots": [
            True, False
        ]
    }

    custom_defaults = {
        "P": "promoters",
        "E": "enhancers",
        "A": "active ",
        "I": "inactive ",
        "+": " and ",
        "": "anything",
        "Validation": "val"
    }

    arguments = list(itertools.product(*list(fuzzy_args.values())))
    for arg in tqdm(arguments):
        kwargs = dict(zip(fuzzy_args.keys(), arg))
        path = "examples/{orientation}".format(
            orientation=kwargs["orientation"]
        )

        if kwargs["show_legend"]:
            path += "_legend"

        if kwargs["subplots"]:
            path += "_subplots"
        else:
            kwargs["groupby"] = kwargs["groupby"][1:]

        if kwargs["show_legend"] and kwargs["major_rotation"]:
            continue

        if kwargs["show_legend"] and kwargs["orientation"] == "horizontal" and not kwargs["minor_rotation"]:
            continue

        if kwargs["show_legend"] and kwargs["orientation"] == "vertical" and kwargs["minor_rotation"]:
            continue

        if not kwargs["show_legend"] and kwargs["orientation"] == "vertical" and not kwargs["minor_rotation"]:
            continue

        if not kwargs["show_legend"] and kwargs["orientation"] == "horizontal" and kwargs["minor_rotation"]:
            continue

        if not kwargs["show_legend"] and kwargs["orientation"] == "vertical" and kwargs["major_rotation"]:
            continue

        if not (kwargs["minor_rotation"] or kwargs["major_rotation"]) and kwargs["orientation"] == "horizontal":
            continue

        if kwargs["major_rotation"]:
            path += "_major_rotation"

        if kwargs["minor_rotation"]:
            path += "_minor_rotation"

        path += "_{feature}.jpg"

        barplots(**kwargs, path=path, custom_defaults=custom_defaults)
