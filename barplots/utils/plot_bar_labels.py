"""Submodule handling the plotting of the bar labels."""

from typing import Dict, List, Union, Optional

import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from sanitize_ml_labels import sanitize_ml_labels

from barplots.utils.get_max_bar_position import get_max_bar_position
from barplots.utils.text_positions import text_positions

factors = [
    ("_", 0),
    ("y", 1e-24),
    ("z", 1e-21),
    ("a", 1e-18),
    ("f", 1e-15),
    ("p", 1e-12),
    ("n", 1e-9),
    ("µ", 1e-6),
    ("m", 1e-3),
    ("K", 1e3),
    ("M", 1e6),
    ("G", 1e9),
    ("T", 1e12),
    ("P", 1e15),
    ("E", 1e18),
    ("Z", 1e21),
    ("Y", 1e24),
    ("_", float("inf")),
]


def sanitize_digits(digit: float, unit: Optional[str], normalized: bool):
    unit = "" if unit is None else unit
    absolute_digit = abs(digit)
    if (
        not normalized
        and digit != 0.0
        and (absolute_digit <= 1e-3 or absolute_digit >= 1e3)
    ):
        for (lower_factor, lower_value), (higher_factor, higher_value) in zip(
            factors[:-1],
            factors[1:],
        ):
            if absolute_digit < higher_value:
                if lower_factor == "_":
                    denominator = higher_value
                    factor = higher_factor
                else:
                    denominator = lower_value
                    factor = lower_factor
                digit /= denominator
                unit = factor + unit
                break

    return sanitize_ml_labels(digit) + unit


def plot_bar_labels(
    axes: Axes,
    figure: Figure,
    df: pd.DataFrame,
    vertical: bool,
    levels: int,
    bar_width: float,
    space_width: float,
    minor_rotation: Union[float, str],
    major_rotation: Union[float, str],
    unique_minor_labels: bool,
    unique_major_labels: bool,
    unique_data_label: bool,
    custom_defaults: Dict[str, List[str]],
    unit: Optional[str],
    normalized_metric: bool,
    absolutely_normalized_metric: bool,
):
    """
    Parameters
    ------------
    minor_rotation: Union[float, str]
        Rotation for the minor ticks of the bars.
        By default, with the "auto" mode, the library tries to find
        the rotation with which we minimize the overlap for the provided
        labels, including also the overlap with minor and major.
    major_rotation: Union[float, str]
        Rotation for the major ticks of the bars.
        By default, with the "auto" mode, the library tries to find
        the rotation with which we minimize the overlap for the provided
        labels, including also the overlap with minor and major.
    unique_minor_labels: bool = True,
        Avoid replicating minor labels on the same axis in multiple subplots settings.
    unique_major_labels: bool = True,
        Avoid replicating major labels on the same axis in multiple subplots settings.
    unique_data_label: bool = True,
        Avoid replication of data axis label when using subplots.
    unit: Optional[str]
        Optional unit to show on the value axis.
    normalized_metric: bool
        Whether to consider the current metric normalized in a range (0, 1)
    absolutely_normalized_metric: bool
        Whether to consider the current metric absolutely normalized in a range (-1, 1)
    """
    other_positions = set()
    width = get_max_bar_position(df, bar_width, space_width)

    if unique_data_label:
        axes.set_ylabel("")

    if normalized_metric or absolutely_normalized_metric:
        nbins = 5 if normalized_metric else 10

        if vertical:
            axes.locator_params(axis="y", nbins=nbins)
        else:
            axes.locator_params(axis="x", nbins=nbins)

    def sanitizer(x, *args, **kwargs):
        return sanitize_digits(
            x, unit=unit, normalized=normalized_metric or absolutely_normalized_metric
        )

    if vertical:
        axes.yaxis.set_major_formatter(plt.FuncFormatter(sanitizer))
    else:
        axes.xaxis.set_major_formatter(plt.FuncFormatter(sanitizer))

    for level in reversed(range(max(levels - 2, 0), levels)):
        positions, labels = zip(*text_positions(df, bar_width, space_width, level))
        labels = sanitize_ml_labels(labels, custom_defaults=custom_defaults)

        max_characters_number_in_labels = max((len(label) for label in labels))

        positions = [round(pos, 5) for pos in positions]
        positions = [
            position + width * 0.0002 if position in other_positions else position
            for position in positions
        ]
        other_positions |= set(positions)
        minor = level == levels - 1

        # Handle the automatic rotation of minor labels.
        if minor_rotation == "auto":
            if (
                minor
                and len(set(labels)) <= width * 5 / max_characters_number_in_labels
                and vertical
            ):
                adapted_minor_rotation = 90
            elif (
                minor
                and len(set(labels)) <= width * 20 / max_characters_number_in_labels
                and not vertical
            ):
                adapted_minor_rotation = 90
            else:
                adapted_minor_rotation = 0
        else:
            adapted_minor_rotation = minor_rotation

        # Handle the automatic rotation of major labels.
        if major_rotation == "auto":
            if (
                not minor
                and len(set(labels)) <= width * 5 / max_characters_number_in_labels
                and not vertical
            ):
                adapted_major_rotation = 90
            elif (
                not minor
                and len(set(labels)) >= width * 20 / max_characters_number_in_labels
                and vertical
            ):
                adapted_major_rotation = 90
            else:
                adapted_major_rotation = 0
        else:
            adapted_major_rotation = major_rotation

        if minor and unique_minor_labels:
            continue
        if not minor and unique_major_labels:
            continue

        if vertical:
            axes.set_xticks(positions, minor=minor)
            axes.set_xticklabels(labels, minor=minor, ha="center")
            if minor:
                axes.tick_params(
                    axis="x",
                    labelsize=9,
                    which="minor",
                    labelrotation=adapted_minor_rotation,
                )

                if adapted_minor_rotation > 80:
                    length = 6 * (max_characters_number_in_labels + 1)
                else:
                    length = 20

                axes.tick_params(
                    axis="x",
                    labelsize=10,
                    which="major",
                    direction="out",
                    length=length,
                    width=0,
                )
            else:
                axes.tick_params(
                    axis="x",
                    labelsize=10,
                    which="major",
                    labelrotation=adapted_major_rotation,
                )
        else:
            axes.set_yticks(positions, minor=minor)
            axes.set_yticklabels(labels, minor=minor, va="center")
            if minor:
                axes.tick_params(
                    axis="y",
                    which="minor",
                    labelsize=9,
                    labelrotation=adapted_minor_rotation,
                )

                if adapted_minor_rotation > 80:
                    length = 20
                else:
                    length = 6 * (max_characters_number_in_labels + 1)

                axes.tick_params(
                    axis="y",
                    which="major",
                    labelsize=10,
                    direction="out",
                    length=length,
                    # This is the size of the actual `tick`
                    # in the plot, which we do not want to show
                    # for the major ticks in this case and therefore
                    # we set it to zero.
                    width=0,
                )
            else:
                axes.tick_params(
                    axis="y", which="major", labelrotation=adapted_major_rotation
                )
