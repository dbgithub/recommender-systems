"""
This file is the main file. Main methods for personalized recommender system can be found here.

"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

from numpy import mean
import data
import utils

MOVIE_PICKLE_LOCATION = "movies_pickle_06-05-2018--23-43-45.pkl"
RATINGS_PICKLE_LOCATION = "ratings_pickle_06-05-2018--23-43-45.pkl"
LOG_STATUS = True
RATINGS = None

def calculate_pearson_correlation(common_ratings, userAid, userUid):
    """
    Calculates Pearson correlation.
    :param common_ratings: a dictionary with "Key=userID" and "Value=list of rating objects"
    :param userAid: int number of the id of user A
    :param userUid: int number of the id of user B
    :return: float number, weight of Pearson correlation
    """
    mean_ratings_A = calculate_mean_ratings(userAid)
    mean_ratings_U = calculate_mean_ratings(userUid)
    # numerator =
    # denominator =
    # sum((m - r + 1) * (n - r + 1) for r in zip(common_ratings[userAid],common_ratings[userUid]))
    # return float(numerator)/float(denominator)

def calculate_mean_ratings(userID):
    """
    Calculates the average of the ratings of the user given by parameter
    :param userID: int number of the id of the user
    :return: float number, average of the ratings
    """
    return mean(utils.extract_ratings_by_user(userID))

def calculate_user_mean_centered_rating(ratings_user, avgRatingUser):
    """
    Calculates the centered mean rating of a certain user over a subset of his ratings
    :param ratings_user: some ratings of the user. Ratings over which we want to calculate user mean centered rating.
    :param avgRatingUser: mean ratings of the user
    :return: float number
    """
    return (sum(pow(rating-avgRatingUser, 2)) for rating in ratings_user)

def calculate_significance_weighing(userAid, userUid):
    """
    Calculates the significance weighing
    :param userAid: int number of user A
    :param userUid: int number of user B
    :return: float number
    """

def intersection_ratings_users(ratingsA, ratingsU):
    """
    Intersects both ratings sets to find the common ratings by both users
    :param ratingsA: list of ratings of user A
    :param ratingsU: list of ratings of user B
    :return: list of ratings
    """

def rating_prediction_user(userAid,itemID, neighborsIDs):
    """
    Calculates the rating prediction for user A and for item 'itemID'
    based on the nearest neighbors.
    :param userAid: int number of user A
    :param itemID: int number of the item
    :param neighborsIDs: list of the nearest neighbors IDs
    :return: float number
    """

def top_k_most_similar_neighbors(userID, itemID):
    """
    Retrieves the most similar neighbor of user 'userID' with respect to item 'itemID'
    :param userID: int number of the user
    :param itemID: int number of the item
    :return: list of neighbors IDs
    """

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

    # # Question 1:
    # print "Question 1: rating of movie 1125 by user 289."


def test():
    """
    This function is used as a test-bed.
    Just for TESTING purposes. It shouldn't be used for production code.
    :return:
    """
    print "HelloWorldTEST!"

    # Data:
    movies_pkl = data.load_pickle(MOVIE_PICKLE_LOCATION)
    ratings_pkl = data.load_pickle(RATINGS_PICKLE_LOCATION)
    # Testing methods:
    # ...


if __name__ == '__main__':
    main()
    # test()