"""Module implementing plotting of a barplot."""

from typing import List, Tuple, Dict, Union, Callable, Optional
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from sanitize_ml_labels import is_normalized_metric, is_absolutely_normalized_metric
from barplots.utils import (
    get_axes,
    get_levels,
    remove_duplicated_legend_labels,
    get_max_bar_length,
    save_picture,
    plot_bars,
    plot_bar_labels,
)

# List of 10 distinct colors from the Tableau palette.
TABLEAU_COLORS = [
    "#4e79a7",
    "#f28e2b",
    "#e15759",
    "#76b7b2",
    "#59a14e",
    "#edc949",
    "#b07aa2",
    "#ff9da7",
    "#9c755f",
    "#bab0ac",
]

# List of 20 distinct colors composed by Sasha Trubetskoy.
SASHA_COLORS = [
    "#e6194B",
    "#3cb44b",
    "#ffe119",
    "#4363d8",
    "#f58231",
    "#911eb4",
    "#42d4f4",
    "#f032e6",
    "#bfef45",
    "#fabed4",
    "#469990",
    "#dcbeff",
    "#9A6324",
    "#fffac8",
    "#800000",
    "#aaffc3",
    "#808000",
    "#ffd8b1",
    "#000075",
    "#a9a9a9",
]

# List of hatches supported by matplotlib.
HATCHES = [
    "x",
    "o",
    "*",
    "/",
    "O",
    "\\",
    "|",
    ".",
    "-",
    "+",
]


def barplot(
    df: pd.DataFrame,
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
    data_label: Optional[str] = None,
    title: Optional[str] = None,
    path: Optional[str] = None,
    colors: Optional[Dict[str, str]] = None,
    hatch: Optional[Dict[str, str]] = None,
    alphas: Optional[Dict[str, float]] = None,
    facecolors: Optional[Dict[str, str]] = None,
    orientation: str = "vertical",
    subplots: bool = False,
    plots_per_row: Union[int, str] = "auto",
    minor_rotation: Union[float, str] = "auto",
    major_rotation: Union[float, str] = "auto",
    unique_minor_labels: bool = False,
    unique_major_labels: bool = True,
    unique_data_label: bool = True,
    auto_normalize_metrics: bool = True,
    placeholder: bool = False,
    scale: str = "linear",
    sanitize_metrics: bool = True,
    unit: Optional[str] = None,
    legend_entries_size: float = 8,
    legend_title_size: float = 9,
    letter_per_subplot: Optional[List[str]] = None,
    show_legend_title: bool = True,
    custom_defaults: Dict[str, List[str]] = None,
<<<<<<< HEAD
    sort_bars: Callable[[pd.DataFrame], pd.DataFrame] = None,
=======
    sort_subplots: Callable[[List], List] = None,
    sort_bars: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
>>>>>>> 6fc1cff (Working on MyPy support)
    letter: Optional[str] = None,
    letter_font_size: int = 20,
    ncol: Optional[int] = None,
) -> Tuple[Figure, Axes]:
    """Plot barplot corresponding to given dataframe, containing y value and optionally std.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to extrat data for plotting barplot.
    bar_width: float = 0.3,
        Width of the bar of the barplot.
    space_width: float = 0.2
        Width of the space between bar groups.
    height: Optional[float] = None,
        Height of the barplot. By default golden ratio of the width.
    dpi: int = 200,
        DPI for plotting the barplots.
    min_std: float = 0.001,
        Minimum standard deviation for showing error bars.
    min_value: Optional[float] = None,
        Minimum value for the barplot.
    max_value: float = 0,
        Maximum value for the barplot.
    show_legend: bool = True,
        Whether to show the legend.
    show_last_level_as_legend: bool = True,
        Whetever to show or not the legend.
        If legend is hidden, the bar ticks are shown alternatively.
    show_title: str = True
        Whetever to show or not the barplot title.
    show_column_name: bool = True
        Whether to show the metric name.
    legend_position: str = "best",
        Legend position, by default "best".
    data_label: Optional[str] = None,
        Barplot's data_label.
        Use None for not showing any data_label (default).
    title: Optional[str] = None,
        Barplot's title.
        Use None for not showing any title (default).
    path: Optional[str] = None,
        Path where to save the barplot.
        Use None for not saving it (default).
    colors: Optional[Dict[str, str]] = None,
        Dict of colors to be used for innermost index of dataframe.
        By default None, using the default color tableau from matplotlib.
    hatch: Optional[Dict[str, str]] = None
        Dict of hatch, i.e. patterns for the bars, to be used for innermost index of dataframe.
    alphas: Optional[Dict[str, float]] = None,
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
    sanitize_metrics: bool = True,
        Whetever to sanitize the metrics names.
    unit: Optional[str] = None
        The unit to show in the value axis of the plot.
    legend_entries_size: float = 8
        Size for the legend entries font.
    legend_title_size: float = 9
        Size for the legend title font.
    show_legend_title: bool = True
        Whether to show the legend title.
    custom_defaults: Dict[str, List[str]],
        Dictionary to normalize labels.
    letter: Optional[str] = None
        Letter to show on the top left of the figure.
        This is sometimes necessary on papers.
        By default it is None, that is no letter to be shown.
    letter_per_subplot: Optional[List[str]] = None
        Letter to show on the top left of each subplot.
        This is sometimes necessary on papers.
        By default it is None, that is no letter to be shown.
    letter_font_size: int = 20
        Font size to use for the barplot letter,
        if provided.
    ncol: Optional[int] = None
        The number of columns to show in the barplot.

    Raises
    ------
    ValueError:
        If the given orientation is nor "vertical" nor "horizontal".
    ValueError:
        If the given plots_per_row is nor "auto" or a positive integer.
    ValueError:
        If subplots is True and less than a single index level is provided.

    Returns
    -------
    Tuple containing Figure and Axes of created barplot.
    """

    if orientation not in ("vertical", "horizontal"):
