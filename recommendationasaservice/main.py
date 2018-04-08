"""
This file is the main file. The interaction with the recommender service starts here.

"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

import sugestio
from sugestio import Consumption, Item, User
import data
import utils

ACCOUNT = 'sandbox'
SECRET = 'demo'
# ACCOUNT = 's2018debla'
# SECRET = 'Dzkux4G9k1AZzVCA'
MOVIE_PICKLE_LOCATION = "movies_pickle_05-04-2018--20-02-35.pkl"
RATINGS_PICKLE_LOCATION = "ratings_pickle_05-04-2018--20-02-35.pkl"

# Declare Sugestio client (using already existing Sugestio library for python):
# Info: https://github.com/sugestio/sugestio-python
SUGESTIOCLIENT = sugestio.Client(ACCOUNT, SECRET)


def submit_metadata_single_movie(movieID, metadata):
    """
    Submits information about the movie with ID passed by parameter.
    Different data fields can be specified. Request method is POST.
    :param movieID: int number of the movie identifier
    :param metadata: a dictionary containing the metadata about the movie to be added
    :return: int status
    """
    item = Item(movieID)
    item.title = metadata['title']
    genres = metadata['genre'].split('|')
    for genre in genres:
        item.category.append(genre)
    status, raw = SUGESTIOCLIENT.add_item(item)
    if status == 200 or status == 202:
        print "[",status,"]: Movie metadata submitted successfully!"
    else:
        print "[",str(status),"]: Something went wrong."
    return status


def submit_rating_single_movie(movieID, rating):
    """
    Submits a rating (consumption) for a certain movie.
    Different data fields can be specified. Request method is POST.
    :param movieID: int number of the movie identifier
    :param rating: the rating object to be submitted
    :return: int status
    """
    con = Consumption(rating['userid'], movieID)
    con.type = "RATING"
    con.detail = "STAR:5:1:" + str(int(rating['rating']))
    con.date = rating['timestamp']
    status, raw = SUGESTIOCLIENT.add_consumption(con)
    if status == 200 or status == 202:
        print "[",status,"]: Rating for single movie submitted/updated successfully!"
    else:
        print "[",str(status),"]: Something went wrong."
    return status


def update_rating_single_movie(movieID, rating):
    """
    Updates a rating (consumption) for a certain movie.
    Different fields can be specified. Request method is POST.
    :param movieID: int number of the movie identifier
    :param rating: the rating object to be updated
    :return: int status
    """
    # In order to differentiate between submit and update I declared two methods, but they eventually
    # do the same thing behind the scenes. The reason is to
    return submit_rating_single_movie(movieID, rating)


def topN_recommendations_user(userID, N = None):
    """
    Computes the topN recommendations for this user based on the gathered data and computed tasks
    by the recommender service.
    Request method is GET.
    :param userID: int number of the user identifier
    :param N: amount of recommendation to be retrieved
    :return: int status and a list of recommendations
    """
    # Check if N is none, raise an error if yes.
    try:
        if N is None:
            raise AttributeError
        if not isinstance(N, int):
            raise ValueError
    except AttributeError:
        print "[Error] Parameter value missing. N is none"
    except ValueError:
        print "[Error] N is not an int, it should be an int number"
    status, recommendations = SUGESTIOCLIENT.get_recommendations(userID, limit=N)
    if status == 200 or status == 202:
        print "[",status,"]: top N recommendations retrieved successfully!"
    else:
        print "[",str(status),"]: Something went wrong."
    return status, recommendations


def rating_history_user(userID):
    """
    Obtains the consumption data (ratings) of a certain user passed by parameter.
    It basically retrieves all the consumption data related to that user.
    :param userID: int number of the user identifier
    :return: int status and a list of consumptions
    """
    status, consumptions = SUGESTIOCLIENT.get_user_consumptions(userID)
    if status == 200 or status == 202:
        print "[",status,"]: user history retrieved successfully!"
    else:
        print "[",str(status),"]: Something went wrong."
    return status, consumptions


def get_metadata_movie(movieID):
    """
    Retrieves the metadata related to a movie which was previously submitted.
    :param movieID: int number of the movie identifier
    :return: metadata object
    """
    status, movie = SUGESTIOCLIENT.get_item(movieID)
    if status == 200 or status == 202:
        print "[",status,"]: movie retrieved successfully!"
    else:
        print "[",str(status),"]: Something went wrong."
    return status, movie


def read_movie_metadata_and_ratings():
    """
    TODO: this method is a candidate to be deleted!
    Reads movie metadata and ratings from Movielens data-set.
    :return: movie metadata, ratings
    """


def submit_movies_metadata_bulk(movies):
    """
    Submits in bulk-fashion all movies passed by parameter.
    :param movies: a collection of movies to be submitted to the recommender service.
    :return:
    """
    items = []
    for movie in movies:
        item = Item(movie['id'])
        item.title = movie['title']
        genres = movie['genre'].split('|')
        for genre in genres:
            item.category.append(genre)
    items.append(item)
    SUGESTIOCLIENT.add_items(items)


def submit_movies_ratings_bulk(ratings):
    """
    Submits in bulk-fashion all movies passed by parameter.
    :param ratings: a collection of ratings to be submitted to the recommender service.
    :return:
    """
    consumptions = []
    for rating in ratings:
        con = Consumption(rating['userid'], rating['movieid'])
        con.type = "RATING"
        con.detail = "STAR:5:1:" + str(int(rating['rating']))
        con.date = rating['timestamp']
        consumptions.append(con)
    SUGESTIOCLIENT.add_consumptions(consumptions)


def main():
    print "HelloWorld! (MAIN)"
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


def test():
    """
    This function is used as a test-bed.
    Just for TESTING purposes. It shouldn't be used for production code.
    :return:
    """
    print "HelloWorldTEST!"
    # Testing library against Sugestio API:
    # client = sugestio.Client(ACCOUNT, SECRET)
    # status, content = client.get_recommendations(1, 5)
    # if status == 200:
    #     print("Title\tScore")
    #     for recommendation in content:
    #         print(recommendation.item.title + "\t" + str(recommendation.score))
    # else:
    #     print("server response code:", status)

    # Testing own implemented methods:
    # Dummy rating:
    dummyrating = {'userid': 671, 'movieid': 8, 'rating':4.0, 'timestamp': 1260759182}
    dummyrating2 = {'userid': 1, 'movieid': 9, 'rating':2.0, 'timestamp': 1260759182}  # dummy rating changed
    dummyratings = []
    dummyratings.append(dummyrating)
    dummyratings.append(dummyrating2)
    # Dummy movies:
    dummymovie1 = {'id': 10, 'title': 'invented movie', 'genre': 'horror|comedy'}
    dummymovie2 = {'id': 5, 'title': 'yet another invented movie', 'genre': 'adventure|drama'}
    dummymovies = []
    dummymovies.append(dummymovie1)
    dummymovies.append(dummymovie2)
    # Data:
    movies_pkl = data.load_pickle(MOVIE_PICKLE_LOCATION)
    ratings_pkl = data.load_pickle(RATINGS_PICKLE_LOCATION)
    # Testing methods:
    submit_metadata_single_movie(4, movies_pkl['4'])
    submit_rating_single_movie(8, dummyrating)
    update_rating_single_movie(8, dummyrating2)
    topN_recommendations_user(1, N=5)
    rating_history_user(1)
    get_metadata_movie(2)
    submit_movies_metadata_bulk(dummymovies)
    submit_movies_ratings_bulk(dummyratings)


if __name__ == '__main__':
    # main()
    test()
