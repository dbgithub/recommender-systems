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
IICF_MODEL_NAME = "IICF-model_pickle_12-05-2018--01-18-59.pkl"
RATINGS_X_BY_USERS_PATH = "RATINGS_X_BY_USERS_pickle_10-05-2018--07-00-01.pkl"
MEAN_RATINGS_ITEM_PATH = "MEAN_RATINGS_ITEM_pickle_10-05-2018--07-00-02.pkl"
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
    Calculates the average of the ratings of the user 'userID'
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


def rating_prediction_user(userAid, itemID, neighborsIDs, neighbors_data):
    """
    Calculates the rating prediction for user A and item 'itemID' based on the nearest neighbors.
    For UUCF, we only consider neighbors with positive similarity value.
    If neighborsIDs is empty, this means no neighbors were found!! Then prediction is calculated in another way.
    :param userAid: int number of user A
    :param itemID: int number of the item
    :param neighborsIDs: list of the nearest neighbors IDs. If empty, this means no neighbors were found!!
    :param neighbors_data: dictionary that holds relevant values of neighbors (such as: Pearson value, common ratings...)
    :return: float number
    """
    if globals.RATINGS_BY_USER is None:
        raise ValueError("[Error] RATINGS_BY_USER is none! Cannot continue with the method!")
    if globals.RATINGS_BY_USER_MAP is None:
        raise ValueError("[Error] RATINGS_BY_USER_MAP is none! Cannot continue with the method!")
    ratings_by_user_A = globals.RATINGS_BY_USER[userAid]  # list of ALL ratings by user U
    mean_ratings_A = calculate_mean_ratings(userAid, ratings_by_user_A)  # mean ratings of user U

    # WATCH OUT! To save time and computation resources, there is no need to calculate the Pearson correlation
    # as many times as it appears in the formula.
    # A numerator and denominator have to be calculated: it would be convenient to collect the corresponding
    # Pearson correlations once and use it either in numerator and denominator later on.
    # If 'neighbors_data' was populated with relevant data, we can obtain it from that dictionary.
    numerator = 0.0
    denominator = 0.0
    # If the target item has not been rated by anyone else, then, we return the mean rating of user A:
    if len(neighborsIDs) == 0:
        return mean_ratings_A
    for userUid in neighborsIDs:
        pearson_value = neighbors_data[userUid]['pearson']  # retrieve Pearson value
        ratings_by_user_U = neighbors_data[userUid]['ratings_by_user']  # retrieve all ratings by user U
        mean_ratings_U = calculate_mean_ratings(userUid, ratings_by_user_U)  # mean ratings of user U
        if globals.LOG_STATUS is True:
            print "Pearson value for user {0} = {1}".format(userUid, pearson_value)
        # Fetch the rating of user U for item 'itemID':
        rating_u_i = globals.RATINGS_BY_USER_MAP[userUid][itemID]
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
        itemids_userU = globals.RATINGS_BY_USER_MAP[userUid].keys()
        if itemID not in itemids_userU:
            continue
        common_ratings, amount = utils.find_common_ratings(userID, userUid, None)  # common ratings
        pearson_value = calculate_pearson_correlation(common_ratings, userID, userUid)  # calculation of Pearson correlation
        # We are only interested in positive similarity value. If it's negative, we skip it:
        if pearson_value <= 0.0:
            continue
        # Pearson correlation value needs to be multiplied by significance weighting factor:
        pearson_value = pearson_value * calculate_significance_weighing_factor(userID, userUid, None, amount)
        # Relevant data of this user will be added to a dictionary for later use outside this method:
        neighbors_data[userUid] = {}
        neighbors_data[userUid]['pearson'] = pearson_value
        neighbors_data[userUid]['ratings_by_user'] = ratings_by_user_U
        user_pearson_tuples.append((userUid, pearson_value))
        if pearson_value in pearson_userids_dict:
            pearson_userids_dict[pearson_value].append(userUid)
        else:
            pearson_userids_dict[pearson_value] = []
            pearson_userids_dict[pearson_value].append(userUid)
    # Watch out! If none of the possible neighbors or users have rated the target item or by any reason no neighbors were found,
    # then, 'neighbors_data' will take the value None indicating that no neighbors were found.
    if len(user_pearson_tuples) == 0:
        neighbors_data = None
    else:
        mysorted = sorted(user_pearson_tuples, key=operator.itemgetter(1, 0), reverse=True)  # tuples sorted from BIG to SMALL Pearson value
        if globals.LOG_STATUS is True:
            print "Len(mysorted) # similar users found = ", len(mysorted)
        # Now we should delete duplicate Pearson values. In case of draw, keep the one corresponding to the user with lowest ID:
        tmp = []  # temporal list to keep track of which Pearson values we have already used
        for tuple in mysorted:
            current_pearson_value = tuple[1]
            if current_pearson_value in tmp:
                continue
            amount_users_with_same_pearson_value = len(pearson_userids_dict[current_pearson_value])
            if amount_users_with_same_pearson_value > 1:
                neighborsIDs.append(min(pearson_userids_dict[current_pearson_value]))
            else:
                neighborsIDs.append(tuple[0])
            tmp.append(current_pearson_value)
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


