"""Module implementing plotting of multiple barplots in parallel and sequential manner."""

from typing import Dict, List, Tuple, Callable, Union, Optional

import pandas as pd
import numpy as np
from sanitize_ml_labels import sanitize_ml_labels
from userinput.utils import closest
from tqdm.auto import tqdm
from matplotlib.figure import Figure
from matplotlib.axis import Axis

from barplots.barplot import barplot


def plot_feature(
    values: pd.Series,
    skip_constant_columns: bool = True,
    skip_boolean_columns: bool = True,
) -> bool:
    """Returns whether to plot a given column."""
    return (
        # It does not contain NaN values
        not pd.isna(values).any().any()
        and
        # This is not an empty dataframe
        not len(values) == 0
        and
        # This is not a column of objects
        values.dtype != object
        and
        # It is not a sporiously loaded numeric index
        (values != np.arange(values.size)).any()
        and
        # It is not a binary-only column
        (not skip_boolean_columns or values.dtype != bool)
        and
        # It is not a column with constant values
        (not skip_constant_columns or (values != values.iloc[0]).any())
    )


def barplots(
    df: pd.DataFrame,
    groupby: Optional[Union[List[str], str]] = None,
    show_standard_deviation: Union[bool, str] = "auto",
    title: str = "{feature}",
    data_label: str = "{feature}",
    path: str = "barplots/{feature}.png",
    sanitize_metrics: bool = True,
    letters: Optional[Dict[str, str]] = None,
    letter_font_size: int = 20,
    bar_width: float = 0.3,
    space_width: float = 0.2,
    height: Optional[float] = None,
    dpi: int = 200,
    min_std: float = 0,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    show_legend: bool = True,
    show_last_level_as_legend: bool = True,
    show_title: str = True,
    show_column_name: bool = True,
    legend_position: str = "best",
    colors: Optional[Dict[str, str]] = None,
    hatch: Optional[Dict[str, str]] = None,
    alphas: Dict[str, float] = None,
    facecolors: Optional[Dict[str, str]] = None,
    orientation: str = "vertical",
    subplots: Union[bool, str] = "auto",
    plots_per_row: Union[int, str] = "auto",
    minor_rotation: Union[float, str] = "auto",
    major_rotation: Union[float, str] = "auto",
    unique_minor_labels: bool = True,
    unique_major_labels: bool = True,
    unique_data_label: bool = True,
    auto_normalize_metrics: bool = True,
    skip_constant_columns: bool = True,
    skip_boolean_columns: bool = True,
    placeholder: bool = False,
    scale: str = "linear",
    legend_entries_size: float = 8,
    legend_title_size: float = 9,
    show_legend_title: bool = True,
    letter_per_subplot: Optional[List[str]] = None,
    custom_defaults: Optional[Dict[str, List[str]]] = None,
    units: Optional[Dict[str, str]] = None,
    sort_bars: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
    ncol: Optional[int] = None,
    verbose: bool = True,
) -> Tuple[List[Figure], List[Axis]]:
    """Returns list of the built figures and axes.

    Plot barplots corresponding to given dataframe,
    grouping by mean and if required also standard deviation.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe from which to extrat data for plotting barplot.
    groupby: Optional[Union[List[str], str]] = None
        List of groupby over to run group by.
        If groupby was previously executed, leave this as None.
    show_standard_deviation: Union[bool, str] = "auto",
        Whetever to show or not the standard deviation.
        This can either be a boolean or "auto". With auto, we show the
        standard deviation for all the metrics where two or more values
        were provided, and we turn it off otherwise as it would not
        be defined with a single value.
        By default "auto".
    title: str = "{feature}"
        The title to use for the subgraphs.
        The `feature` placeholder is replaced with the considered column name.
    data_label: str = "{feature}"
        The label to use for the data axis.
        The `feature` placeholder is replaced with the considered column name.
    path: str = "barplots/{feature}.png"
        The path where to store the pictures.
        The `feature` placeholder is replaced with the considered column name.
    sanitize_metrics: bool = True
        Whetever to automatically sanitize to standard name given features.
        For instance, "acc" to "Accuracy" or "lr" to "Learning rate"
    letters: Optional[Dict[str, str]] = None
        Dictionary of letters to add to the top left of the barplots.
        Use the name of the metric (the dataframe column) as key of the dictionary.
        This is sometimes necessary on papers.
        By default it is None, that is no letter to be shown.
    letter_font_size: int = 20
        Font size to use for the barplot letter,
        if provided.
    bar_width: float = 0.3
        Width of the bar of the barplot.
    space_width: float = 0.2
        Width of the space between bar groups.
    height: Optional[float] = None
        Height of the barplot. By default golden ratio of the width.
    dpi: int = 200
        DPI for plotting the barplots.
    min_std: float = 0.001
        Minimum standard deviation for showing error bars.
    min_value: Optional[float] = None
        Minimum value for the barplot.
    max_value: float = 0
        Maximum value for the barplot.
    show_legend: bool = True,
        Whether to show the legend.
    show_last_level_as_legend: bool = True
        Whetever to show or not the legend.
        If legend is hidden, the bar ticks are shown alternatively.
    show_title: str = True
        Whetever to show or not the barplot title.
    show_column_name: bool = True
        Whether to show the metric name.
    legend_position: str = "best"
        Legend position, by default "best".
    data_label: str = None
        Barplot's data_label.
        Use None for not showing any data_label (default).
    title: str = None
        Barplot's title.
        Use None for not showing any title (default).
    path: str = None
        Path where to save the barplot.
        Use None for not saving it (default).
    colors: Optional[Dict[str, str]] = None
        Dict of colors to be used for innermost index of dataframe.
        By default None, using the default color tableau from matplotlib.
    hatch: Optional[Dict[str, str]] = None
        Dict of hatch, i.e. patterns for the bars, to be used for innermost index of dataframe.
    alphas: Dict[str, float] = None
        Dict of alphas to be used for innermost index of dataframe.
        By default None, using the default alpha.
    orientation: str = "vertical"
        Orientation of the bars.
        Can either be "vertical" of "horizontal".
    subplots: Union[bool, str] = "auto"
        Whetever to slit the top indexing layer to multiple subplots.
        If left to "auto", it will enable automatically subplots when
        an index in four dimensions is provided in the group by.
    plots_per_row: Union[int, str] = "auto"
        If subplots is True, specifies the number of plots for row.
        If "auto" is used, for vertical the default is 2 plots per row,
        while for horizontal the default is 4 plots per row.
    minor_rotation: Union[float, str] = "auto"
        Rotation for the minor ticks of the bars.
        By default, with the "auto" mode, the library tries to find
        the rotation with which we minimize the overlap for the provided
        labels, including also the overlap with minor and major.
    major_rotation: Union[float, str] = "auto"
        Rotation for the major ticks of the bars.
        By default, with the "auto" mode, the library tries to find
        the rotation with which we minimize the overlap for the provided
        labels, including also the overlap with minor and major.
    unique_minor_labels: bool = False
        Avoid replicating minor labels on the same axis in multiple subplots settings.
    unique_major_labels: bool = True
        Avoid replicating major labels on the same axis in multiple subplots settings.
    unique_data_label: bool = True
        Avoid replication of data axis label when using subplots.
    auto_normalize_metrics: bool = True
        Whetever to apply or not automatic normalization
        to the metrics that are recognized to be between
        zero and one. For example AUROC, AUPRC or accuracy.
    skip_constant_columns: bool = True
        Whether to drop the constant columns from plotting.
    skip_boolean_columns: bool = True
        Whether to drop the boolean columns from plotting.
    placeholder: bool = False
        Whetever to add a text on top of the barplots to show
        the word "placeholder". Useful when generating placeholder data.
    scale: str = "linear"
        Scale to use for the barplots.
        Can either be "linear" or "log".
    legend_entries_size: float = 8
        Size for the legend entries font.
    legend_title_size: float = 9
        Size for the legend title font.
    show_legend_title: bool = True
        Whether to show the legend title.
    letter_per_subplot: Optional[List[str]] = None
        Letter to show on the top left of each subplot.
        This is sometimes necessary on papers.
        By default it is None, that is no letter to be shown.
    custom_defaults: Optional[Dict[str, List[str]]] = None
        Dictionary to use to normalize the various labels.
        This argoment will be forwarded to sanitize ML labels.
    units: Optional[Dict[str, str]] = None
        Dictionary of the units to be shown on the side of the metrics.
        The dictionary expected is of the form: {metric: unit}
    sort_bars: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None
        Callable that receives a dataframe and returns it arbitrarily sorted.
    ncol: Optional[int] = None
        The number of columns to show in the barplot.
    verbose: bool
        Whetever to show or not the loading bar.

    Returns
    ---------------------
    Tuple with list of rendered figures and rendered axes.
    """
    if isinstance(groupby, str):
        groupby = [groupby]

    if len(df.columns) == 0:
        raise ValueError("The provided DataFrame does not have any column.")

    if subplots == "auto":
        if groupby is not None and len(groupby) == 4:
            subplots = True
        else:
            subplots = False

    if not subplots and len(groupby) > 3:
        raise ValueError(
            (
                "Without subplots it is not possible to visualize a "
                f"dataframe with an index of size of {len(groupby)}."
            )
        )

    # Filtering out columns that are not visualizable.
    df = df[
        [
            column
            for column in df.columns
            if groupby is not None
            and column in groupby
            or plot_feature(
                df[column],
                skip_constant_columns=skip_constant_columns,
                skip_boolean_columns=skip_boolean_columns,
            )
        ]
    ]

    if groupby is not None:
        if len(groupby) == 0:
            raise ValueError(
                "The provided list of columns to execute groupby on is empty."
            )
        for column_name in groupby:
            if column_name not in df.columns:
                raise ValueError(
                    (
                        f"The provided column {column_name} is not available "
                        "in the set of columns of the dataframe. Di you mean "
                        f"the column {closest(column_name, df.columns)}?"
                    )
                )

            # So we can standardize this.
            backup = pd.options.mode.chained_assignment
            pd.options.mode.chained_assignment = None
            df[column_name] = df[column_name].astype(str)
            pd.options.mode.chained_assignment = backup

        groupby = (
            df.groupby(groupby)
            .agg(("mean",) + (("std",) if show_standard_deviation else tuple()))
            .sort_index()
        )
    else:
        groupby = df

    # If the use has left it to us to decide whether to show
    # or not the standard deviation, we go hunting for Nan values.
    # We proceed to drop the columns of the standard deviation with
    # NaN values in every occasion we encounter them.
    if show_standard_deviation == "auto":
        # First we check whether the dataframe we are currently
        # processing has multi-index columns. If it does not,
        # then this is a custom dataframe and we need to interfere
        # with it.
        if issubclass(groupby.columns.__class__, pd.MultiIndex):
            for column in groupby.columns:
                # We also need to check whether there is any "std"
                # column, as it may be the case that this is a custom
                # dataframe without such a sub-column.
                if "std" not in column:
                    continue
                # If we find any NaN value, we drop the sub-column.
                if groupby[column].isna().any():
                    groupby.drop(columns=[column], inplace=True)

    features = original = {
        col if isinstance(col, str) else col[0] for col in groupby.columns
    }

    if letters is None:
        letters = {}

    if units is None:
        units = {}

    if sanitize_metrics:
        features = sanitize_ml_labels(features)

    return [
        barplot(
            df=groupby[[original]],
            title=title.format(feature=feature.replace("_", " ")),
            data_label=data_label.format(feature=feature.replace("_", " ")),
            path=path.format(feature=feature).replace(" ", "_").lower(),
            bar_width=bar_width,
            space_width=space_width,
            height=height,
            dpi=dpi,
            min_std=min_std,
            min_value=min_value,
            max_value=max_value,
            show_legend=show_legend,
            show_last_level_as_legend=show_last_level_as_legend,
            show_title=show_title,
            show_column_name=show_column_name,
            legend_position=legend_position,
            colors=colors,
            hatch=hatch,
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
            legend_entries_size=legend_entries_size,
            legend_title_size=legend_title_size,
            letter_per_subplot=letter_per_subplot,
            show_legend_title=show_legend_title,
            custom_defaults=custom_defaults,
            sort_bars=sort_bars,
            unit=units.get(original, None),
            letter=letters.get(original, None),
            letter_font_size=letter_font_size,
            ncol=ncol,
        )
        for original, feature in tqdm(
            zip(original, features),
            desc="Rendering barplots",
            total=len(original),
            dynamic_ncols=True,
            leave=False,
            disable=not verbose or len(original) == 1,
        )
    ]
