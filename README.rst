barplots
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Python package to easily make barplots from multi-indexed dataframes.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install barplots

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|


Documentation
----------------------------------------------
Most methods, in particular those exposed to user usage, are provided with doc strings.
Consider reading these docstrings for learning the most recent updates to the library.

Usage examples
----------------------------------------------
Here follows a set of examples of common usages. Basically, every graph show either the same data
or a mean based on the provided group by indices. Choose whetever representation is best for
visualizing your data, as hardly one is better than another for every possible dataset.

N.B. The data used in the following examples are **randomly generated** so to be useful for test porposes.
**DO NOT** consider these values as valid results for experiments using the same labels (cell lines etc...)
which are only used to show possible usages.

For every example, the considered dataframe :code:`df` is loaded as follows:

.. code:: python

    import pandas as pd

    df = pd.read_csv("tests/test_case.csv")


Also, for every example, the :code:`custom_defaults` used to sanitize the labels specific to the used dataset is:

.. code:: python

    custom_defaults = {
        "P": "promoters",
        "E": "enhancers",
        "A": "active ",
        "I": "inactive ",
        "+": " and ",
        "": "anything",
        "Validation":"val"
    }


Horizontal Example A
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the following example we will plot the bars horizontally, rotating the group labels by 90 degrees and
displaying the bar labels as a shared legend.

.. code:: python

    from barplots import barplots

    barplots(
        df,
        groupby=["task","model"],
        orientation="horizontal",
        show_legend=True,
        minor_rotation=90,
        custom_defaults=custom_defaults
    )

Result can be seen `here <https://github.com/LucaCappelletti94/barplots/blob/master/examples/horizontal_legend_minor_rotation_val_auroc.png?raw=true>`__.


Horizontal Example B
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the following example we will plot the top index as multiple
subplots with horizontal bars, rotating the group labels by 90 degrees and
displaying the bar labels as a shared legend.

.. code:: python

    from barplots import barplots

    barplots(
        df,
        groupby=["cell_line", "task","model"],
        orientation="horizontal",
        show_legend=True,
        subplots=True,
        minor_rotation=90,
        custom_defaults=custom_defaults
    )

.. image:: https://github.com/LucaCappelletti94/barplots/blob/master/examples/horizontal_legend_subplots_minor_rotation_val_auroc.png?raw=true


Horizontal Example C
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the following example we will plot horizontal bars, rotating the top group labels by 90 degrees and
displaying the bar labels as minor ticks.

.. code:: python

    from barplots import barplots

    barplots(
        df,
        groupby=["task","model"],
        orientation="horizontal",
        show_legend=False,
        major_rotation=90,
        custom_defaults=custom_defaults
    )

Result can be seen `here <https://github.com/LucaCappelletti94/barplots/blob/master/examples/horizontal_major_rotation_val_auroc.png?raw=true>`__


Horizontal Example D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the following example we will plot the top index as multiple
subplots with horizontal bars, rotating the group labels by 90 degrees and
displaying the bar labels as minor ticks.

.. code:: python

    from barplots import barplots

    barplots(
        df,
        groupby=["cell_line", "task","model"],
        orientation="horizontal",
        show_legend=False,
        major_rotation=90,
        subplots=True,
        custom_defaults=custom_defaults
    )

.. image:: https://github.com/LucaCappelletti94/barplots/blob/master/examples/horizontal_subplots_major_rotation_val_auroc.png?raw=true


Vertical Example A
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the following example we will plot the bars vertically and
displaying the bar labels as a shared legend.

.. code:: python

    from barplots import barplots

    barplots(
        df,
        groupby=["task","model"],
        orientation="vertical",
        show_legend=True,
        custom_defaults=custom_defaults
    )

Result can be seen `here <https://github.com/LucaCappelletti94/barplots/blob/master/examples/vertical_legend_val_auroc.png>`__


Vertical Example B
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the following example we will plot the top index as multiple
subplots with vertical bars  and displaying the bar labels as a shared legend.

.. code:: python

    from barplots import barplots

    barplots(
        df,
        groupby=["cell_line", "task","model"],
        orientation="vertical",
        show_legend=True,
        subplots=True,
        custom_defaults=custom_defaults
    )

.. image:: https://github.com/LucaCappelletti94/barplots/blob/master/examples/vertical_legend_subplots_val_auroc.png


Vertical Example C
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the following example we will plot vertical bars, rotating the minor group labels by 90 degrees and
displaying the bar labels as minor ticks.

.. code:: python

    from barplots import barplots

    barplots(
        df,
        groupby=["task","model"],
        orientation="vertical",
        show_legend=False,
        minor_rotation=90,
        custom_defaults=custom_defaults
    )

Result can be seen `here <https://github.com/LucaCappelletti94/barplots/blob/master/examples/vertical_minor_rotation_val_auroc.png>`__


Vertical Example D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the following example we will plot the top index as multiple
subplots with vertical bars, rotating the minor group labels by 90 degrees and
displaying the bar labels as minor ticks.

.. code:: python

    from barplots import barplots

    barplots(
        df,
        groupby=["cell_line", "task","model"],
        orientation="vertical",
        show_legend=False,
        minor_rotation=90,
        subplots=True,
        custom_defaults=custom_defaults
    )

.. image:: https://github.com/LucaCappelletti94/barplots/blob/master/examples/vertical_subplots_minor_rotation_val_auroc.png


Future features
---------------
Currently it is not possible to automatically detect labels overlap and rotate them.
I will work on this feature when I get the time, currently you will need to use the parameters :code:`minor_rotation` and :code:`major_rotation`.

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/barplots.png
   :target: https://travis-ci.org/LucaCappelletti94/barplots
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_barplots&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_barplots
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_barplots&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_barplots
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_barplots&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_barplots
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/barplots/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/barplots?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/barplots.svg
    :target: https://badge.fury.io/py/barplots
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/barplots
    :target: https://pepy.tech/badge/barplots
    :alt: Pypi total project downloads 

.. |codacy|  image:: https://api.codacy.com/project/badge/Grade/bc5f6f65d4ed4708a5efc47205b8e6d4
    :target: https://www.codacy.com/manual/LucaCappelletti94/barplots?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/barplots&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/9db2a6413e6aa2c7f0b4/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/barplots/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/9db2a6413e6aa2c7f0b4/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/barplots/test_coverage
    :alt: Code Climate Coverate