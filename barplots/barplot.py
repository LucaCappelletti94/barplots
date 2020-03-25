import pandas as pd
from typing import List, Tuple, Dict, Union, Callable
from matplotlib.colors import TABLEAU_COLORS, CSS4_COLORS
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from .utils import get_axes, get_levels, \
    remove_duplicated_legend_labels, get_max_bar_lenght,\
    save_picture, plot_bars, plot_bar_labels
from sanitize_ml_labels import is_normalized_metric


def barplot(
    df: pd.DataFrame,
    bar_width: float = 0.3,
    space_width: float = 0.3,
    height: float = None,
    dpi: int = 200,
    min_std: float = 0,
    show_legend: bool = True,
    legend_position: str = "best",
    data_label: str = None,
    title: str = None,
    path: str = None,
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
    scale: str = "linear",
    custom_defaults: Dict[str, List[str]] = None,
    sort_subplots: Callable[[List], List] = None,
    sort_bars: Callable[[pd.DataFrame], pd.DataFrame] = None
) -> Tuple[Figure, Axes]:
    """Plot barplot corresponding to given dataframe, containing y value and optionally std.

    Parameters
    ----------
    df: pd.DataFrame,
        Dataframe from which to extrat data for plotting barplot.
    bar_width: float = 0.3,
        Width of the bar of the barplot.
    height: float = None,
        Height of the barplot. By default golden ratio of the width.
    dpi: int = 200,
        DPI for plotting the barplots.
    min_std: float = 0.001,
        Minimum standard deviation for showing error bars.
    show_legend: bool = True,
        Whetever to show or not the legend.
        If legend is hidden, the bar ticks are shown alternatively.
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
    custom_defaults: Dict[str, List[str]],
        Dictionary to normalize labels.

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
            zip(levels[-1], list(TABLEAU_COLORS.keys()) + list(CSS4_COLORS.keys())))
    
    if alphas is None:
        alphas = dict(zip(levels[-1], (0.9,)*len(levels[-1])))
    
    if facecolors is None:
        facecolors = dict(zip(levels[0], ("white",)*len(levels[0])))

    if sort_subplots is None:
        sort_subplots = lambda x: x
    
    if sort_bars is None:
        sort_bars = lambda x: x

    sorted_level = sort_subplots(levels[0])

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
        facecolors
    )

    for i, (index, ax) in enumerate(zip(titles, axes)):
        if subplots:
            sub_df = df.loc[index]
        else:
            sub_df = df

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
                ax, legend_position, custom_defaults)

        max_lenght, min_lenght = get_max_bar_lenght(sub_df, bar_width, space_width)
        max_lenght *= 1.01
        min_lenght *= 1.01
        if auto_normalize_metrics and (is_normalized_metric(df.columns[0]) or is_normalized_metric(title)):
            max_lenght = max(max_lenght, 1.01)
            min_lenght = min(min_lenght, 0)

        if vertical:
            ax.set_ylim(min_lenght, max_lenght)
        else:
            ax.set_xlim(min_lenght, max_lenght)

    figure.tight_layout()

    if path is not None:
        save_picture(path, figure)

    return figure, axes
