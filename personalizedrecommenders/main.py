"""
This file is the main file. Main methods for personalized recommender system can be found here.

"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

import numpy as np
import data
import utils
import operator  # used to sort the (key,value) pairs of a dictionary
import globals  # a file to store global variables to use them across all Python files

MOVIE_PICKLE_LOCATION = "movies_pickle_06-05-2018--23-43-45.pkl"
RATINGS_PICKLE_LOCATION = "ratings_pickle_06-05-2018--23-43-45.pkl"
CUT_OFF = 10  # gamma corresponds to the cut-off value of the significance weighting


def calculate_pearson_correlation(common_ratings, userAid, userUid):
    """
    Calculates Pearson correlation.
    If both users have 1 or 0 items in common => return 0
    If denominator is 0 => return 0
    :param common_ratings: a dictionary with "Key=userID" and "Value=list of rating objects"
    :param userAid: int number of the id of user A
    :param userUid: int number of the id of user B
    :return: float number, weight of Pearson correlation
    """
    if len(common_ratings[userAid]) in [0,1] and len(common_ratings[userUid]) in [0,1]:
        return 0.0
    if globals.RATINGS_BY_USER is None:
        raise ValueError("[Error] RATINGS_BY_USER is none! Cannot continue with the method!")
    ratings_by_user_A = globals.RATINGS_BY_USER[userAid]
    ratings_by_user_U = globals.RATINGS_BY_USER[userUid]
    mean_ratings_A = calculate_mean_ratings(userAid, ratings_by_user_A)
    mean_ratings_U = calculate_mean_ratings(userUid, ratings_by_user_U)
    d_a = calculate_user_mean_centered_rating(ratings_by_user_A, mean_ratings_A) # this is the calculation of one part of the formula
    d_u = calculate_user_mean_centered_rating(ratings_by_user_U, mean_ratings_U) # this is the calculation of one part of the formula
    # Calculation of denominator:
    denominator = float(np.sqrt(d_a) * np.sqrt(d_u))
    if denominator == 0.0:
        return 0.0
    # Calculation of numerator:
    numerator = 0.0
    for tuple1, tuple2 in zip(common_ratings[userAid], common_ratings[userUid]):
        numerator += float(tuple1['rating']-mean_ratings_A)*float(tuple2['rating']-mean_ratings_U)
    return numerator/denominator


def calculate_mean_ratings(userID, ratings_by_user=None):
    """
    Calculates the average of the ratings of the user given by parameter
    :param userID: int number of the id of the user
    :param ratings_by_user: list of ratings by the user. It's provided to speed-up execution in run-time
    :return: float number, average of the ratings
    """
    # To avoid excessive computation during run-time, the user ratings are provided by parameter.
    # If it's not none, then it can be used, otherwise we need to calculate it.
    if ratings_by_user is not None:
        return np.mean([rating['rating'] for rating in ratings_by_user])
    else:
        if globals.RATINGS_BY_USER is not None:
            tmp = globals.RATINGS_BY_USER[userID]
            return np.mean([rating['rating'] for rating in tmp])
        else:
            raise ValueError("[Error] RATINGS_BY_USER is none! Cannot continue with the method!")


def calculate_user_mean_centered_rating(ratings_user, avgRatingUser):
    """
    Calculates the centered mean rating of a certain user over a subset of his ratings
    :param ratings_user: some ratings of the user. Ratings over which we want to calculate user mean centered rating.
    :param avgRatingUser: mean ratings of the user
    :return: float number
    """
    sum = 0.0
    for rating in ratings_user:
        sum = sum + pow(rating['rating']-avgRatingUser, 2)
    return sum


def calculate_significance_weighing_factor(userAid, userUid, ratings):
    """
    Calculates the significance weighing
    :param userAid: a list of ALL ratings
    :param userAid: int number of user A
    :param userUid: int number of user B
    :return: float number
    """
    common_ratings, amount = utils.find_common_ratings(userAid, userUid, ratings)
    return float(min(CUT_OFF, amount))/float(CUT_OFF)


def intersection_ratings_users(ratingsA, ratingsU):
    # TODO: delete this function???
    """
    Intersects both ratings sets to find the common ratings by both users
    :param ratingsA: list of ratings of user A
    :param ratingsU: list of ratings of user B
    :return: list of ratings
    """

def rating_prediction_user(userAid,itemID, neighborsIDs):
    """
    Calculates the rating prediction for user A and item 'itemID' based on the nearest neighbors.
    For UUCF, we only consider neighbors with positive similarity value.
    :param userAid: int number of user A
    :param itemID: int number of the item
    :param neighborsIDs: list of the nearest neighbors IDs
    :return: float number
    """
    if globals.RATINGS_BY_USER is None:
        raise ValueError("[Error] RATINGS_BY_USER is none! Cannot continue with the method!")
    ratings_by_user_A = globals.RATINGS_BY_USER[userAid]  # list of ALL ratings by user U
    mean_ratings_A = calculate_mean_ratings(userAid, ratings_by_user_A)  # mean ratings of user U

    # WATCH OUT! To save time and computation resources, there is no need to calculate the Pearson correlation
    # as many times as it appears in the formula.
    # A numerator and denominator have to be calculated: it would be convenient to collect the corresponding
    # Pearson correlations once and use it either in numerator and denominator later on
    # Unfortunately there is too much computation overhead with respect user U
    numerator = 0.0
    denominator = 0.0
    # If the target item has not been rated by anyone else, then, we return the mean rating of user A:
    if len(neighborsIDs) == 0:
        return mean_ratings_A
    for userUid in neighborsIDs:
        common_ratings, amount = utils.find_common_ratings(userAid, userUid, None)  # common ratings
        pearson_value = calculate_pearson_correlation(common_ratings, userAid, userUid)  # calculation of Pearson correlation
        ratings_by_user_U = globals.RATINGS_BY_USER[userUid]  # list of ALL ratings by user U
        mean_ratings_U = calculate_mean_ratings(userUid, ratings_by_user_U)  # mean ratings of user U
        # Find the rating of user U for item 'itemID':
        for rating in ratings_by_user_U:
            if rating['movieid'] == itemID:
                rating_u_i = rating['rating']
        numerator = numerator + ((rating_u_i-mean_ratings_U)*pearson_value)
        denominator = denominator + pearson_value # updating the denominator with accumulative Pearson correlation values
    return mean_ratings_A + (float(numerator)/float(denominator))


def top_k_most_similar_neighbors(userID, itemID, k=20):
    """
    Retrieves the most similar neighbors of user 'userID' with respect to item 'itemID'
    :param userID: int number of the user
    :param itemID: int number of the item
    :param k: int number ideal number of neighbors to find
    :return: list of ints of neighbors IDs
    """
    # TODO: don't forget AITOR to use/multiply significance weighing!!!!!!!
    # TODO: ONLY TAKE INTO ACCOUNT POSITIVE values, not negatives!

    # dictionary with "Key=userID" and "Value=...?????":
    neighbors_data = {}  # TODO: to delete?
    neighborsIDs = []  # a list of ints containing the user IDs of all approved/valid neighbors
    # list of tuples with the following content: ("userID", "calculated Pearson correlation value". This list is used to find the k neighbors:
    user_pearson_tuples = []
    pearson_userids_dict = {}  # this dictionary is a helper to sort and eliminate duplicates throughout this method

    if globals.RATINGS_BY_USER is None:
        raise ValueError("[Error] RATINGS_BY_USER is none! Cannot continue with the method!")
    for userUid in globals.RATINGS_BY_USER.keys():
        common_ratings, amount = utils.find_common_ratings(userID, userUid, None)  # common ratings
        pearson_value = calculate_pearson_correlation(common_ratings, userID, userUid)  # calculation of Pearson correlation
        user_pearson_tuples.append((userUid, pearson_value))
        try:
            pearson_userids_dict[pearson_value].append(userUid)
        except KeyError:
            pearson_userids_dict[pearson_value] = []
            pearson_userids_dict[pearson_value].append(userUid)
    mysorted = sorted(user_pearson_tuples, key=operator.itemgetter(1, 0), reverse=True)  # tuples sorted from BIG to SMALL Pearson value
    # Now we should delete duplicate Pearson values always keeping the one corresponding to the user with lowest ID:
    for tuple in mysorted:
        current_pearson_value = tuple[1]
        amount_users_with_same_pearson_value = len(pearson_userids_dict[current_pearson_value])
        if amount_users_with_same_pearson_value > 1:
            neighborsIDs.append(min(pearson_userids_dict[current_pearson_value]))
        else:
            neighborsIDs.append(tuple[0])
        if len(neighborsIDs) == k:
            break;

def compute_cosine_similarity(itemID_i,itemID_j):
    """
    Computes cosine similarity between item i and item j
    :param itemID_i: int number of item i
    :param itemID_j: int number of item j
    :return: float number
    """

def calculate_item_mean_centered_rating(itemID, userID, avgRatingItem):
    """
    Calculates centered mean rating of the item 'itemID' for all users.
    :param itemID: int number of the item
    :param userID: int number of the user
    :param avgRatingItem: mean ratings of item 'itemID'
    :return: float number
    """

def rating_prediction_item(itemID_i, userID):
    """
    Calculates the rating prediction for user 'userID' and item
    :param itemID_i: int number of the item
    :param userID: int number of the user
    :return: float number
    """

def main():
    # Load data and parse it:
    # mymovies = data.load_dat("movies.csv")
    # myratings = data.load_dat("ratings.csv")
    # Dump the parsed data to pickles into the file system:
    # data.dump_pickle(mymovies, data.generate_file_name("movies", "pkl"))
    # data.dump_pickle(myratings, data.generate_file_name("ratings", "pkl"))
    # Load the pickles (much faster than loading and parsing again the raw data):
    movies_pkl = data.load_pickle(MOVIE_PICKLE_LOCATION)
    ratings_pkl = data.load_pickle(RATINGS_PICKLE_LOCATION)
    print "len(movies_pkl): ", len(movies_pkl)
    print "len(ratings_pkl): ", len(ratings_pkl)

    # Setting some global variables and general information:
    globals.RATINGS_BY_USER = utils.extract_ratings_by_users(ratings_pkl)

    # # Question 1:
    # print "Question 1: rating of movie 1125 by user 289."


def test():
    """
    This function is used as a test-bed.
    Just for TESTING purposes. It shouldn't be used for production code.
    :return:
    """
    print "HelloWorldTEST!"

    movies_pkl = data.load_pickle(MOVIE_PICKLE_LOCATION)
    ratings_pkl = data.load_pickle(RATINGS_PICKLE_LOCATION)
    print "len(movies_pkl): ", len(movies_pkl)
    print "len(ratings_pkl): ", len(ratings_pkl)
    globals.RATINGS_BY_USER = utils.extract_ratings_by_users(ratings_pkl)
    # Testing methods:
    # ...
    common_ratings, amount = utils.find_common_ratings(1,4,ratings_pkl)
    print "Amount of common ratings = ", amount
    pearson_value = calculate_pearson_correlation(common_ratings,1,4)
    print "Pearson correlation between 1 and 4 =", pearson_value
    print "+ significance weighting =", pearson_value*calculate_significance_weighing_factor(1,4,ratings_pkl)


if __name__ == '__main__':
    # main()
    test()