def topN_recommendations_uucf(userID, movies, N=10):
    """
    Top N list of recommendations for a certain user given by parameter over all the ratings.
    For this, rating prediction has to be calculated over all items that userID didn't consumed yet.
    :param userID: int number of the user
    :param movies: a list of ALL movies
    :param N: number of recommended items
    :return: a list containing tuples corresponding to the TOP-N recommended items with the form ("item id, title, prediction value")
    """
    # This dictionary is a helper to sort and eliminate duplicates throughout this method:
    prediction_itemids_dict = {}

    if globals.RATINGS_BY_USER is None:
        raise ValueError("[Error] RATINGS_BY_USER is none! Cannot continue with the method!")
    if globals.RATINGS_BY_USER_MAP is None:
        raise ValueError("[Error] RATINGS_BY_USER_MAP is none! Cannot continue with the method!")
    itemids_user = globals.RATINGS_BY_USER_MAP[userID].keys()  # item IDs of those items rated by user
    # A list for all rating predictions from all those items that the user has not rated yet:
    # The list contains tuples with the form: ("itemid", "rating prediction")
    rating_predictions = []
    allItems = [int(movie['id']) for movie in movies.values()]  # we retrieve all item IDs
    for movieid in allItems:
        # Skip item if the user has already consumed that item!
        if movieid in itemids_user:
            continue
        neighborsIDs, neighbors_data = top_k_most_similar_neighbors(userID, movieid)
        if globals.LOG_STATUS is True:
            print "neighbors IDs (item:{0}) = {1}".format(movieid, neighborsIDs)
        prediction = rating_prediction_user(userID, movieid, neighborsIDs, neighbors_data)
        rating_predictions.append((movieid, prediction))
        if prediction in prediction_itemids_dict:
            prediction_itemids_dict[prediction].append(movieid)
        else:
            prediction_itemids_dict[prediction] = []
            prediction_itemids_dict[prediction].append(movieid)
    mysorted = sorted(rating_predictions, key=operator.itemgetter(1, 0), reverse=True)  # tuples sorted from BIG to SMALL prediction value
    # Now we should delete duplicate Pearson values. In case of draw, keep the one corresponding to the item with lowest ID:
    tmp = []  # temporal list to keep track of which Pearson values we have already used
    topN = []
    for tuple in mysorted:
        current_prediction_value = tuple[1]
        if current_prediction_value in tmp:
            continue
        amount_items_with_same_prediction_value = len(prediction_itemids_dict[current_prediction_value])
        if amount_items_with_same_prediction_value > 1:
            lowest_id = min(prediction_itemids_dict[current_prediction_value])
            topN.append((lowest_id, movies[str(lowest_id)]['title'], tuple[1]))
        else:
            topN.append((tuple[0], movies[str(tuple[0])]['title'], tuple[1]))
        tmp.append(current_prediction_value)
        if len(topN) == N:
            break
    return topN