<<<<<<< HEAD
        raise ValueError(f'Given orientation "{orientation}" is not supported.')
=======
        raise ValueError(
            'Given orientation "{orientation}" is not supported.'.format(
                orientation=orientation
            )
        )
>>>>>>> 6fc1cff (Working on MyPy support)

    if (
        not isinstance(plots_per_row, int)
        and plots_per_row != "auto"
        or isinstance(plots_per_row, int)
        and plots_per_row < 1
    ):
        raise ValueError(
<<<<<<< HEAD
            f"Given plots_per_row \"{plots_per_row}\" is not 'auto' or a positive integer."
=======
            "Given plots_per_row \"{plots_per_row}\" is not 'auto' or a positive integer.".format(
                plots_per_row=plots_per_row
            )
>>>>>>> 6fc1cff (Working on MyPy support)
        )

    vertical = orientation == "vertical"

    levels = get_levels(df)
    expected_levels = len(levels) - int(show_last_level_as_legend) - int(subplots)

    if len(levels) <= 1 and subplots:
        raise ValueError("Unable to split plots with only a single index level.")

    if plots_per_row == "auto":
        if subplots:
            plots_per_row = min(
                len(levels[0]), (1 if df.shape[0] > 40 else 2) if vertical else 4
            )
    else:
        plots_per_row = min(plots_per_row, len(levels[0]))
<<<<<<< HEAD

    infer_alphas = alphas is not None
    infer_colors = colors is not None
    infer_hatch = hatch is not None
    infer_edgecolors = False

    edgecolors = None

    if colors is None:
        # When the number of provide faces is less than the
        # tableau colors, we use the tableau colors, else we use
        # the Sasha colors. If even these are not enough, we use
        # the hatches so that we can differentiate the bars more
        # easily.
        if len(levels[-1]) <= len(TABLEAU_COLORS):
            colors = dict(zip(levels[-1], TABLEAU_COLORS))
        elif len(levels[-1]) <= len(SASHA_COLORS):
            colors = dict(zip(levels[-1], SASHA_COLORS))
        else:
            colors: Dict[str, str] = {}
            hatch: Dict[str, str] = {}
            edgecolors: Dict[str, str] = {}
            for i, level in enumerate(levels[-1]):
                colors[level] = TABLEAU_COLORS[i % len(TABLEAU_COLORS)]
                if i >= len(TABLEAU_COLORS):
                    adjusted_i = i // len(TABLEAU_COLORS) - 1
                    hatch[level] = HATCHES[adjusted_i % len(HATCHES)]
                    edgecolors[level] = "white"
=======

    if colors is None:
        colors = dict(zip(levels[-1], TABLEAU_COLORS + list(OLD_TABLEAU_COLORS.keys())))
