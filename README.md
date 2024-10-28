# Barplots

<<<<<<< HEAD
[![pip](https://badge.fury.io/py/barplots.svg)](https://pypi.org/project/barplots/)
[![downloads](https://pepy.tech/badge/barplots)](https://pepy.tech/project/barplots)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/LucaCappelletti94/barplots/blob/master/LICENSE)
[![CI](https://github.com/LucaCappelletti94/barplots/actions/workflows/python.yml/badge.svg)](https://github.com/LucaCappelletti94/barplots/actions)

Python package to easily make barplots from multi-indexed dataframes.

## How do I install this package?

As usual, just download it using pip:
=======
![pip](https://badge.fury.io/py/barplots.svg) ![downloads](https://pepy.tech/badge/barplots)

Python package to easily make barplots from multi-indexed DataFrames.

## Installation

Install with pip:
>>>>>>> 6fc1cff (Working on MyPy support)

```shell
pip install barplots
```

## Documentation

<<<<<<< HEAD
Most methods, in particular those exposed to user usage, are provided with docstrings. Consider reading these docstrings to learn about the most recent updates to the library.

## Examples of the DataFrame structure

The dataframe to be provided to the barplots library may look like the following:

| miss_rate  | fall_out | mcc       | evaluation_type | unbalance | graph_name                 | normalization_name |
|------------|----------|-----------|-----------------|-----------|----------------------------|--------------------|
| 0.0332031  | 0.705078 | 0.353357  | train           | 10        | AlligatorSinensis           | Traditional        |
| 0.240234   | 0.478516 | 0.289591  | train           | 1         | CanisLupus                  | Right Laplacian     |
| 0.0253906  | 0.931641 | 0.101643  | train           | 100       | AlligatorSinensis           | Right Laplacian     |
| 0.121094   | 0.699219 | 0.220219  | train           | 10        | HomoSapiens                 | Traditional        |
| 0.0136719  | 0.292969 | 0.722095  | test            | 1         | CanisLupus                  | Right Laplacian     |
| 0.0605469  | 0.90625  | 0.0622185 | test            | 10        | AmanitaMuscariaKoideBx008    | Traditional        |
| 0.0078125  | 0.4375   | 0.614287  | train           | 100       | AmanitaMuscariaKoideBx008    | Traditional        |
| 0.171875   | 0.869141 | -0.0572194| train           | 100       | AlligatorSinensis           | Traditional        |
| 0.0859375  | 0.810547 | 0.150206  | train           | 10        | MusMusculus                 | Right Laplacian     |
| 0.0273438  | 0.646484 | 0.415357  | test            | 10        | MusMusculus                 | Right Laplacian     |

Specifically, in this example, we may create bar plots for the features **Miss rate**, **fallout**, and **Matthew Correlation Coefficient** by grouping on the `evaluation_type`, `unbalance`, `graph_name`, and `normalization_name` columns.

An example CSV file can be seen [here](https://github.com/LucaCappelletti94/barplots/blob/master/tests/test_case.csv).

## Usage examples

Here follows a set of examples of common usages. Basically, every graph shows either the same data or a mean based on the provided group by indices. Choose whatever representation is best for visualizing your data, as one is not necessarily better than another for every dataset.

> **Note**: The data used in the following examples are **randomly generated** for testing purposes. **DO NOT** consider these values as valid results for experiments using the same labels (cell lines, etc.), which are only used to show possible usages.

For every example, the considered dataframe `df` is loaded as follows:

```python
import pandas as pd

df = pd.read_csv("tests/test_case.csv")
```

Also, for every example, the `custom_defaults` used to sanitize the labels specific to the dataset is:
=======
Most methods, especially those exposed to users, include docstrings. Refer to these docstrings to learn about the most recent updates to the library.

## Examples of the DataFrame Structure

The DataFrame to be used with the `barplots` library might look like this:

| miss_rate | fall_out | mcc       | evaluation_type | unbalance | graph_name                | normalization_name |
|-----------|----------|-----------|-----------------|-----------|---------------------------|---------------------|
| 0.0332031 | 0.705078 | 0.353357  | train           | 10        | AlligatorSinensis         | Traditional         |
| 0.240234  | 0.478516 | 0.289591  | train           | 1         | CanisLupus                | Right Laplacian     |
| 0.0253906 | 0.931641 | 0.101643  | train           | 100       | AlligatorSinensis         | Right Laplacian     |
| ...       | ...      | ...       | ...             | ...       | ...                       | ...                 |

In this example, you can create bar plots for features such as *miss rate*, *fallout*, and *Matthew Correlation Coefficient* by grouping on columns like `evaluation_type`, `unbalance`, `graph_name`, and `normalization_name`.

An example CSV file is available [here](https://github.com/LucaCappelletti94/barplots/blob/master/tests/test_case.csv).

## Usage Examples

Below are examples of common usages. Each graph either displays the same data or a mean based on the provided grouping indices. Choose the representation that best visualizes your data, as there is no universally superior format.

> **Note**: The data in these examples is **randomly generated** and is intended only for test purposes. **DO NOT** consider these values as valid results.

For all examples, load the DataFrame `df` as follows:

```python
import pandas as pd
df = pd.read_csv("tests/test_case.csv")
```

And the `custom_defaults` used to sanitize labels specific to this dataset:
>>>>>>> 6fc1cff (Working on MyPy support)

```python
custom_defaults = {
    "P": "promoters",
    "E": "enhancers",
    "A": "active ",
    "I": "inactive ",
    "+": " and ",
    "": "anything",
<<<<<<< HEAD
    "Validation": "val"
=======
    "Validation":"val"
>>>>>>> 6fc1cff (Working on MyPy support)
}
```

### Horizontal Example A

<<<<<<< HEAD
In the following example, we will plot the bars horizontally, rotating the group labels by 90 degrees, and displaying the bar labels as a shared legend.

```python
from barplots import barplots
import pandas as pd

df = pd.read_csv("tests/test_case.csv")
custom_defaults = {
    "P": "promoters",
    "E": "enhancers",
    "A": "active ",
    "I": "inactive ",
    "+": " and ",
    "": "anything",
    "Validation": "val"
}
=======
This example plots horizontal bars with group labels rotated by 90 degrees and displays the bar labels in a shared legend.

```python
from barplots import barplots
>>>>>>> 6fc1cff (Working on MyPy support)

barplots(
    df,
    groupby=["task", "model"],
    orientation="horizontal",
    show_legend=True,
    minor_rotation=90,
    custom_defaults=custom_defaults
)
```

Result can be seen [here](https://github.com/LucaCappelletti94/barplots/blob/master/examples/1/horizontal_legend_minor_rotation_val_auroc.png?raw=true).

### Horizontal Example B

<<<<<<< HEAD
In this example, we will plot the top index as multiple subplots with horizontal bars, rotating the group labels by 90 degrees, and displaying the bar labels as a shared legend.

```python
from barplots import barplots
import pandas as pd

df = pd.read_csv("tests/test_case.csv")
custom_defaults = {
    "P": "promoters",
    "E": "enhancers",
    "A": "active ",
    "I": "inactive ",
    "+": " and ",
    "": "anything",
    "Validation": "val"
}
=======
This example creates multiple subplots with horizontal bars, rotating group labels by 90 degrees and displaying bar labels as a shared legend.

```python
from barplots import barplots
>>>>>>> 6fc1cff (Working on MyPy support)

barplots(
    df,
    groupby=["cell_line", "task", "model"],
    orientation="horizontal",
    show_legend=True,
    subplots=True,
    minor_rotation=90,
    custom_defaults=custom_defaults
)
```

![Horizontal Example B](https://github.com/LucaCappelletti94/barplots/blob/master/examples/1/horizontal_legend_subplots_minor_rotation_val_auroc.png?raw=true)

### Horizontal Example C

<<<<<<< HEAD
In this example, we will plot horizontal bars, rotating the top group labels by 90 degrees, and displaying the bar labels as minor ticks.

```python
from barplots import barplots
import pandas as pd

df = pd.read_csv("tests/test_case.csv")
custom_defaults = {
    "P": "promoters",
    "E": "enhancers",
    "A": "active ",
    "I": "inactive ",
    "+": " and ",
    "": "anything",
    "Validation": "val"
}
=======
This example shows horizontal bars, with the top group labels rotated by 90 degrees, and displays the bar labels as minor ticks.

```python
from barplots import barplots
>>>>>>> 6fc1cff (Working on MyPy support)

barplots(
    df,
    groupby=["task", "model"],
    orientation="horizontal",
    show_legend=False,
    major_rotation=90,
    custom_defaults=custom_defaults
)
```

Result can be seen [here](https://github.com/LucaCappelletti94/barplots/blob/master/examples/1/horizontal_major_rotation_val_auroc.png?raw=true).

### Horizontal Example D

<<<<<<< HEAD
In this example, we will plot the top index as multiple subplots with horizontal bars, rotating the group labels by 90 degrees, and displaying the bar labels as minor ticks.

```python
from barplots import barplots
import pandas as pd

df = pd.read_csv("tests/test_case.csv")
custom_defaults = {
    "P": "promoters",
    "E": "enhancers",
    "A": "active ",
    "I": "inactive ",
    "+": " and ",
    "": "anything",
    "Validation": "val"
}
=======
This example plots multiple subplots with horizontal bars, rotating group labels by 90 degrees and displaying bar labels as minor ticks.

```python
from barplots import barplots
>>>>>>> 6fc1cff (Working on MyPy support)

barplots(
    df,
    groupby=["cell_line", "task", "model"],
    orientation="horizontal",
    show_legend=False,
    major_rotation=90,
    subplots=True,
    custom_defaults=custom_defaults
)
```

![Horizontal Example D](https://github.com/LucaCappelletti94/barplots/blob/master/examples/1/horizontal_subplots_major_rotation_val_auroc.png?raw=true)

### Vertical Example A

<<<<<<< HEAD
In this example, we will plot the bars vertically and display the bar labels as a shared legend.

```python
from barplots import barplots
import pandas as pd

df = pd.read_csv("tests/test_case.csv")
custom_defaults = {
    "P": "promoters",
    "E": "enhancers",
    "A": "active ",
    "I": "inactive ",
    "+": " and ",
    "": "anything",
    "Validation": "val"
}
=======
This example plots vertical bars and displays the bar labels as a shared legend.

```python
from barplots import barplots
>>>>>>> 6fc1cff (Working on MyPy support)

barplots(
    df,
    groupby=["task", "model"],
    orientation="vertical",
    show_legend=True,
    custom_defaults=custom_defaults
)
```

Result can be seen [here](https://github.com/LucaCappelletti94/barplots/blob/master/examples/1/vertical_legend_val_auroc.png).

### Vertical Example B

<<<<<<< HEAD
In this example, we will plot the top index as multiple subplots with vertical bars, displaying the bar labels as a shared legend.

```python
from barplots import barplots
import pandas as pd

df = pd.read_csv("tests/test_case.csv")
custom_defaults = {
    "P": "promoters",
    "E": "enhancers",
    "A": "active ",
    "I": "inactive ",
    "+": " and ",
    "": "anything",
    "Validation": "val"
}
=======
In this example, we plot multiple subplots with vertical bars and display the bar labels as a shared legend.

```python
from barplots import barplots
>>>>>>> 6fc1cff (Working on MyPy support)

barplots(
    df,
    groupby=["cell_line", "task", "model"],
    orientation="vertical",
    show_legend=True,
    subplots=True,
    custom_defaults=custom_defaults
)
```

![Vertical Example B](https://github.com/LucaCappelletti94/barplots/blob/master/examples/1/vertical_legend_subplots_val_auroc.png)

### Vertical Example C

<<<<<<< HEAD
In this example, we will plot vertical bars, rotating the minor group labels by 90 degrees, and displaying the bar labels as minor ticks.

```python
from barplots import barplots
import pandas as pd

df = pd.read_csv("tests/test_case.csv")
custom_defaults = {
    "P": "promoters",
    "E": "enhancers",
    "A": "active ",
    "I": "inactive ",
    "+": " and ",
    "": "anything",
    "Validation": "val"
}
=======
Here, we plot vertical bars with the minor group labels rotated by 90 degrees, displaying bar labels as minor ticks.

```python
from barplots import barplots
>>>>>>> 6fc1cff (Working on MyPy support)

barplots(
    df,
    groupby=["task", "model"],
    orientation="vertical",
    show_legend=False,
    minor_rotation=90,
    custom_defaults=custom_defaults
)
```

Result can be seen [here](https://github.com/LucaCappelletti94/barplots/blob/master/examples/1/vertical_minor_rotation_val_auroc.png).

### Vertical Example D

<<<<<<< HEAD
In this example, we will plot the top index as multiple subplots with vertical bars, rotating the minor group labels by 90 degrees, and displaying the bar labels as minor ticks.

```python
from barplots import barplots
import pandas as pd

df = pd.read_csv("tests/test_case.csv")
custom_defaults = {
    "P": "promoters",
    "E": "enhancers",
    "A": "active ",
    "I": "inactive ",
    "+": " and ",
    "": "anything",
    "Validation": "val"
}
=======
This example shows multiple subplots with vertical bars, rotating minor group labels by 90 degrees, and displays bar labels as minor ticks.

```python
from barplots import barplots
>>>>>>> 6fc1cff (Working on MyPy support)

barplots(
    df,
    groupby=["cell_line", "task", "model"],
    orientation="vertical",
    show_legend=False,
    minor_rotation=90,
    subplots=True,
    custom_defaults=custom_defaults
)
```

![Vertical Example D](https://github.com/LucaCappelletti94/barplots/blob/master/examples/1/vertical_subplots_minor_rotation_val_auroc.png)
<<<<<<< HEAD
=======

## Future Features

Automatic detection and rotation of overlapping labels are planned features. Currently, you can adjust label orientation manually with `minor_rotation` and `major_rotation`.
>>>>>>> 6fc1cff (Working on MyPy support)
