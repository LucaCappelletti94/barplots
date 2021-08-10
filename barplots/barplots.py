"""Module implementing plotting of multiple barplots in parallel and sequential manner."""
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Tuple, Callable, Union

import pandas as pd
from sanitize_ml_labels import sanitize_ml_labels
from tqdm.auto import tqdm
from matplotlib.figure import Figure
from matplotlib.axis import Axis

from .barplot import barplot


def _barplot(kwargs: Dict) -> Tuple[Figure, Axis]:
    """Wrapper over barplot call to expand given kwargs."""
    return barplot(**kwargs)


def barplots(
    df: pd.DataFrame,
    groupby: List = None,
    show_standard_deviation: bool = True,
    title: str = "{feature}",
    data_label: str = "{feature}",
    path: str = "barplots/{feature}.png",
    sanitize_metrics: bool = True,
    letters: Dict[str, str] = None,
    bar_width: float = 0.3,
    space_width: float = 0.3,
    height: float = None,
    dpi: int = 200,
    min_std: float = 0,
    min_value: float = None,
    max_value: float = None,
    show_legend: bool = True,
    show_title: str = True,
    legend_position: str = "best",
    colors: Dict[str, str] = None,
    alphas: Dict[str, float] = None,
    facecolors: Dict[str, str] = None,
    orientation: str = "vertical",
    subplots: bool = False,
    plots_per_row: Union[int, str] = "auto",
    minor_rotation: float = 0,
    major_rotation: float = 0,
    unique_minor_labels: bool = False,
    unique_major_labels: bool = True,
    unique_data_label: bool = True,
    auto_normalize_metrics: bool = True,
    placeholder: bool = False,
    scale: str = "linear",
    custom_defaults: Dict[str, List[str]] = None,
    sort_subplots: Callable[[List], List] = None,
    sort_bars: Callable[[pd.DataFrame], pd.DataFrame] = None,
    use_multiprocessing: bool = True,
    verbose: bool = True,
) -> Tuple[List[Figure], List[Axis]]:
    """Returns list of the built figures and axes.

    Plot barplots corresponding to given dataframe,
    grouping by mean and if required also standard deviation.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to extrat data for plotting barplot.
    groupby: List = None,
        List of groupby over to run group by.
        If groupby was previously executed, leave this as None.
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
    letters: Dict[str, str] = None,
        Dictionary of letters to add to the top left of the barplots.
        Use the name of the metric (the dataframe column) as key of the dictionary.
        This is sometimes necessary on papers.
        By default it is None, that is no letter to be shown.
    bar_width: float = 0.3,
        Width of the bar of the barplot.
    height: float = None,
        Height of the barplot. By default golden ratio of the width.
    dpi: int = 200,
        DPI for plotting the barplots.
    min_std: float = 0.001,
        Minimum standard deviation for showing error bars.
    min_value: float = None,
        Minimum value for the barplot.
    max_value: float = 0,
        Maximum value for the barplot.
    show_legend: bool = True,
        Whetever to show or not the legend.
        If legend is hidden, the bar ticks are shown alternatively.
    show_title: str = True,
        Whetever to show or not the barplot title.
    legend_position: str = "best",
        Legend position, by default "best".
    data_label: str = None,
        Barplot's data_label.
        Use None for not showing any data_label (default).
    title: str = None,
        Barplot's title.
        Use None for not showing any title (default).
    path: str = None,
        Path where to save the barplot.
        Use None for not saving it (default).
    colors: Dict[str, str] = None,
        Dict of colors to be used for innermost index of dataframe.
        By default None, using the default color tableau from matplotlib.
    alphas: Dict[str, float] = None,
        Dict of alphas to be used for innermost index of dataframe.
        By default None, using the default alpha.
    orientation: str = "vertical",
        Orientation of the bars.
        Can either be "vertical" of "horizontal".
    subplots: bool = False,
        Whetever to slit the top indexing layer to multiple subplots.
    plots_per_row: Union[int, str] = "auto",
        If subplots is True, specifies the number of plots for row.
        If "auto" is used, for vertical the default is 2 plots per row,
        while for horizontal the default is 4 plots per row.
    minor_rotation: float = 0,
        Rotation for the minor ticks of the bars.
    major_rotation: float = 0,
        Rotation for the major ticks of the bars.
    unique_minor_labels: bool = False,
        Avoid replicating minor labels on the same axis in multiple subplots settings.
    unique_major_labels: bool = True,
        Avoid replicating major labels on the same axis in multiple subplots settings.
    unique_data_label: bool = True,
        Avoid replication of data axis label when using subplots.
    auto_normalize_metrics: bool = True,
        Whetever to apply or not automatic normalization
        to the metrics that are recognized to be between
        zero and one. For example AUROC, AUPRC or accuracy.
    placeholder: bool = False,
        Whetever to add a text on top of the barplots to show
        the word "placeholder". Useful when generating placeholder data.
    scale: str = "linear",
        Scale to use for the barplots.
        Can either be "linear" or "log".
    custom_defaults: Dict[str, List[str]],
        Dictionary to normalize labels.
    use_multiprocessing: bool = True,
        Whetever to use or not multiple processes.
    verbose:bool,
        Whetever to show or not the loading bar.

    Returns
    ---------------------
    Tuple with list of rendered figures and rendered axes.
    """
    if groupby is not None:
        groupby = df.groupby(groupby).agg(
            ("mean",)+(("std",) if show_standard_deviation else tuple())
        ).sort_index()
    else:
        groupby = df

    features = original = {
        col if isinstance(col, str) else col[0]
        for col in groupby.columns
    }

    if letters is None:
        letters = {}
    if sanitize_metrics:
        features = sanitize_ml_labels(features)

    tasks = [
        dict(
            df=groupby[[original]],
            title=title.format(feature=feature.replace("_", " ")),
            data_label=data_label.format(feature=feature.replace("_", " ")),
            path=path.format(feature=feature).replace(" ", "_").lower(),
            letter=letters.get(original, None),
            bar_width=bar_width,
            space_width=space_width,
            height=height,
            dpi=dpi,
            min_std=min_std,
            min_value=min_value,
            max_value=max_value,
            show_legend=show_legend,
            show_title=show_title,
            legend_position=legend_position,
            colors=colors,
            alphas=alphas,
            facecolors=facecolors,
            orientation=orientation,
            subplots=subplots,
            plots_per_row=plots_per_row,
            minor_rotation=minor_rotation,
            major_rotation=major_rotation,
            unique_minor_labels=unique_minor_labels,
            unique_major_labels=unique_major_labels,
            unique_data_label=unique_data_label,
            auto_normalize_metrics=auto_normalize_metrics,
            placeholder=placeholder,
            scale=scale,
            custom_defaults=custom_defaults,
            sort_subplots=sort_subplots,
            sort_bars=sort_bars,
        ) for original, feature in zip(original, features)
        if not pd.isna(groupby[original]).any().any() and not len(groupby[original]) == 0
    ]

    if len(tasks) == 0:
        raise ValueError("No plottable feature found in given dataframe!")

    use_multiprocessing = use_multiprocessing and not len(tasks) == 1
    arguments = dict(
        desc="Rendering barplots",
        total=len(tasks),
        dynamic_ncols=True,
        disable=not verbose
    )

    if use_multiprocessing:
        with Pool(min(len(tasks), cpu_count())) as p:
            try:
                figures, axes = list(zip(*list(tqdm(
                    p.imap(_barplot, tasks),
                    **arguments
                ))))
                p.close()
                p.join()
            except Exception as e:
                p.close()
                p.join()
                raise e
    else:
        figures, axes = list(zip(*[
            barplot(**task)
            for task in tqdm(tasks, **arguments)
        ]))
    return figures, axes
