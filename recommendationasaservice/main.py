"""
This file is the main file. The interaction with the recommender service starts here.

"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

import sugestio
import data
import utils

ACCOUNT = 'sandbox'
SECRET = 'demo'
# ACCOUNT = 's2018debla'
# SECRET = 'Dzkux4G9k1AZzVCA'
MOVIE_PICKLE_LOCATION = ""
RATINGS_PICKLE_LOCATION = ""

def submit_metadata_single_movie(movieID, metadata):
    """
    Submits information about the movie with ID passed by parameter.
    Different data fields can be specified. Request method is POST.
    :param movieID: int number of the movie identifier
    :param metadata: the metadata object about the movie to be included
    :return:
    """

def submit_rating_single_movie(movieID, rating):
    """
    Submits a rating (consumption) for a certain movie.
    Different data fields can be specified. Request method is POST.
    :param movieID: int number of the movie identifier
    :param rating: the rating object to be submitted
    :return:
    """

def update_rating_single_movie(movieID, rating):
    """
    Updates a rating (consumption) for a certain movie.
    Different fields can be specified. Request method is POST.
    :param movieID: int number of the movie identifier
    :param rating: the rating object to be updated
    :return:
    """

def topN_recommendations_user(N, userID):
    """
    Computes the topN recommendations for this user based on the gathered data and computed tasks
    by the recommender service.
    Request method is GET.
    :param N: amount of recommendation to be retrieved
    :param userID: int number of the user identifier
    :return: # TODO? (possibly a list of recommendations)
    """
    # TODO: there is a query parameter in the API that lets you set how many recommendation to obtain
    # https://www.sugestio.com/documentation/get-personal-recommendations

def rating_history_user(userID):
    """
    Obtains the consumption data (ratings) of a certain user passed by parameter.
    It basically retrieves all the consumption data related to that user.
    :param userID: int number of the user identifier
    :return: # TODO? (possibly a list of consumptions)
    """

def get_metadata_movie(movieID):
    """
    Retrieves the metadata related to a movie which was previously submitted.
    :param movieID: int number of the movie identifier
    :return: metadata object
    """

def read_movie_metadata_and_ratings():
    """
    Reads movie metadata and ratings from Movielens data-set.
    :return: movie metadata, ratings
    """

def submit_movies_metadata_bulk(movies):
    """
    Submits in bulk-fashion all movies passed by parameter.
    :param movies: a collection of movies to be submitted to the recommender service.
    :return:
    """

def submit_movies_ratings_bulk(ratings):
    """
    Submits in bulk-fashion all movies passed by parameter.
    :param ratings: a collection of ratings to be submitted to the recommender service.
    :return:
    """


def main():
    print "HelloWorld! (MAIN)"
    # Load data and parse it:
    mymovies = data.load_dat("movies.csv")
    # myratings = data.load_dat("ratings.csv")


def test():
    """
    This function is used as a test-bed.
    Just for TESTING purposes. It shouldn't be used for production code.
    :return:
    """
    print "HelloWorldTEST!"
    client = sugestio.Client(ACCOUNT, SECRET)
    status, content = client.get_recommendations(1, 5)

    if status == 200:
        print("Title\tScore")
        for recommendation in content:
            print(recommendation.item.title + "\t" + str(recommendation.score))
    else:
        print("server response code:", status)


if __name__ == '__main__':
    main()
    # test()