>>>>>>> 6fc1cff (Working on MyPy support)

    if alphas is None:
        alphas = dict(zip(levels[-1], (0.95,) * len(levels[-1])))

    if facecolors is None:
        facecolors = dict(zip(levels[0], ("white",) * len(levels[0])))

    sorted_level = levels[0]

    if subplots:
        titles = sorted_level
    else:
        titles = ("",)

    figure, axes = get_axes(
        df,
        bar_width,
        space_width,
        height,
        dpi,
        title,
        data_label,
        vertical,
        subplots,
        titles,
        plots_per_row,
        custom_defaults,
        expected_levels,
        scale,
        sanitize_metrics,
        facecolors,
        show_title,
        show_column_name,
    )

    if letter_per_subplot is None:
        letter_per_subplot = ["" for _ in range(len(axes))]

    for i, (subplot_letter, index, ax) in enumerate(
        zip(letter_per_subplot, titles, axes)
    ):
        if subplots:
            sub_df = df.loc[index]
        else:
            sub_df = df

        if sort_bars is not None:
            sub_df = sort_bars(sub_df)

        plot_bars(
            ax,
            sub_df,
            bar_width,
            space_width,
            alphas,
<<<<<<< HEAD
            infer_alphas,
            colors,
            infer_colors,
            edgecolors,
            infer_edgecolors,
            hatch,
            infer_hatch,
=======
            colors,
            hatch,
>>>>>>> 6fc1cff (Working on MyPy support)
            index,
            vertical=vertical,
            min_std=min_std,
        )

        is_not_first_ax = subplots and (
            (not vertical and i % plots_per_row)
            or (vertical and i < len(axes) - plots_per_row)
        )

        is_not_first_vertical_ax = subplots and (
            (vertical and i % plots_per_row)
            or (not vertical and i < len(axes) - plots_per_row)
        )

        normalized_metric = auto_normalize_metrics and (
<<<<<<< HEAD
            is_normalized_metric(df.columns[0][0]) or is_normalized_metric(title)
        )
        absolutely_normalized_metric = auto_normalize_metrics and (
            is_absolutely_normalized_metric(df.columns[0][0])
=======
            is_normalized_metric(df.columns[0]) or is_normalized_metric(title)
        )
        absolutely_normalized_metric = auto_normalize_metrics and (
            is_absolutely_normalized_metric(df.columns[0])
>>>>>>> 6fc1cff (Working on MyPy support)
            or is_absolutely_normalized_metric(title)
        )

        plot_bar_labels(
            ax,
            figure,
            sub_df,
            vertical,
            expected_levels,
            bar_width,
            space_width,
            minor_rotation,
            major_rotation,
            unique_minor_labels and is_not_first_ax,
            unique_major_labels and is_not_first_ax,
            unique_data_label and is_not_first_vertical_ax,
            custom_defaults,
            unit,
            normalized_metric=normalized_metric,
            absolutely_normalized_metric=absolutely_normalized_metric,
<<<<<<< HEAD
            sanitize_metrics=sanitize_metrics,
=======
>>>>>>> 6fc1cff (Working on MyPy support)
        )

        ax.text(
            x=-0.1,
            y=1.1,
            s=subplot_letter,
            size=12,
            color="black",
            weight="bold",
            horizontalalignment="left",
            verticalalignment="center",
            transform=ax.transAxes,
        )

        if show_last_level_as_legend and show_legend:
            remove_duplicated_legend_labels(
                ax,
                legend_position,
                df.index.names[-1],
                legend_entries_size,
                legend_title_size,
                show_legend_title,
                custom_defaults,
                ncol,
            )

        max_length, min_length = get_max_bar_length(sub_df, bar_width, space_width)
        max_length *= 1.01
        min_length *= 1.01
        min_length = min(min_length, 0)

        if min_value is not None:
            min_length = min_value

        if normalized_metric:
            max_length = max(max_length, 1.01)
        elif absolutely_normalized_metric:
            max_length = max(max_length, 1.01)
            if min_length < 0:
                min_length = min(min_length, -1.01)

        if max_value is not None:
            max_length = max_value

        if placeholder:
            ax.text(
                0.5,
                0.5,
                "PLACEHOLDER",
                fontsize=30,
                alpha=0.75,
                color="red",
                rotation=8,
                horizontalalignment="center",
                verticalalignment="center",
                transform=ax.transAxes,
            )

        if vertical:
            ax.set_ylim(min_length, max_length)
        else:
            ax.set_xlim(min_length, max_length)

    figure.tight_layout()

    if letter:
        figure.text(
            0,
            0.95,
            letter,
            horizontalalignment="left",
            verticalalignment="top",
            weight="bold",
            fontsize=letter_font_size,
        )

    if path is not None:
        save_picture(path, figure)

    return figure, axes
