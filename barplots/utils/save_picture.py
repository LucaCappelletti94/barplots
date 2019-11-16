from matplotlib.figure import Figure
import os


def save_picture(path: str, figure: Figure):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    figure.savefig(path, bbox_inches='tight')