def build_model_iicf(movies, ratings):
    """
    Builds the IICF model using cosine similarity
    :param movies: list of ALL movies
    :param ratings: list of ALL ratings
    :return: nothing
    """
    # Firstly, we capture all item IDs (movie IDs) to iterate through them:
    # We cannot assume that the IDs go from 1 to 9125. That's the reason why we better retrieve them from the movie list.
    itemIDs = [int(movie['id']) for movie in movies.values()]
    itemIDs = sorted(itemIDs)  # ordered from BIG to SMALL
    globals.IICF_MODEL = {}  # reset the model just in case
    globals.IICF_MODEL[-1] = {}  # declare negative branch as a dictionary in the model
    globals.IICF_MODEL[1] = {}  # declare positive branch as a dictionary in the model
    flag_calculate = False  # a boolean flag to indicate whether cosine similarity has to be calculated or not.
    for item_i in itemIDs:
        for item_j in itemIDs:
            # Skip similarity with itself!
            if item_i == item_j:
                continue
            # print "({0},{1})".format(item_i, item_j)
            # Cosine similarity calculation may take big amount of time if sim(i,j)=sim(j,i) is not taken into account.
            # Therefore, we will check if the value for its counterpart is already computed or not.
            # Given the data structure designed for the IICF MODEL, first we need to check if the possible computed value resides in the negative or positive branch of the model.
            # Based on that, we will set a flag to True or False to indicate that we need to calculate the Cosine similarity or not.
            if item_i not in globals.IICF_MODEL[1]:
                if item_i not in globals.IICF_MODEL[-1]:
                    flag_calculate = True
                elif item_j not in globals.IICF_MODEL[-1][item_i]:
                    try:
                        if item_j in globals.IICF_MODEL[1][item_i]:
                            flag_calculate = False
                        else:
                            flag_calculate = True
                    except KeyError:
                        flag_calculate = True
            elif item_j not in globals.IICF_MODEL[1][item_i]:
                try:
                    if item_j in globals.IICF_MODEL[-1][item_i]:
                        flag_calculate = False
                    else:
                        flag_calculate = True
                except KeyError:
                    flag_calculate = True
            # Now we check if flag was set to True or False:
            if flag_calculate is False:
                continue  # this means no need to calculate cosine similarity for this pair of indexes
            flag_calculate = False  # reset flag
            cos_similarity = compute_cosine_similarity(item_i, item_j)  # compute cosine similarity
            print "{0} --> ({1}, {2})".format(cos_similarity, item_i, item_j)
            # After calculating cosine similarity, the value has to be stored in (i,j) location and (j,i) too.
            # For this, we need to check if the computed similarity is positive or negative:
            if cos_similarity is not None and cos_similarity > 0.0:  # POSITIVE similarities
                if item_i not in globals.IICF_MODEL[1]:
                    globals.IICF_MODEL[1][item_i] = {}
                globals.IICF_MODEL[1][item_i][item_j] = cos_similarity
                # sim(i,j) has been stored, so we know that sim(j,i) takes the same value:
                if item_j not in globals.IICF_MODEL[1]:
                    globals.IICF_MODEL[1][item_j] = {}
                globals.IICF_MODEL[1][item_j][item_i] = cos_similarity
            elif cos_similarity is not None and cos_similarity < 0.0:  # NEGATIVE similarities
                if item_i not in globals.IICF_MODEL[-1]:
                    globals.IICF_MODEL[-1][item_i] = {}
                globals.IICF_MODEL[-1][item_i][item_j] = cos_similarity
                # sim(i,j) has been stored, so we know that sim(j,i) takes the same value:
                if item_j not in globals.IICF_MODEL[-1]:
                    globals.IICF_MODEL[-1][item_j] = {}
                globals.IICF_MODEL[-1][item_j][item_i] = cos_similarity
    print "IICF model build!"


def compute_cosine_similarity(itemID_i,itemID_j):
    """
    Computes cosine similarity between item i and item j.
    Watch out! To speed-up the execution time several data objects are already provided by means of global variables.
    If any of those global variables is missin (None) this method cannot proceed.
    :param itemID_i: int number of item i
    :param itemID_j: int number of item j
    :return: float number
    """
    if globals.RATINGS_BY_USER is None:
        raise ValueError("[Error] RATINGS_BY_USER is none! Cannot continue with the method!")
    if globals.RATINGS_BY_USER_MAP is None:
        raise ValueError("[Error] RATINGS_BY_USER_MAP is none! Cannot continue with the method!")
    if globals.RATINGS_X_BY_USERS is None:
        raise ValueError("[Error] RATINGS_X_BY_USERS is none! Cannot continue with the method!")
    if globals.MEAN_RATINGS_ITEM is None:
        raise ValueError("[Error] MEAN_RATINGS_ITEM is none! Cannot continue with the method!")
    ratings_i_by_users = globals.RATINGS_X_BY_USERS[itemID_i]
    ratings_j_by_users = globals.RATINGS_X_BY_USERS[itemID_j]
    mean_ratings_i = globals.MEAN_RATINGS_ITEM[itemID_i]
    mean_ratings_j = globals.MEAN_RATINGS_ITEM[itemID_j]
    d_i = calculate_item_mean_centered_rating(ratings_i_by_users, mean_ratings_i)  # this is the calculation of one part of the formula
    d_j = calculate_item_mean_centered_rating(ratings_j_by_users, mean_ratings_j)  # this is the calculation of one part of the formula
    # Calculation of denominator:
    denominator = float(np.sqrt(d_i) * np.sqrt(d_j))
    if denominator == 0.0:
        return 0.0
    # Calculation of numerator:
    numerator = 0.0
    for userIDs in globals.RATINGS_BY_USER.keys():
        try:
            rating_i = globals.RATINGS_BY_USER_MAP[userIDs][itemID_i]  # rating of the user for item i
            rating_j = globals.RATINGS_BY_USER_MAP[userIDs][itemID_j]  # rating of the user for item j
        except KeyError:
            continue
        numerator += float(rating_i - mean_ratings_i) * float(rating_j - mean_ratings_j)
    return numerator/denominator


