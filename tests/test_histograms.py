import pandas as pd
from barplots import barplots
import shutil
import itertools
from tqdm.auto import tqdm


def test_histograms():
    fuzzy_args = {
        "df": [
            pd.read_csv("tests/test_case.csv", index_col=0)
        ],
        "indices": [
            ["cell_line","task","model"]
        ],
        "show_legend": [
            True, False
        ],
        "orientation": [
            "horizontal", "vertical"
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
        "": "anything"
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
        
        path += "_{feature}.jpg"

        barplots(**kwargs, path=path, custom_defaults=custom_defaults)
