"""
This module is called 'utils' because it owns miscellaneous methods that can come in handy
in different scenarios throughout the project/application.

For instance, statistics methods, subroutines for main methods in main, etc.
"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

import globals  # a file to store global variables to use them across all Python files


def find_common_ratings(userAid, userUid, ratings):
    """
    Finds the movies that were rated by both users given by parameters and collects
    their ratings.
    :param userAid: int number of user A
    :param userUid: int number of user U
    :param ratings: list of ratings
    :return: a dictionary with "Key=int number of the user" and "Value=list of ratings of the user" AND amount of common items
    """
    # First, retrieve all the ratings made by both users:
    if globals.RATINGS_BY_USER is not None:
        ratingsA = globals.RATINGS_BY_USER[userAid]
        ratingsU = globals.RATINGS_BY_USER[userUid]
    else:
        if ratings is None:
            raise ValueError("[Error] 'ratings' is none! Cannot continue with the method!")
        ratings_by_user = extract_ratings_by_users(ratings)
        ratingsA = ratings_by_user[userAid]
        ratingsU = ratings_by_user[userUid]
    # Secondly, perform the intersection between the retrieved ratings.
    # For that, we will use Sets: a Set is an unordered collection with no duplicate elements.
    # Before that, we will truncate the ratings of both users into another representation to make the computation easier and faster towards run-time.
    # For that, we will translate current ratings model into a dictionary with "Key=movieID" and "Value=rating object" just for the two provided users.

    def truncate(mydict, rating):
        """
        It saves the provided rating object in the provided dictionary stored by 'movieID'.
        In other words: "Key=movieID" and "Value=rating object"
        :param mydict: a dictionary where we want to store the rating object
        :param rating: a rating object that is desired to be stored in the dictionary
        :return: nothing
        """
        mydict[rating['movieid']] = rating

    # Now we declare two dictionaries corresponding to both users. These dictionaries will store all their corresponding
    # ratings with "Key=movieID" and "Value=rating object"
    ratingsA_by_movieID = {}
    ratingsU_by_movieID = {}
    for rating in ratingsA:
        truncate(ratingsA_by_movieID, rating)  # we apply truncate over ratings of user A
    for rating in ratingsU:
        truncate(ratingsU_by_movieID, rating)  # we apply truncate over ratings of user U
    movieIDs_rated_by_both = set(ratingsA_by_movieID.keys()) & set(ratingsU_by_movieID.keys())  # intersection!!
    if globals.LOG_STATUS is True:
        print "Common movie IDs between user {0} and {1}:".format(userAid,userUid), movieIDs_rated_by_both
    common_ratings = {}
    common_ratings[userAid] = []
    common_ratings[userUid] = []
    # Finally, we iterate over the movieIDs that both users have in common and we store their corresponding rating
    # object in a dictionary.
    for movieid in movieIDs_rated_by_both:
        common_ratings[userAid].append(ratingsA_by_movieID[movieid])
        common_ratings[userUid].append(ratingsU_by_movieID[movieid])
    return common_ratings, len(movieIDs_rated_by_both)


def extract_ratings_by_users(ratings):
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