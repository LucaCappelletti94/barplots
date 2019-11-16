def sanitize_label(label: str) -> str:
    """Return sanitized label.

    Parameters
    ----------
    label: str,
        The label to be sanitize.

    Returns
    -------
    The sanitized label.
    """
    return str(label).replace("_", " ")