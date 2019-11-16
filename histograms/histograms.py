import pandas as pd
from typing import List, Dict
from .histogram import histogram
from tqdm.auto import tqdm
from multiprocessing import Pool, cpu_count


def _histogram(kwargs):
    histogram(**kwargs)


def histograms(
    df: pd.DataFrame,
    indices: List,
    show_standard_deviation: bool = True,
    title: str = "{feature}",
    data_label: str = "{feature}",
    path: str = "histograms/{feature}.jpg",
    verbose: bool = True,
    **histogram_kwargs: Dict
):
    """
    Plot histograms corresponding to given dataframe,
    grouping by mean and if required also standard deviation.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to extrat data for plotting histogram.
    indices: List,
        List of indices over to run group by.
    show_standard_deviation:bool=True,
        Whetever to show or not the standard deviation. By default True.
    title: str = "{feature}",
        The title to use for the subgraphs.
        The `feature` placeholder is replaced with the considered column name.
    data_label: str = "{feature}",
        The label to use for the data axis.
        The `feature` placeholder is replaced with the considered column name.
    path: str = "histograms/{feature}.jpg",
        The path where to store the pictures.
        The `feature` placeholder is replaced with the considered column name.
    histogram_kwargs:Dict,
        Kwargs parameters to pass to the histogram method.
        Read docstring for histogram method for more information on the available parameters.
    verbose:bool
    """
    groupby = df.groupby(indices).agg(
        ("mean",)+(("std",) if show_standard_deviation else tuple())
    ).sort_index()
    
    tasks = [
        {
            "df": groupby[feature],
            "title":title.format(feature=feature.replace("_", " ")),
            "data_label":data_label.format(feature=feature.replace("_", " ")),
            "path":path.format(feature=feature),
            **histogram_kwargs
        } for feature in groupby.columns.levels[0]
    ]
    with Pool(cpu_count()) as p:
        list(tqdm(
            p.imap(_histogram, tasks),
            desc="Rendering histograms",
            total=len(tasks),
            dynamic_ncols=True,
            disable=not verbose
        ))
        p.close()
        p.join()
