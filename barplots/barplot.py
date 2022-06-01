"""Module implementing plotting of a barplot."""
import pandas as pd
from typing import List, Tuple, Dict, Union, Callable, Optional
from matplotlib.colors import TABLEAU_COLORS as OLD_TABLEAU_COLORS
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from .utils import get_axes, get_levels, \
    remove_duplicated_legend_labels, get_max_bar_length,\
    save_picture, plot_bars, plot_bar_labels
from sanitize_ml_labels import is_normalized_metric, is_absolutely_normalized_metric

# These colors are from Tableau
TABLEAU_COLORS = [
    '#4e79a7',
    '#f28e2b',
    '#e15759',
    '#76b7b2',
    '#59a14e',
    "#edc949",
    "#b07aa2",
    "#ff9da7",
    "#9c755f",
    "#bab0ac",
]

def barplot(
    df: pd.DataFrame,
    bar_width: float = 0.3,
    space_width: float = 0.3,
    height: Optional[float] = None,
    dpi: int = 200,
    min_std: float = 0,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    show_legend: bool = True,
    show_title: str = True,
    legend_position: str = "best",
    data_label: Optional[str] = None,
    title: Optional[str] = None,
    path: Optional[str] = None,
    colors: Optional[Dict[str, str]] = None,
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
    custom_defaults: Dict[str, List[str]] = None,
    sort_subplots: Callable[[List], List] = None,
    sort_bars: Callable[[pd.DataFrame], pd.DataFrame] = None,
    letter: Optional[str] = None
) -> Tuple[Figure, Axes]:
    """Plot barplot corresponding to given dataframe, containing y value and optionally std.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to extrat data for plotting barplot.
    bar_width: float = 0.3,
        Width of the bar of the barplot.
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
        Whetever to show or not the legend.
        If legend is hidden, the bar ticks are shown alternatively.
    show_title: str = True,
        Whetever to show or not the barplot title.
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
    custom_defaults: Dict[str, List[str]],
        Dictionary to normalize labels.
    letter: Optional[str] = None,
        Letter to show on the top left of the figure.
        This is sometimes necessary on papers.
        By default it is None, that is no letter to be shown.

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
        raise ValueError("Given orientation \"{orientation}\" is not supported.".format(
            orientation=orientation
        ))

    if not isinstance(plots_per_row, int) and plots_per_row != "auto" or isinstance(plots_per_row, int) and plots_per_row < 1:
        raise ValueError("Given plots_per_row \"{plots_per_row}\" is not 'auto' or a positive integer.".format(
            plots_per_row=plots_per_row
        ))

    vertical = orientation == "vertical"

    levels = get_levels(df)
    expected_levels = len(levels) - int(show_legend) - int(subplots)

    if len(levels) <= 1 and subplots:
        raise ValueError(
            "Unable to split plots with only a single index level.")

    if plots_per_row == "auto":
        if subplots:
            plots_per_row = min(
                len(levels[0]),
                2 if vertical else 4
            )
    else:
        plots_per_row = min(
            plots_per_row,
            len(levels[0])
        )

    if colors is None:
        colors = dict(
            zip(levels[-1], TABLEAU_COLORS + list(OLD_TABLEAU_COLORS.keys()))
        )

    if alphas is None:
        alphas = dict(zip(levels[-1], (0.95,)*len(levels[-1])))

    if facecolors is None:
        facecolors = dict(zip(levels[0], ("white",)*len(levels[0])))

    sorted_level = levels[0]

    if sort_subplots is not None:
        sorted_level = sort_subplots(sorted_level)

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
        facecolors,
        show_title
    )

    for i, (index, ax) in enumerate(zip(titles, axes)):
        if subplots:
            sub_df = df.loc[index]
        else:
            sub_df = df

        if sort_bars is not None:
            sub_df = sort_bars(sub_df)

        plot_bars(ax, sub_df, bar_width, space_width, alphas, colors, index,
                  vertical=vertical, min_std=min_std)

        is_not_first_ax = subplots and (
            (not vertical and i % plots_per_row) or
            (vertical and i < len(axes) - plots_per_row)
        )

        is_not_first_vertical_ax = subplots and (
            (vertical and i % plots_per_row) or
            (not vertical and i < len(axes) - plots_per_row)
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
            custom_defaults
        )

        if show_legend:
            remove_duplicated_legend_labels(
                ax,
                legend_position,
                df.index.names[-1],
                custom_defaults,
            )

        max_length, min_length = get_max_bar_length(
            sub_df,
            bar_width,
            space_width
        )
        max_length *= 1.01
        min_length *= 1.01
        min_length = min(min_length, 0)

        if min_value is not None:
            min_length = min_value

        if auto_normalize_metrics:
            if is_normalized_metric(df.columns[0]) or is_normalized_metric(title):
                max_length = max(max_length, 1.01)
            elif is_absolutely_normalized_metric(df.columns[0]) or is_absolutely_normalized_metric(title):
                max_length = max(max_length, 1.01)
                if min_length < 0:
                    min_length = min(min_length, -1.01)

        if max_value is not None:
            max_length = max_value

        if placeholder:
            ax.text(
                0.5, 0.5,
                "PLACEHOLDER",
                fontsize=30,
                alpha=0.75,
                color="red",
                rotation=8,
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes
            )

        if vertical:
            ax.set_ylim(min_length, max_length)
        else:
            ax.set_xlim(min_length, max_length)

    if letter:
        figure.text(
            0.01, 0.9, letter,
            horizontalalignment='center',
            verticalalignment='center',
            weight='bold',
            fontsize=15
        )

    figure.tight_layout()

    if path is not None:
        save_picture(path, figure)

    return figure, axes
