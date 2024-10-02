"""Save the given figure to the given path."""

import os
from matplotlib.figure import Figure


def save_picture(path: str, figure: Figure):
    """Save the given figure to the given path.

    Parameters
    ----------
    path: str,
        Path where to save the figure.
    figure: Figure,
        Figure to save.
    """
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    figure.savefig(path, bbox_inches="tight")
