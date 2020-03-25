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
    path: str = "barplots/{feature}.png",
    sanitize_metrics: bool = True,
    use_multiprocessing: bool = True,
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
    path: str = "barplots/{feature}.png",
        The path where to store the pictures.
        The `feature` placeholder is replaced with the considered column name.
    sanitize_metrics: bool = True,
        Whetever to automatically sanitize to standard name given features.
        For instance, "acc" to "Accuracy" or "lr" to "Learning rate"
    use_multiprocessing: bool = True,
        Whetever to use or not multiple processes.
    verbose:bool,
        Whetever to show or not the loading bar.
    barplot_kwargs:Dict,
        Kwargs parameters to pass to the barplot method.
        Read docstring for barplot method for more information on the available parameters.
    """
    groupby = df.groupby(groupby).agg(
        ("mean",)+(("std",) if show_standard_deviation else tuple())
    ).sort_index()

    features = original = groupby.columns.levels[0]
    if sanitize_metrics:
        features = sanitize_ml_labels(features)

    tasks = [
        {
            "df": groupby[original],
            "title":title.format(feature=feature.replace("_", " ")),
            "data_label":data_label.format(feature=feature.replace("_", " ")),
            "path":path.format(feature=feature).replace(" ", "_").lower(),
            **barplot_kwargs
        } for original, feature in zip(original, features)
        if not pd.isna(groupby[original]).any().any() and not len(groupby[original]) == 0
    ]

    if len(tasks) == 0:
        raise ValueError("No plottable feature found in given dataframe!")
    
    use_multiprocessing = use_multiprocessing and not len(tasks) == 1

    if use_multiprocessing: 
        with Pool(min(len(tasks), cpu_count())) as p:
            try:
                list(tqdm(
                    p.imap(_barplot, tasks),
                    desc="Rendering barplots",
                    total=len(tasks),
                    dynamic_ncols=True,
                    disable=not verbose
                ))
                p.close()
                p.join()
            except Exception as e:
                p.close()
                p.join()
                raise e
    else:
        for task in tqdm(tasks,
            desc="Rendering barplots",
            total=len(tasks),
            dynamic_ncols=True,
            disable=not verbose
        ):
            barplot(**task)