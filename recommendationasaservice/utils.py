"""
This module is called 'utils' because it owns miscellaneous methods that can come in handy
in different scenarios throughout the project/application.

For instance, statistics methods, subroutines for main methods in main, etc.
"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"


def plot_top10_rated_distribution(movies, ratings):
    """
    Plots a distribution of top10 rated movies.
    :param movies: ten most rated movies' names.
    :param ratings: ten most rated movies' aggregated ratings
    :return:
    """
    print movies
    print ratings
    plt.rcParams.update({'figure.autolayout': True})
    plt.figure(figsize=(10, 4))
    plt.barh(range(len(movies)), ratings)
    plt.yticks(range(len(movies)), movies)
    plt.gca().invert_yaxis()
    plt.ylabel("Movies")
    plt.xlabel("Amount of ratings")
    plt.show()