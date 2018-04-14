"""
This module is called 'utils' because it owns miscellaneous methods that can come in handy
in different scenarios throughout the project/application.

For instance, statistics methods, subroutines for main methods in main, etc.
"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

from main import SUGESTIOCLIENT, LOG_STATUS


def delete_all_consumptions_user(userID):
    """
    Deletes all consumptions made by user identified by userID.
    :param userID: int number of the user identifier
    :return:
    """


def get_rating(userID, movieID):
    """
    Retrieves the consumption from the recommender service provided the user ID.
    :param userID: int number of the user identifier
    :param movieID: int number of the movie identifier
    :return: the rating. It returns a list with a single item containing tuples accessed as attributes of an object
    """
    s, rating = SUGESTIOCLIENT.get_user_consumptions(userID, movieID)
    if s == 200 or s == 202:
        if LOG_STATUS is True:
            print "[", s, "]: Movie rating retrieved successfully!"
        return s, rating
    else:
        print "[", str(s), "]: Something went wrong."
        return s


def decode_stars(detailfield):
    """
    Decodes the stars rating from the provided parameter
    :param detailfield: string representation of the rating for a certain movie
    :return: float of the rating
    """
    return float(detailfield.split(':')[3])