def calculate_mean_ratings_for_item(itemID, ratings_by_users=None, ratings=None):
    """
    Calculates the average of the ratings of all users who rated this item
    :param itemID: int number of the id of the item
    :param ratings_by_users: list of ratings by all users. Provided by parameter to speed-up execution in run-time.
    :param ratings: list of ALL ratings
    :return: float number, average of the ratings
    """
    # To avoid excessive computation during run-time, the item ratings are provided by parameter.
    # If it's not none, then it can be used, otherwise we need to calculate it.
    if ratings_by_users is not None:
        return np.mean([rating['rating'] for rating in ratings_by_users])
    else:
        if ratings is not None:
            tmp = [rating for rating in ratings if rating['movieid']==itemID]
            return np.mean([rating['rating'] for rating in tmp])
        else:
            raise ValueError("[Error] 'ratings' is none! Cannot continue with the method!")


def calculate_item_mean_centered_rating(ratings_by_users, avgRatingItem):
    """
    Calculates centered mean rating of an item among all users who rated that item
    :param ratings_by_users: list of ratings for an item. Ratings over which we want to calculate user mean centered rating.
    :param avgRatingItem: mean ratings of item
    :return: float number
    """
    sum = 0.0
    for rating in ratings_by_users:
        sum = sum + pow(rating['rating'] - avgRatingItem, 2)
    return sum


def rating_prediction_item(itemID_i, userID, neighborsIDs=None):
    """
    Calculates the rating prediction for target user 'userID' and target item 'itemID_i'
    :param itemID_i: int number of the item
    :param userID: int number of the user
    :param neighborsIDs: a list of tuples with the form: ("itemJid", "similarity value") with the top k most similar items
    :return: float number
    """
    if globals.RATINGS_BY_USER_MAP is None:
        raise ValueError("[Error] RATINGS_BY_USER_MAP is none! Cannot continue with the method!")
    numerator = 0.0
    denominator = 0.0
    # We find the top-k most similar neighbors (items) that are also rated by user:
    # we get a list of tuples with the form: ("itemJid", "similarity value")
    if neighborsIDs is not None:
        itemid_similarities_tuples = neighborsIDs
    else:
        itemid_similarities_tuples = top_k_most_similar_items(userID, itemID_i)
    # print itemid_similarities_tuples
    # If the neighborhood size is 0, the rating prediction takes 0 as well:
    if len(itemid_similarities_tuples) == 0:
        return 0.0
    # Calculating the rating prediction:
    for tuple in itemid_similarities_tuples:
        numerator = numerator + tuple[1]*globals.RATINGS_BY_USER_MAP[userID][tuple[0]]
        denominator = denominator + abs(tuple[1])
    return float(numerator)/float(denominator)


def top_k_most_similar_items(userID, itemID, k=20):
    """
    Retrieves the most similar items that are rated by user 'userID' based on the pre-computed similarities.
    :param userID: int number of the user
    :param userID: int number of the item
    :param k: int number ideal number of neighbors to find
    :return: list of tuples with the form: ("itemJid", "similarity value")
    """
    if globals.RATINGS_BY_USER_MAP is None:
        raise ValueError("[Error] RATINGS_BY_USER_MAP is none! Cannot continue with the method!")
    if globals.IICF_MODEL is None:
        raise ValueError("[Error] IICF_MODEL is none! Cannot continue with the method!")
    if globals.SIMILARITY_TYPE is None:
        raise ValueError("[Error] SIMILARITY_TYPE is none! Cannot continue with the method!")
    # List of tuples with the form: ("itemJid", "similarity value"):
    item_similarity_tuples = []
    # Firstly, we retrieve the item IDs of the items that the user rated. Top-k most similar items ensures that similar
    # items are actually rated by the user:
    itemIDs_rated_by_user = globals.RATINGS_BY_USER_MAP[userID].keys()
    # The model only contains positive similarity values, let's check if current itemID is in the model:
    if itemID not in globals.IICF_MODEL[1] and itemID not in globals.IICF_MODEL[-1]:
        return item_similarity_tuples
    # Secondly, we iterate over all positive AND/OR negative similar items of 'itemID' making sure the item was rated by current user:
    # The goal is to find the 'k' most similar items:
    if globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.positive() or globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.both():
        for itemid in globals.IICF_MODEL[1][itemID].keys():
            if itemid in itemIDs_rated_by_user:
                item_similarity_tuples.append((itemid, globals.IICF_MODEL[1][itemID][itemid]))
    if globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.negative() or globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.both():
        for itemid in globals.IICF_MODEL[-1][itemID].keys():
            if itemid in itemIDs_rated_by_user:
                item_similarity_tuples.append((itemid, globals.IICF_MODEL[-1][itemID][itemid]))
    if len(item_similarity_tuples) == 0:
        return item_similarity_tuples
    mysorted = sorted(item_similarity_tuples, key=operator.itemgetter(1, 0), reverse=True)  # tuples sorted from BIG to SMALL similarity value
    if globals.LOG_STATUS is True:
        print "Len(mysorted) (# similar items found) = ", len(mysorted)
    return mysorted[0:k]


