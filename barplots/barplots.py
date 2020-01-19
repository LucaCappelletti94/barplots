import pandas as pd
from typing import List, Dict
from .barplot import barplot
from tqdm.auto import tqdm
from multiprocessing import Pool, cpu_count
from sanitize_ml_labels import sanitize_ml_labels


def _barplot(kwargs):
    barplot(**kwargs)


def barplots(
    df: pd.DataFrame,
    groupby: List,
    show_standard_deviation: bool = True,
    title: str = "{feature}",
    data_label: str = "{feature}",
    path: str = "barplots/{feature}.jpg",
    sanitize_metrics: bool = True,
    verbose: bool = True,
    **barplot_kwargs: Dict
):
    """
    Plot barplots corresponding to given dataframe,
    grouping by mean and if required also standard deviation.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to extrat data for plotting barplot.
    groupby: List,
        List of groupby over to run group by.
    show_standard_deviation:bool=True,
        Whetever to show or not the standard deviation. By default True.
    title: str = "{feature}",
        The title to use for the subgraphs.
        The `feature` placeholder is replaced with the considered column name.
    data_label: str = "{feature}",
        The label to use for the data axis.
        The `feature` placeholder is replaced with the considered column name.
    path: str = "barplots/{feature}.jpg",
        The path where to store the pictures.
        The `feature` placeholder is replaced with the considered column name.
    sanitize_metrics: bool = True,
        Whetever to automatically sanitize to standard name given features.
        For instance, "acc" to "Accuracy" or "lr" to "Learning rate"
    verbose:bool,
        Whetever to show or not the loading bar.
    barplot_kwargs:Dict,
        Kwargs parameters to pass to the barplot method.
        Read docstring for barplot method for more information on the available parameters.
    """
    groupby = df.groupby(groupby).agg(
        ("mean",)+(("std",) if show_standard_deviation else tuple())
    ).sort_index()

    tasks = [
        {
            "df": groupby[feature],
            "title":title.format(feature=feature.replace("_", " ")),
            "data_label":data_label.format(feature=feature.replace("_", " ")),
            "path":path.format(feature=feature),
            **barplot_kwargs
        } for feature in sanitize_ml_labels(groupby.columns.levels[0])
        if not pd.isna(groupby[feature]).any().any()
    ]

    if len(tasks) == 0:
        raise ValueError("No plottable feature found in given dataframe!")

    with Pool(min(len(tasks), cpu_count())) as p:
        list(tqdm(
            p.imap(_barplot, tasks),
            desc="Rendering barplots",
            total=len(tasks),
            dynamic_ncols=True,
            disable=not verbose
        ))
        p.close()
        p.join()
