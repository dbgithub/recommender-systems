"""
This module is called 'utils' because it owns miscellaneous methods that can come in handy
in different scenarios throughout the project/application.

For instance, plotting charts, declaration of subroutines used in main, etc.
"""

import matplotlib.pyplot as plt
import globals  # a file to store global variables to use them across all Python files

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
    plt.barh(movies, ratings)
    plt.ylabel("Movies")
    plt.xlabel("Amount of ratings")
    plt.show()


def how_many_Z(movieID, ratings):
    """
    Computes how many instances (ratings) are done for movieID.
    It's named: "how_many_Z" because it's valid to calculate the amount of ratings for every movie ID (not just X or Y).
    :param movieID: movie ID from which we want to know how many ratings were done
    :param ratings: a collection of all ratings
    :return: returns an integer.
    """
    counter = 0
    movieID = str(movieID) #TODO: it depends on the final implementation of the Recommender System, this might not be necessary anymore
    for rating in ratings:
        if rating['movieid'] == movieID:
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
    counter = 0
    ratings_by_user = globals.RATINGS_BY_USER
    if ratings_by_user is None:
        ratings_by_user = extract_ratings_by_user(ratings)
    movieX_ID = str(movieX_ID) #TODO: it depends on the final implementation of the Recommender System, this might not be necessary anymore
    movieY = str(movieY) #TODO: it depends on the final implementation of the Recommender System, this might not be necessary anymore
    for user in ratings_by_user.values():
        if len(user) is not 0:
            movieids = [rating['movieid'] for rating in user]
            if movieX_ID in movieids and movieY in movieids:
                counter += 1
            # Another way of implementing it:
            # x_found = False
            # y_found = False
            # for rating in user:
            #     if rating['movieid'] == movieX_ID:
            #         x_found = True
            #     elif rating['movieid'] == movieY:
            #         y_found = True
            #     if x_found and y_found:
            #         counter += 1
            #         break
    return counter


def extract_ratings_by_user(ratings):
    """
    It iterates all ratings and for each user it collects all his/her ratings in a list format.
    It returns a dictionary with "Key=userID" and "Value=the rating object itself".
    :param ratings: a collection of all ratings
    :return: a dictionary with "Key=userID" and "Value=the rating object itself".
    """
    ratings_by_user = {}
    for rating in ratings:
        if rating['userid'] in ratings_by_user:
            ratings_by_user[rating['userid']].append(rating)
        else:
            ratings_by_user[rating['userid']] = []
    return ratings_by_user