def topN_recommendations_iicf(userID, movies, N=10):
    """
    Top N list of recommendations for a certain target user and target item.
    Items cannot be the ones already rated by the target user.
    :param userID: int number of the user
    :param movies: a list of ALL movies
    :return: a list containing tuples corresponding to the TOP-N recommended items with the form ("item id, title, prediction value")
    """
    if globals.RATINGS_BY_USER_MAP is None:
        raise ValueError("[Error] RATINGS_BY_USER_MAP is none! Cannot continue with the method!")
    # List of tuples with the form: ("itemJid", "similarity value"):
    item_prediction_tuples = []
    # Firstly, we retrieve the item IDs of the items that the user rated. Top-N recommendations cannot recommend items
    # that have already been consumed.
    itemIDs_rated_by_user = globals.RATINGS_BY_USER_MAP[userID].keys()
    allItems = [int(movie['id']) for movie in movies.values()]
    for movieid in allItems:
        # Skip item if already rated by user:
        if movieid in itemIDs_rated_by_user:
            continue
        # print "movie id = ", movieid
        most_similar_items_tuples = top_k_most_similar_items(userID, movieid)  # search for top k most similar items with current movie ID
        if len(most_similar_items_tuples) != 0:
            prediction = rating_prediction_item(movieid, userID, most_similar_items_tuples)  # perform the prediction
            # print "\t| prediction = ", prediction
            item_prediction_tuples.append((movieid, prediction))  # append the prediction to the final list (before sorting)
    mysorted = sorted(item_prediction_tuples, key=operator.itemgetter(1, 0), reverse=True)  # tuples sorted from BIG to SMALL prediction value
    topN = []  # final TOP N list
    for tuple in mysorted[0:N]:
        topN.append((tuple[0],movies[str(tuple[0])]['title'],tuple[1]))
    return topN


def topN_recommendations_basket(basket, movies, N=10):
    """
    Top N list of recommendations based on the item(s) in the basket.
    If shopping basket contains only 1 item, the recommendations are the most similar items.
    If multiple items in the basket, score for target item is calculated as the sum of similarities between
    target item and all items in the basket.
    :param basket: list of ints of item IDs in the basket
    :param movies: list of ALL movies
    :param N: int number of items to recommend
    :return: a list containing tuples corresponding to the TOP-N recommended items with the form ("item id, title, prediction value")
    """
    if globals.SIMILARITY_TYPE is None:
        raise ValueError("[Error] SIMILARITY_TYPE is none! Cannot continue with the method!")
    if globals.IICF_MODEL is None:
        raise ValueError("[Error] IICF_MODEL is none! Cannot continue with the method!")
    score_target_items = []  # a list of tuples with the form ('itemID', 'score')
    if len(basket) == 1:
        if globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.positive() or globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.both():  # POSITIVE similarities (or BOTH)
            for movieid in globals.IICF_MODEL[1][basket[0]].keys():
                # Skip cosine similarity with itself:
                if movieid == basket[0]:
                    continue
                score_target_items.append((movieid, globals.IICF_MODEL[1][basket[0]][movieid]))
        if globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.negative() or globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.both():  # NEGATIVE similarities (or BOTH)
            for movieid in globals.IICF_MODEL[-1][basket[0]].keys():
                # Skip cosine similarity with itself:
                if movieid == basket[0]:
                    continue
                score_target_items.append((movieid, globals.IICF_MODEL[-1][basket[0]][movieid]))
    elif len(basket) > 1:
        allItems = [int(movie['id']) for movie in movies.values()]
        for movieid in allItems:
            score = 0.0
            for j in basket:
                if globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.positive() or globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.both():  # POSITIVE similarities (or BOTH)
                    if movieid != j and movieid in globals.IICF_MODEL[1]:  # Skip cosine similarity with itself
                        if j in globals.IICF_MODEL[1][movieid]:
                            score = score + globals.IICF_MODEL[1][movieid][j]
                if globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.negative() or globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.both():  # NEGATIVE similarities (or BOTH)
                    if movieid != j and movieid in globals.IICF_MODEL[-1]:  # Skip cosine similarity with itself
                        if j in globals.IICF_MODEL[-1][movieid]:
                            score = score + globals.IICF_MODEL[-1][movieid][j]
            score_target_items.append((movieid, score))
    mysorted = sorted(score_target_items, key=operator.itemgetter(1, 0), reverse=True)  # tuples sorted from BIG to SMALL score value
    topN = []  # final TOP N list
    for tuple in mysorted[0:N]:
        topN.append((tuple[0], movies[str(tuple[0])]['title'], tuple[1]))
    return topN


