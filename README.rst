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

Usage examples
----------------------------------------------
Here follows a set of examples of common usages. Basically, every graph show either the same data
or a mean based on the provided group by indices. Choose whetever representation is best for
visualizing your data, as hardly one is better than another for every possible dataset.

N.B. The data used in the following examples as **randomly generated** so to be useful for test porposes.
**DO NOT** consider these values as valid results for experiments using the same labels (cell lines etc...)
which are only used to show possible usages.

For every example, the considered dataframe :code:`df` is loaded as follows:

.. code:: python

    import pandas as pd
    
    df = pd.read_csv("tests/test_case.csv")

Example B
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the following example we will plot the bars horizontally, rotating the group labels by 90 degrees and
displaying the bar labels as a shared legend.

.. code:: shell

    from barplots import barplots

    barplots(
        df
    )

.. image:: https://github.com/LucaCappelletti94/barplots/blob/master/examples/horizontal_legend_minor_rotation_val_auroc.jpg?raw=true
    :width: 100px
    :align: center 

This will output the following images (just a few examples reported here):

.. image:: https://github.com/LucaCappelletti94/barplots/blob/master/examples/test_auroc.jpg?raw=true
    :width: 800 px

.. image:: https://github.com/LucaCappelletti94/barplots/blob/master/examples/test_auprc.jpg?raw=true
    :width: 800 px

.. image:: https://github.com/LucaCappelletti94/barplots/blob/master/examples/required_time.jpg?raw=true
    :width: 800 px


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