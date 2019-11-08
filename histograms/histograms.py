import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce
from typing import List
from matplotlib.colors import TABLEAU_COLORS
import os
from tqdm.auto import tqdm


def bar_offset(bar_index: int, indices: List[int], bar_width: float, increase: float) -> float:
    x = bar_index * bar_width
    previous_bars = 1
    for index in reversed(indices):
        previous_bars *= index
        if bar_index >= previous_bars:
            x += (bar_index // previous_bars) * bar_width * (increase)
    return x


def histograms(df: pd.DataFrame, path: str, bar_width: float = 0.3, increase: float = 1.05, height: float = 5):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    indices = [len(x) for x in df.index.levels]
    colors = list(TABLEAU_COLORS.keys())
    prod = reduce(lambda x, y: x*y, indices)-1
    width = bar_offset(prod, indices, bar_width, increase) + bar_width

    for feature in tqdm(df.columns.levels[0], leave=False):
        fig, axis = plt.subplots(figsize=(
            width,
            height
        ), dpi=200)

        labels_offsets = []
        for i, (names, (mean, std)) in enumerate(df[feature].iterrows()):
            x = bar_offset(i, indices, bar_width, increase) + bar_width/2
            axis.bar(
                x,
                mean,
                **({"yerr": std} if std > 0 else {}),
                color=colors[list(df.index.levels[-1]).index(names[-1])],
                width=0.3,
                capsize=5,
                alpha=0.9,
                label=names[-1]
            )
            previous_bars = indices[-1]

            for j, index in enumerate(reversed(indices[:-1])):
                #previous_bars *= index
                if (i+1) % previous_bars == 0 and i != 0:
                    if j == len(labels_offsets):
                        labels_offsets.append(x/2)
                    axis.text(
                        x - labels_offsets[j] + bar_width/4,
                        -0.05,
                        names[j],
                        horizontalalignment='center'
                    )
        axis.yaxis.grid(True, which="both")
        # fig.tight_layout()
        axis.set_xlim(0, width)
        axis.set_ylim(0, 1)
        axis.set_xticks([])
        handles, labels = fig.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        axis.legend(by_label.values(), by_label.keys(), loc='best')
        axis.set_title(feature.replace("_", " ").capitalize())

        fig.savefig("{path}/{feature}.jpg".format(
            path=path,
            feature=feature
        ))