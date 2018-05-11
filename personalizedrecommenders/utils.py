"""
This module is called 'utils' because it owns miscellaneous methods that can come in handy
in different scenarios throughout the project/application.

For instance, statistics methods, subroutines for main methods in main, etc.
"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

import globals  # a file to store global variables to use them across all Python files
from main import calculate_mean_ratings_for_item


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
            ratings_by_user[rating['userid']].append(rating)
    return ratings_by_user


def extract_ratings_by_users_map(ratings):
    """
    It iterates over all ratings and for each user it collects all his/her ratings in a dictionary.
    It returns a dictionary with "Key=userID" and "Value=a Dictionary with 'Key=itemID' and 'Value=rating (stars)'".
    :param ratings: a collection of all ratings
    :return: a dictionary with "Key=userID" and "Value=a Dictionary with 'Key=itemID' and 'Value=rating (stars)'".
    """
    if globals.RATINGS_BY_USER is None:
        globals.RATINGS_BY_USER = extract_ratings_by_users(ratings)
    ratings_by_user_map = {}
    for key in globals.RATINGS_BY_USER.keys():
        ratings_user = globals.RATINGS_BY_USER[key]
        if len(ratings_user) != 0:  # this means the user has rated some items
            ratings_by_user_map[key] = {}
            for rating in ratings_user:
                ratings_by_user_map[key][rating['movieid']] = rating['rating']
    return ratings_by_user_map


def extract_ratings_x_by_users(movies, ratings):
    """
    For each item ID it collects all the ratings done by the users who rated that item.
    :param movies: list of ALL movies
    :param ratings: list of ALL ratings
    :return: a dictionary with "Key=itemID" and "Value=list of ratings for that item by all user who rated it"
    """
    # Firstly, we collect all the item IDs of all movies to iterate over them later on:
    itemIDs = [int(movie['id']) for movie in movies.values()]
    ratings_x_by_users = {}

    for itemid in itemIDs:
        ratings_x_by_users[itemid] = []
        if globals.LOG_STATUS is True:
            print "ITEM ID: ", itemid
        for rating in ratings:
            if rating['movieid'] == itemid:
                # Put it into the dictionary
                ratings_x_by_users[itemid].append(rating)
                if globals.LOG_STATUS is True:
                    print "\t| rating: ", rating
    return ratings_x_by_users


def extract_mean_ratings(movies):
    """
    It calculates the mean of the ratings of all users who rated this item
    :param movies: list of ALL movies
    :return: a dictionary with "Key=itemID" and "Value=average of the ratings of all users who rated this item"
    """
    if globals.RATINGS_X_BY_USERS is None:
        raise ValueError("[Error] RATINGS_X_BY_USERS is none! Cannot continue with the method!")

    # Firstly, we collect all the item IDs of all movies to iterate over them later on:
    itemIDs = [int(movie['id']) for movie in movies.values()]
    mean_ratings = {}

    for itemid in itemIDs:
        try:
            mean = calculate_mean_ratings_for_item(itemid, globals.RATINGS_X_BY_USERS[itemid], None)  # compute the mean
        except KeyError:
            continue
        # Put it into the dictionary
        mean_ratings[itemid] = mean
    return mean_ratings