def topN_recommendations_hybrid(userID, movies, weight_uucf=0.5, weight_iicf=0.5, N=10):
    """
    Combines two recommenders: UUCF and IICF. Both with equal weights by default: 50%
    :param userID: int number of the user to whom the recommendations are calculated
    :param weight_uucf: float number of the weight for this recommender
    :param weight_iicf: float number of the weight for this recommender
    :param N: int number of items to recommend
    :return: a list containing tuples corresponding to the TOP-N recommended items with the form ("item id, title, prediction value")
    """
    topn_uucf = topN_recommendations_uucf(userID, movies, N) # returns top-N recommended items with the form ("item id, title, prediction value")
    topn_iicf = topN_recommendations_iicf(userID, movies, N) # returns top-N recommended items with the form ("item id, title, prediction value")
    # List of tuples with the form: ("item id, title, prediction value for iicf, prediction value for uucf"):
    merge = [(tuple1[0], tuple1[1], tuple1[2], tuple2[2]) for tuple1 in topn_iicf for tuple2 in topn_uucf if tuple1[0]==tuple2[0]]
    topn_hybrid = []
    for tuple in merge:
        prediction_hybrid = tuple[2]*weight_iicf + tuple[3]*weight_uucf
        topn_hybrid.append((tuple1[0], tuple1[1], prediction_hybrid))
    return topn_hybrid

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
    globals.RATINGS_BY_USER_MAP = utils.extract_ratings_by_users_map(ratings_pkl)
    # globals.RATINGS_X_BY_USERS = utils.extract_ratings_x_by_users(movies_pkl, ratings_pkl)  # TODO: uncomment
    # globals.MEAN_RATINGS_ITEM = utils.extract_mean_ratings(movies_pkl)  # TODO: uncomment
    globals.RATINGS_X_BY_USERS = data.load_pickle(RATINGS_X_BY_USERS_PATH)  # load pickle  # TODO: to delete
    globals.MEAN_RATINGS_ITEM = data.load_pickle(MEAN_RATINGS_ITEM_PATH)  # load pickle  # TODO: to delete
    globals.SIMILARITY_TYPE = globals.SimilarityType()
    print "len(RATINGS_BY_USER): ", len(globals.RATINGS_BY_USER)
    print "len(RATINGS_BY_USER_MAP): ", len(globals.RATINGS_BY_USER_MAP)
    print "len(RATINGS_X_BY_USERS): ", len(globals.RATINGS_X_BY_USERS)
    print "len(MEAN_RATINGS_ITEM): ", len(globals.MEAN_RATINGS_ITEM)
    print "SIMILARITY_TYPE.type(): ", globals.SIMILARITY_TYPE.type()

    # Question 1:
    print "Question 1: Pearson correlation (without significance weighting) user 1 and 4."
    common_ratings, amount = utils.find_common_ratings(1, 4, None)
    p = calculate_pearson_correlation(common_ratings, 1, 4)
    print "\t| Result =", p
    # Question 2:
    print "Question 2: Pearson correlation (with significance weighting) user 1 and 4."
    common_ratings, amount = utils.find_common_ratings(1, 4, None)
    p = calculate_pearson_correlation(common_ratings, 1, 4)
    result = p * calculate_significance_weighing_factor(1,4,ratings_pkl,amount)
    print "\t| Result =", result
    # Question 5:
    print "Question 5: Amount of neighbors (strict positive similarity) user 1 and item 10."
    neighborsIDs, neighbors_data = top_k_most_similar_neighbors(1,10,1000)
    print "\t| # of neighbors = ", len(neighborsIDs)
    # Question 6:
    print "Question 6: List those neighbors."
    neighborsIDs, neighbors_data = top_k_most_similar_neighbors(1, 10)
    for item in neighborsIDs:
        print "\t| ID: ", item, " | Pearson: ", neighbors_data[item]['pearson']
    # Question 7:
    print "Question 7: Weighted average of the deviation from mean rating. Neighbors of user 1 item 10."
    pre = rating_prediction_user(1,10,neighborsIDs,neighbors_data)
    print "\t| Result = ", pre
    # Question 8:
    print "Question 8: Rating prediction user 1 item 10."
    pre = rating_prediction_user(1,10,neighborsIDs,neighbors_data)
    print "\t| Result = ", pre
    # Question 9:
    print "Question 9: Title item 10."
    print "\t Title = ", movies_pkl['10']['title']
    # Question 10:
    print "Question 10: Amount of neighbors (strict positive similarity) user 1 and item 260."
    neighborsIDs, neighbors_data = top_k_most_similar_neighbors(1,260,1000)
    print "\t| # of neighbors = ", len(neighborsIDs)
    # Question 11:
    print "Question 11: List those neighbors."
    neighborsIDs, neighbors_data = top_k_most_similar_neighbors(1, 260)
    for item in neighborsIDs:
        print "\t| ID: ", item, " | Pearson: ", neighbors_data[item]['pearson']
    # Question 12:
    print "Question 12: Weighted average of the deviation from mean rating. Neighbors of user 1 item 260."
    pre = rating_prediction_user(1, 260, neighborsIDs, neighbors_data)
    print "\t| Result = ", pre
    # Question 13:
    print "Question 13: Rating prediction user 1 item 260."
    pre = rating_prediction_user(1, 260, neighborsIDs, neighbors_data)
    print "\t| Result = ", pre
    # Question 14:
    print "Question 14: Title item 260."
    print "\t Title = ", movies_pkl['260']['title']
    # Question 16:
    print "Question 16: Top-N recommendations user 1."
    # topn = topN_recommendations_uucf(1,movies_pkl)
    # for item in topn:
    #     print "\t| ({0},{1},{2})".format(item[0], item[1], item[2])
    # Question 17:
    print "Question 17: Top-N recommendations user 522."
    # topn = topN_recommendations_uucf(522,movies_pkl)
    # for item in topn:
    #     print "\t| ({0},{1},{2})".format(item[0], item[1], item[2])
    # Question 19:
    print "Question 19: IICF model. Strict positive similarities."
    globals.IICF_MODEL = data.load_pickle(IICF_MODEL_NAME)  # load the IICF model
    print "\t| Result = ", len(globals.IICF_MODEL[1])
    # Question 20:
    print "Question 20: Cosine similarity between items 594 and 596."
    sim = globals.IICF_MODEL[1][594][596]
    print "\t| Similarity = ", sim
    print "\t| Movie 594 =", movies_pkl['594']['title']
    print "\t| Movie 596 =", movies_pkl['596']['title']
    # Question 21:
    print "Question 21: Rating prediction for user 522 and item 25. Similar neighbors rated by user:"
    globals.SIMILARITY_TYPE.setPositive()
    result = top_k_most_similar_items(522,25,1000)
    print "\t| Result = ", len(result)
    # Question 22:
    print "Question 22: Top-k similar items for user 522 and item 25."
    globals.SIMILARITY_TYPE.setPositive()
    topk = top_k_most_similar_items(522, 25)
    for item in topk:
        print "\t| ({0} , {1} , {2})".format(item[0], movies_pkl[str(item[0])]['title'], item[1])
    # Question 24:
    print "Question 24: Top-N recommendations for user 522."
    globals.SIMILARITY_TYPE.setPositive()
    topn = topN_recommendations_iicf(522, movies_pkl)
    for item in topn:
        print "\t| ( {0} , {1}, {2} )".format(item[0], item[1], item[2])
    # Question 25:
    print "Question 25: Top-N recommendations basket items: [1]."
    globals.SIMILARITY_TYPE.setPositive()
    topn = topN_recommendations_basket([1], movies_pkl)
    for item in topn:
        print "\t| ( {0} , {1}, {2} )".format(item[0], item[1], item[2])
    # Question 26:
    print "Question 26: Top-N recommendations basket items: [1, 48, 239]."
    globals.SIMILARITY_TYPE.setPositive()
    topn = topN_recommendations_basket([1, 48, 239], movies_pkl)
    for item in topn:
        print "\t| ( {0} , {1}, {2} )".format(item[0], item[1], item[2])
    # Question 27:
    print "Question 27: Top-N recommendations basket items: [1, 48, 239] plus negative similarities."
    globals.SIMILARITY_TYPE.setBoth()
    topn = topN_recommendations_basket([1, 48, 239], movies_pkl)
    for item in topn:
        print "\t| ( {0} , {1}, {2} )".format(item[0], item[1], item[2])
    # Question 29:
    print "Question 29: Top-N recommendations hybrid for user 522."
    globals.SIMILARITY_TYPE.setPositive()
    topn = topN_recommendations_hybrid(522,movies_pkl)
    for item in topn:
        print "\t| ( {0} , {1}, {2} )".format(item[0], item[1], item[2])



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
    globals.RATINGS_BY_USER_MAP = utils.extract_ratings_by_users_map(ratings_pkl)
    # globals.RATINGS_X_BY_USERS = utils.extract_ratings_x_by_users(movies_pkl, ratings_pkl)
    # globals.MEAN_RATINGS_ITEM = utils.extract_mean_ratings(movies_pkl)
    globals.RATINGS_X_BY_USERS = data.load_pickle(RATINGS_X_BY_USERS_PATH)  # load pickle
    globals.MEAN_RATINGS_ITEM = data.load_pickle(MEAN_RATINGS_ITEM_PATH)  # load pickle
    globals.SIMILARITY_TYPE = globals.SimilarityType()
    print "len(RATINGS_BY_USER): ", len(globals.RATINGS_BY_USER)
    print "len(RATINGS_BY_USER_MAP): ", len(globals.RATINGS_BY_USER_MAP)
    print "len(RATINGS_X_BY_USERS): ", len(globals.RATINGS_X_BY_USERS)
    print "len(MEAN_RATINGS_ITEM): ", len(globals.MEAN_RATINGS_ITEM)
    print "SIMILARITY_TYPE.type(): ", globals.SIMILARITY_TYPE.type()
    # Dump some globals:
    # data.dump_pickle(globals.RATINGS_X_BY_USERS, data.generate_file_name("RATINGS_X_BY_USERS", "pkl"))
    # data.dump_pickle(globals.MEAN_RATINGS_ITEM, data.generate_file_name("MEAN_RATINGS_ITEM", "pkl"))

    # Testing methods:
    # ...

    # build_model_iicf(movies_pkl, ratings_pkl)
    # Dump the IICF model to pickle into file system:
    # data.dump_pickle(globals.IICF_MODEL, data.generate_file_name("IICF-model", "pkl"))
    # Load the pickle of the IICF model:
    # globals.IICF_MODEL = data.load_pickle(IICF_MODEL_NAME)
    # print "len(IICF_MODEL) =", len(globals.IICF_MODEL)
    # print "len(IICF_MODEL) positives =", len(globals.IICF_MODEL[1])
    # print "len(IICF_MODEL) negatives =", len(globals.IICF_MODEL[-1])
    # print "value = ", globals.IICF_MODEL[-1][10][148626]
    # print "globals.IICF_MODEL[1][594][596] similarity =", globals.IICF_MODEL[1][594][596]
    # print "-----------------------"
    # pre = rating_prediction_item(25,522)
    # print "Rating prediction for item 25 and user 522: ", pre
    # print "-----------------------"
    # print "Top N recommendations for user with id=522:"
    # result = topN_recommendations_iicf(522,movies_pkl)
    # for item in result:
    #     print "\t|({0},{1},{2})".format(item[0], item[1], item[2])
    # print "-----------------------"
    # common_ratings, amount = utils.find_common_ratings(1,4,ratings_pkl)
    # print "Amount of common ratings = ", amount
    # pearson_value = calculate_pearson_correlation(common_ratings,1,4)
    # print "Pearson correlation between 1 and 4 =", pearson_value
    # print "Pearson X significance weighting =", pearson_value*calculate_significance_weighing_factor(1,4,ratings_pkl, None)
    # print "Top-k most similar positive users of user 1 and target item 10:"
    # neighborsIDs, neighbors_data = top_k_most_similar_neighbors(1, 10)
    # print "\t| neighborsIDs: ", neighborsIDs
    # print "\t| neighbors data --> count: ", len(neighbors_data)
    # print "Ratings prediction for user 1 and target item 10:"
    # rating = rating_prediction_user(1,10,neighborsIDs,neighbors_data)
    # print "\t| Rating: ", rating
    # print "-----------------------"
    # print "Top-k most similar positive users of user 1 and target item 260:"
    # neighborsIDs, neighbors_data = top_k_most_similar_neighbors(1, 260)
    # print "\t| neighborsIDs: ", neighborsIDs
    # print "\t| neighbors data --> count: ", len(neighbors_data)
    # print "Ratings prediction for user 1 and target item 260:"
    # rating = rating_prediction_user(1, 260, neighborsIDs, neighbors_data)
    # print "\t| Rating: ", rating
    # print "-----------------------"
    # print "TOP-N recommended items for user 522:"
    # topn = topN_recommendations_uucf(522, movies_pkl)
    # for item in topn:
    #     print "\t|({0},{1},{2})".format(item[0], item[1], item[2])
    # print "-----------------------"
    # print "BASKET top-N recommendations ---> basket:[1]"
    # basket = [1]
    # topn = topN_recommendations_basket(basket, movies_pkl)
    # for item in topn:
    #     print "\t|({0},{1},{2})".format(item[0], item[1], item[2])
    # print "-----------------------"
    # print "BASKET top-N recommendations ---> basket:[1,48,239]"
    # basket = [1, 48, 239]
    # topn = topN_recommendations_basket(basket, movies_pkl)
    # for item in topn:
    #     print "\t|({0},{1},{2})".format(item[0], item[1], item[2])
    # print "-----------------------"
    # print "Hybrid recommender for user 522:"
    # topN_recommendations_hybrid(522, movies_pkl)
    # print "-----------------------"
    # print "Playing with SimilarityType:"
    # print "Current similarity type = ", globals.SIMILARITY_TYPE.type()
    # print "Set similarity type to 'Positive': "
    # globals.SIMILARITY_TYPE.setPositive()
    # print "\t Type: ", globals.SIMILARITY_TYPE.type()
    # print "Set similarity type to 'Negative': "
    # globals.SIMILARITY_TYPE.setNegative()
    # print "\t Type: ", globals.SIMILARITY_TYPE.type()
    # print "Set similarity type to 'Both': "
    # globals.SIMILARITY_TYPE.setBoth()
    # print "\t Type: ", globals.SIMILARITY_TYPE.type()
    # print "SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.positive():"
    # print globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.positive()
    # print "SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.negative():"
    # print globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.negative()
    # print "SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.both():"
    # print globals.SIMILARITY_TYPE.type() == globals.SIMILARITY_TYPE.both()
    # print "-----------------------"

if __name__ == '__main__':
    main()
    # test()
