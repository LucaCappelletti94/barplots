"""Submodule providing a function to apply regex patterns to a list of strings and return the best match."""

import re


def get_best_match(mapping, index):
    compiled_keys = {
        key: (
            (re.compile(key),) if isinstance(key, str) else [re.compile(k) for k in key]
        )
        for key in mapping
    }
    if not isinstance(index, tuple):
        index = (index,)

    scores = {
        key: sum(
            len(match)
            for pattern in compiled_keys[key]
            for level in index
            for match in pattern.findall(level)
        )
        for key in mapping
    }

    return mapping[max(scores.keys(), key=(lambda key: scores[key]))]
