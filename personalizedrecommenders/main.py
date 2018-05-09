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


def calculate_significance_weighing_factor(userAid, userUid, ratings, amount=None):
    """
    Calculates the significance weighing
    :param userAid: int number of user A
    :param userUid: int number of user B
    :param ratings: a list of ALL ratings
    :param amount: number of common ratings (not necessary but if provided, it accelerates the calculations)
    :return: float number
    """
    if amount is None:
        if ratings is None:
            raise ValueError("[Error] 'ratings' is none! Cannot continue with the method!")
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

#TODO: round the result of the prediction????
def rating_prediction_user(userAid, itemID, neighborsIDs, neighbors_data=None):
    """
    Calculates the rating prediction for user A and item 'itemID' based on the nearest neighbors.
    For UUCF, we only consider neighbors with positive similarity value.
    If neighborsIDs is empty, this means no neighbors were found!! Then prediction is calculated in another way.
    :param userAid: int number of user A
    :param itemID: int number of the item
    :param neighborsIDs: list of the nearest neighbors IDs. If empty, this means no neighbors were found!!
    :param neighbors_data: dictionary that hols relevant values of neighbors (such as: Pearson value, common ratings...)
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
    # If 'neighbors_data' was populated with relevant data, we can obtain it from that dictionary.
    numerator = 0.0
    denominator = 0.0
    # If the target item has not been rated by anyone else, then, we return the mean rating of user A:
    if len(neighborsIDs) == 0:
        return mean_ratings_A
    for userUid in neighborsIDs:
        # common_ratings = neighbors_data[userUid]['common_ratings']  # retrieve common ratings TODO: to delete!
        # common_ratings, amount = utils.find_common_ratings(userAid, userUid, None)  # common ratings TODO: to delete!
        # pearson_value = calculate_pearson_correlation(common_ratings, userAid, userUid)  # calculation of Pearson correlation TODO: to delete!
        # ratings_by_user_U = globals.RATINGS_BY_USER[userUid]  # list of ALL ratings by user U TODO: to delete!
        pearson_value = neighbors_data[userUid]['pearson']  # retrieve Pearson value
        ratings_by_user_U = neighbors_data[userUid]['ratings_by_user']  # retrieve all ratings by user U
        mean_ratings_U = calculate_mean_ratings(userUid, ratings_by_user_U)  # mean ratings of user U
        if globals.LOG_STATUS is True:
            print "Pearson value with user {0} = {1}".format(userUid, pearson_value)
        # Find the rating of user U for item 'itemID':
        for rating in ratings_by_user_U:
            if rating['movieid'] == itemID:
                rating_u_i = rating['rating']
        numerator = numerator + ((rating_u_i-mean_ratings_U)*pearson_value)
        denominator = denominator + pearson_value  # updating the denominator with accumulative Pearson correlation values
    return mean_ratings_A + (float(numerator)/float(denominator))


def top_k_most_similar_neighbors(userID, itemID, k=20):
    """
    Retrieves the most similar neighbors of user 'userID' with respect to item 'itemID'.
    Target item must be rated by both users.
    Pearson correlation similarity value must be positive.
    Significance weighting must be taken into account.
    When absolutely no neighbors were found, neighborsIDs list will be empty and 'neighbors_data' will be 'None'
    :param userID: int number of the target user
    :param itemID: int number of the target item
    :param k: int number ideal number of neighbors to find
    :return: list of ints of neighbors IDs AND a dictionary with relevant data of the user
    """
    # A list of ints containing the user IDs of all approved/valid neighbors
    neighborsIDs = []
    # This dictionary holds data (relevant values) for each neighbor to avoid re-calculating them again later on.
    # It contains: "Key=userID" and "Value=a Dictionary with 'Key=name of the property' and 'Value=the value of the property'":
    # e.g. Pearson correlation value, common ratings etc.
    neighbors_data = {}
    # List of tuples with the form: ("userID", "Pearson correlation value"). This list is used to find the k neighbors:
    user_pearson_tuples = []
    # This dictionary is a helper to sort and eliminate duplicates throughout this method:
    pearson_userids_dict = {}

    if globals.RATINGS_BY_USER is None:
        raise ValueError("[Error] RATINGS_BY_USER is none! Cannot continue with the method!")
    for userUid in globals.RATINGS_BY_USER.keys():
        # Skip user if we are comparing the user with her/himself:
        if userUid == userID:
            continue
        # The target item must be rated by current user, otherwise we will not consider current user as a neighbor:
        ratings_by_user_U = globals.RATINGS_BY_USER[userUid]
        itemids_userU = [rating['movieid'] for rating in ratings_by_user_U]
        if itemID not in itemids_userU:
            continue
        common_ratings, amount = utils.find_common_ratings(userID, userUid, None)  # common ratings
        pearson_value = calculate_pearson_correlation(common_ratings, userID, userUid)  # calculation of Pearson correlation
        # We are only interested in positive similarity value. If it's negative, we skip it:
        if pearson_value <= 0:
            continue
        # Relevant data of this user will be added to a dictionary for later use outside this method:
        neighbors_data[userUid] = {}
        neighbors_data[userUid]['pearson'] = pearson_value
        neighbors_data[userUid]['ratings_by_user'] = ratings_by_user_U
        # neighbors_data[userUid]['common_ratings'] = common_ratings # TODO: to delete??? it's not necessary outside the scope of this method!
        # Pearson correlation value needs to be multiplied by significance weighting factor:
        pearson_value = pearson_value * calculate_significance_weighing_factor(userID, userUid, None, amount)
        user_pearson_tuples.append((userUid, pearson_value))
        try:
            pearson_userids_dict[pearson_value].append(userUid)
        except KeyError:
            pearson_userids_dict[pearson_value] = []
            pearson_userids_dict[pearson_value].append(userUid)
    # Watch out! If none of the possible neighbors or users have rated the target item or by any reason no neighbors were found,
    # then, 'neighbors_data' will take the value None indicating that no neighbors were found.
    if len(user_pearson_tuples) == 0:
        neighbors_data = None
    else:
        mysorted = sorted(user_pearson_tuples, key=operator.itemgetter(1, 0), reverse=True)  # tuples sorted from BIG to SMALL Pearson value
        if globals.LOG_STATUS is True:
            print "Len(mysorted) = ", len(mysorted)
        # Now we should delete duplicate Pearson values. In case of draw, keep the one corresponding to the user with lowest ID:
        for tuple in mysorted:
            current_pearson_value = tuple[1]
            amount_users_with_same_pearson_value = len(pearson_userids_dict[current_pearson_value])
            if amount_users_with_same_pearson_value > 1:
                neighborsIDs.append(min(pearson_userids_dict[current_pearson_value]))
            else:
                neighborsIDs.append(tuple[0])
            if len(neighborsIDs) == k:
                break
        if globals.LOG_STATUS is True:
            print "Len(neighbors_data) before = ", len(neighbors_data)
        # Delete all superfluous data from neighbors/users who are not in neighborsIDs:
        for key in neighbors_data.keys():
            if key not in neighborsIDs:
                del neighbors_data[key]
        if globals.LOG_STATUS is True:
            print "Len(neighbors_data) after = ", len(neighbors_data)
    return neighborsIDs, neighbors_data


def topN_recommendations_uucf(userID, ratings, movies, N=10):
    """
    Top N list of recommendations for a certain user given by parameter over all the ratings.
    For this, rating prediction has to be calculated over all items that userID didn't consumed yet.
    :param userID: int number of the user
    :param ratings: a list of ALL ratings
    :param movies: a list of ALL movies
    :param N: number of recommended items
    :return: a list containing tuples corresponding to the TOP-N recommended items with the form ("item id, title, prediction value")
    """
    # This dictionary is a helper to sort and eliminate duplicates throughout this method:
    prediction_itemids_dict = {}

    if globals.RATINGS_BY_USER is None:
        raise ValueError("[Error] RATINGS_BY_USER is none! Cannot continue with the method!")
    ratings_by_user = globals.RATINGS_BY_USER[userID] # list of ALL ratings by the user
    itemids_user = [rating['movieid'] for rating in ratings_by_user]
    # A list for all rating predictions from all those items that the user has not rated yet:
    # The list contains tuples with the form: ("itemid", "rating prediction")
    rating_predictions = []
    for rating in ratings:
        print "------------> movie id = ", rating['movieid'] # TODO: to delete!
        # Skip item if the user has already consumed that item!
        if rating['movieid'] in itemids_user:
            continue
        neighborsIDs, neighbors_data = top_k_most_similar_neighbors(userID, rating['movieid'])
        print "\t| 'top_k_most_similar_neighbors' computed!" # TODO: to delete!
        if globals.LOG_STATUS is True:
            print "neighbors IDs (item:{0}) = {1}".format(rating['movieid'], neighborsIDs)
        prediction = rating_prediction_user(userID, rating['movieid'], neighborsIDs, neighbors_data)
        print "\t| 'rating_prediction_user' computed!" # TODO: to delete!
        rating_predictions.append((rating['movieid'], prediction))
        try:
            prediction_itemids_dict[prediction].append(rating['movieid'])
        except KeyError:
            prediction_itemids_dict[prediction] = []
            prediction_itemids_dict[prediction].append(rating['movieid'])
    mysorted = sorted(rating_predictions, key=operator.itemgetter(1, 0), reverse=True)  # tuples sorted from BIG to SMALL prediction value
    # Now we should delete duplicate Pearson values. In case of draw, keep the one corresponding to the item with lowest ID:
    topN = []
    for tuple in mysorted:
        current_prediction_value = tuple[1]
        amount_items_with_same_prediction_value = len(prediction_itemids_dict[current_prediction_value])
        if amount_items_with_same_prediction_value > 1:
            topN.append((tuple[0], movies[str(tuple[0])]['title'], min(prediction_itemids_dict[current_prediction_value])))
        else:
            topN.append((tuple[0], movies[str(tuple[0])]['title'], tuple[1]))
    return topN


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


def topN_recommendations_iicf(userID, ratings, N=10):
    """
    ??????
    :param userID:
    :param ratings:
    :return:
    """
    pass

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
    print "Pearson X significance weighting =", pearson_value*calculate_significance_weighing_factor(1,4,ratings_pkl, None)
    print "Top-k most similar positive users of user 1 and target item 10:"
    neighborsIDs, neighbors_data = top_k_most_similar_neighbors(1, 10)
    print "\t| neighborsIDs: ", neighborsIDs
    print "\t| neighbors data --> count: ", len(neighbors_data)
    print "Ratings prediction for user 1 and target item 10:"
    rating = rating_prediction_user(1,10,neighborsIDs,neighbors_data)
    print "\t| Rating: ", rating
    print "-----------------------"
    print "Top-k most similar positive users of user 1 and target item 260:"
    neighborsIDs, neighbors_data = top_k_most_similar_neighbors(1, 260)
    print "\t| neighborsIDs: ", neighborsIDs
    print "\t| neighbors data --> count: ", len(neighbors_data)
    print "Ratings prediction for user 1 and target item 260:"
    rating = rating_prediction_user(1, 260, neighborsIDs, neighbors_data)
    print "\t| Rating: ", rating
    print "-----------------------"
    print "TOP-N recommended items for user 1:"
    topn = topN_recommendations_uucf(1, ratings_pkl, movies_pkl)
    for item in topn:
        print "\t|({0},{1},{2})".format(item[0], item[1], item[2])



if __name__ == '__main__':
    # main()
    test()
