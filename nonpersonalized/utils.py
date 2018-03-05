"""
This module is called 'utils' because it owns miscellaneous methods that can come in handy
in different scenarios throughout the project/application.

For instance, plotting charts, declaration of subroutines used in main, etc.
"""

import matplotlib.pyplot as plt

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"


def plot_top10_rated_distribution(movies, ratings):
    """
    Plots a distribution of top10 rated movies.
    :param movies: ten most rated movies' names.
    :param ratings: ten most rated movies' ratings
    :return:
    """
    print movies
    print ratings
    plt.rcParams.update({'figure.autolayout': True})
    plt.figure(figsize=(10, 4))
    plt.barh(movies, ratings)
    plt.ylabel("Movies")
    plt.xlabel("Amount of ratings")
    plt.show()


def how_many_Z(movieID, ratings):
    """
    Computes how many instances (ratings) are done for movieID.
    It's named: "how_many_Z" because it's valid to calculate the amount of ratings for every movie ID.
    :param movieID: movie ID from which we want to know how many ratings were done
    :param ratings: a collection of all ratings
    :return: returns an integer.
    """
    counter = 0
    for rating in ratings:
        if rating['movieid'] is movieID:
            counter += 1
    return counter

def how_many_X_and_Y(movieX_ID, movieY, ratings):
    """
    Computes how many users rated movie X and movie Y as well.
    :param movieX_ID: a movie ID
    :param movieY: another movie ID
    :param ratings: a collection of all ratings
    :return: returns an integer.
    """