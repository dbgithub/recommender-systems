"""
This module is called 'utils' because it owns miscellaneous methods that can come in handy
in different scenarios throughout the project/application.

For instance, statistics methods, subroutines for main methods in main, etc.
"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"


def find_common_ratings(ratings, userAid, userUid):
    """
    Finds the movies that were rated by both users given by parameters and collects
    their ratings.
    :param ratings: list of ratings
    :param userAid: int number of user A
    :param userUid: int number of user U
    :return: a dictionary with "Key=int number of the user" and "Value=list of ratings of the user"
    """
    ratings_by_user = extract_ratings_by_user(ratings)
    ratingsA = ratings_by_user[userAid]
    ratingsU = ratings_by_user[userUid]
    common_ratings = {}
    common_ratings[userAid] = ratingsA
    common_ratings[userUid] = ratingsU
    return common_ratings


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