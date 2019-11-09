histograms
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Python package to easily make histograms from multi-indexed dataframes.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install histograms

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Usage examples
----------------------------------------------
The library offers two main methods: :code:`histogram`, for plotting a single histogram, and  :code:`histograms`, for plotting
a number of histograms in parallel fashion.

Histograms
~~~~~~~~~

.. code:: python

    from histograms import histograms
    df = pd.read_csv("tests/test_case.csv", index_col=0)
    histograms(df, ["dataset", "resource", "model"])

This will output the following images (just a few examples reported here):

.. image:: https://github.com/LucaCappelletti94/histograms/blob/master/examples/test_auroc.jpg?raw=true
    :width: 800 px

.. image:: https://github.com/LucaCappelletti94/histograms/blob/master/examples/test_auprc.jpg?raw=true
    :width: 800 px

.. image:: https://github.com/LucaCappelletti94/histograms/blob/master/examples/required_time.jpg?raw=true
    :width: 800 px

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/histograms.png
   :target: https://travis-ci.org/LucaCappelletti94/histograms
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_histograms&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_histograms
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_histograms&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_histograms
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_histograms&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_histograms
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/histograms/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/histograms?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/histograms.svg
    :target: https://badge.fury.io/py/histograms
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/histograms
    :target: https://pepy.tech/badge/histograms
    :alt: Pypi total project downloads 

.. |codacy|  image:: https://api.codacy.com/project/badge/Grade/bc5f6f65d4ed4708a5efc47205b8e6d4
    :target: https://www.codacy.com/manual/LucaCappelletti94/histograms?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/histograms&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/9db2a6413e6aa2c7f0b4/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/histograms/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/9db2a6413e6aa2c7f0b4/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/histograms/test_coverage
    :alt: Code Climate Coverate