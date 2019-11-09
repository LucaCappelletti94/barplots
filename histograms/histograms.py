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
    y_label: str = "{feature}",
    path: str = "histograms/{feature}.jpg",
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
    histogram_kwargs:Dict,
        Kwargs parameters to pass to the histogram method.
    """
    groupby = df.groupby(indices).agg(
        ("mean",)+(("std",) if show_standard_deviation else tuple())
    ).sort_index()
    tasks = [
        {
            "df": groupby[feature],
            "title":title.format(feature=feature.replace("_", " ")),
            "y_label":title.format(feature=feature.replace("_", " ")),
            "path":path.format(feature=feature),
            **histogram_kwargs
        } for feature in groupby.columns.levels[0]
    ]
    with Pool(cpu_count()) as p:
        list(tqdm(
            p.imap(_histogram, tasks),
            desc="Rendering histograms",
            total=len(tasks),
            dynamic_ncols=True
        ))
        p.close()
        p.join()
