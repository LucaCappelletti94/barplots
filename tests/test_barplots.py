import pandas as pd
from barplots import barplots
import itertools
from tqdm.auto import tqdm


def test_barplots():
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
        "plots_per_row": [
            5, "auto"
        ],
        "unique_minor_labels": [
            True, False
        ],
        "show_standard_deviation": [
            True, False
        ],
        "unique_major_labels": [
            True, False
        ],
        "unique_data_label": [
            False, True
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

        if (kwargs["show_legend"] or not kwargs["subplots"]) and (kwargs["unique_data_label"] or kwargs["unique_minor_labels"] or kwargs["unique_major_labels"]):
            continue

        if kwargs["major_rotation"]:
            path += "_major_rotation"

        if kwargs["minor_rotation"]:
            path += "_minor_rotation"

        if kwargs["unique_minor_labels"]:
            path += "_unique_minor_labels"

        if kwargs["unique_major_labels"]:
            path += "_unique_major_labels"

        path += "_{feature}.jpg"

        barplots(**kwargs, path=path, custom_defaults=custom_defaults)


def test_single_index():
    root = "test_barplots"
    df = pd.read_csv("tests/test_case.csv")
    barplots(
        df,
        ["cell_line"],
        path="{root}/{{feature}}.jpg".format(root=root)
    )
