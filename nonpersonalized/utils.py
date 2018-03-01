"""
This module is called 'utils' because it owns miscellaneous methods that can come in handy
in different scenarios throughout the project/application.

For instance, plotting charts.
"""

import matplotlib.pyplot as plt
import operator  # used to sort the (key,value) pairs of a dictionary

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"


def plot_top10_rated_distribution(movies, ratings):
    """
    Plots a distribution of top10 rated movies.
    :param movies: a collection of movies (mainly used for the names, instead of using IDs)
    :param ratings: a collection of ratings
    :return:
    """
    aggregated_ratings = {}
    top10_movies = []
    top10_ratings = []
    # Now, we will iterate over all ratings and we will aggregate/count all ratings for every movie:
    for elem in ratings:
        if not elem['movieid'] in aggregated_ratings:
            aggregated_ratings[elem['movieid']] = 1
        else:
            aggregated_ratings[elem['movieid']] += 1
    print "Num elements (aggregated dictionary): ", len(aggregated_ratings)
    # 'sorted' function sorts the dictionary from small to big, returns a list:
    mysorted = sorted(aggregated_ratings.items(), key=operator.itemgetter(1))
    # We take the last 10 elements from the tail:
    mysorted = mysorted[-10:]
    # We reverse the order of the items within the list:
    mysorted.reverse()
    # print mysorted
    for elem in mysorted:
        top10_movies.append(movies[elem[0]]['title'])
        top10_ratings.append(elem[1])
    print top10_movies
    print top10_ratings
    plt.rcParams.update({'figure.autolayout': True})
    plt.figure(figsize=(10, 4))
    plt.barh(top10_movies, top10_ratings)
    plt.ylabel("Movies")
    plt.xlabel("Amount of ratings")
    plt.show()