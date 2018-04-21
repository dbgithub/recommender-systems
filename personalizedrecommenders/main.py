"""
This file is the main file. The interaction with the recommender service starts here.

"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

import sugestio
from sugestio import Consumption, Item, User
from numpy import mean, median, unique
import data
import utils

# ACCOUNT = 'sandbox'
# SECRET = 'demo'
ACCOUNT = 's2018debla'
SECRET = 'Dzkux4G9k1AZzVCA'
MOVIE_PICKLE_LOCATION = "movies_pickle_10-04-2018--18-59-27.pkl"
RATINGS_PICKLE_LOCATION = "ratings_pickle_05-04-2018--20-02-35.pkl"
LOG_STATUS = True

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
        if LOG_STATUS is True:
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
    con.detail = "STAR:5:0.5:" + str(float(rating['rating']))
    con.date = rating['timestamp']
    status, raw = SUGESTIOCLIENT.add_consumption(con)
    if status == 200 or status == 202:
        if LOG_STATUS is True:
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
        if LOG_STATUS is True:
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
        if LOG_STATUS is True:
            print "[",status,"]: user history retrieved successfully!"
    else:
        print "[",str(status),"]: Something went wrong."
    return status, consumptions


def get_metadata_movie(movieID):
    """
    Retrieves the metadata related to a movie which was previously submitted.
    :param movieID: int number of the movie identifier
    :return: metadata of the movie. It returns a single item containing tuples accessed as attributes of an object
    """
    status, movie = SUGESTIOCLIENT.get_item(movieID)
    if status == 200 or status == 202:
        if LOG_STATUS is True:
            print "[",status,"]: movie retrieved successfully!"
    else:
        print "[",str(status),"]: Something went wrong."
    return status, movie


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
        con.detail = "STAR:5:0.5:" + str(float(rating['rating']))
        con.date = rating['timestamp']
        consumptions.append(con)
    SUGESTIOCLIENT.add_consumptions(consumptions)


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
    # submit_movies_metadata_bulk(movies_pkl.values())
    # submit_movies_ratings_bulk(ratings_pkl)

    # # Question 1:
    print "Question 1: rating of movie 1125 by user 289."
    # s, rating = utils.get_rating(289, 1125)
    # print "\t\t| rating =", utils.decode_stars(rating[0].detail)
    # print "\t\t| date & time =", rating[0].date
    # s, metadata = get_metadata_movie(1125)
    # print "\t\t| title =", metadata.title
    # print "\t\t| genre(s) =",
    # for genre in metadata.category:
    #     print genre,
    # print ""  # this print is just for readability
    # # Question 3:
    print "\nQuestion 3: rating history user 249."
    # s, history = rating_history_user(249)
    # rating_stars = []
    # for rating in history:
    #     s, metadata = get_metadata_movie(rating.itemid)
    #     genres = ""
    #     for genre in metadata.category:
    #         if genres is "":
    #             genres = "{0}".format(genre)
    #         else:
    #             genres = "{0}, {1}".format(genres, genre)
    #     print "\t\t| Movie id =", rating.itemid, ":: Title =", metadata.title, ":: Genre(s) =", genres, ":: Rating =", utils.decode_stars(rating.detail)
    #     rating_stars.append(utils.decode_stars(rating.detail))
    # print "\t\t| Mean =", mean(rating_stars)
    # print "\t\t| Median =", median(rating_stars)
    # print "\t\t| Uniqueness =", dict(zip(*unique(rating_stars, return_counts=True)))
    # # Question 4:
    print "\nQuestion 4: top five collaborative filtering recommendations user 249."
    # s, top5 = topN_recommendations_user(249, 5)
    # for rec in top5:
    #     genres = ""
    #     for genre in rec.item.category:
    #         if genres is "":
    #             genres = "{0}".format(genre)
    #         else:
    #             genres = "{0}, {1}".format(genres, genre)
    #     print "\t\t| Movie id =", rec.item.id, ":: Title =", rec.item.title, ":: Genre(s) =", genres, ":: Score =", rec.score
    # # Question 5:
    print "\nQuestion 5: rating history user 35."
    # s, history = rating_history_user(35)
    # rating_stars = []
    # for rating in history:
    #     s, metadata = get_metadata_movie(rating.itemid)
    #     genres = ""
    #     for genre in metadata.category:
    #         if genres is "":
    #             genres = "{0}".format(genre)
    #         else:
    #             genres = "{0}, {1}".format(genres, genre)
    #     print "\t\t| Movie id =", rating.itemid, ":: Title =", metadata.title, ":: Genre(s) =", genres, ":: Rating =", utils.decode_stars(rating.detail)
    #     rating_stars.append(utils.decode_stars(rating.detail))
    # print "\t\t| Mean =", mean(rating_stars)
    # print "\t\t| Median =", median(rating_stars)
    # print "\t\t| Uniqueness =", dict(zip(*unique(rating_stars, return_counts=True)))
    # # Question 6:
    print "\nQuestion 6: top five collaborative filtering recommendations user 35."
    # s, top5 = topN_recommendations_user(35, 5)
    # for rec in top5:
    #     genres = ""
    #     for genre in rec.item.category:
    #         if genres is "":
    #             genres = "{0}".format(genre)
    #         else:
    #             genres = "{0}, {1}".format(genres, genre)
    #     print "\t\t| Movie id =", rec.item.id, ":: Title =", rec.item.title, ":: Genre(s) =", genres, ":: Score =", rec.score
    # # Question 8:
    print "\nQuestion 8: top five content based recommendations user 249."
    # s, top5 = topN_recommendations_user(249, 5)
    # for rec in top5:
    #     genres = ""
    #     for genre in rec.item.category:
    #         if genres is "":
    #             genres = "{0}".format(genre)
    #         else:
    #             genres = "{0}, {1}".format(genres, genre)
    #     print "\t\t| Movie id =", rec.item.id, ":: Title =", rec.item.title, ":: Genre(s) =", genres, ":: Score =", rec.score
    # # Question 9:
    print "\nQuestion 9: top five content based recommendations user 35."
    # s, top5 = topN_recommendations_user(35, 5)
    # for rec in top5:
    #     genres = ""
    #     for genre in rec.item.category:
    #         if genres is "":
    #             genres = "{0}".format(genre)
    #         else:
    #             genres = "{0}, {1}".format(genres, genre)
    #     print "\t\t| Movie id =", rec.item.id, ":: Title =", rec.item.title, ":: Genre(s) =", genres, ":: Score =", rec.score
    # Question 10a:
    print "\nQuestion 10a: additional raitings for new user 1000."
    # additional_ratings = [
    #     {'userid': 1000, 'movieid': 1590, 'rating': 4.0, 'timestamp': 1476640644},
    #     {'userid': 1000, 'movieid': 1196, 'rating': 4.5, 'timestamp': 1476640644},
    #     {'userid': 1000, 'movieid': 4878, 'rating': 4.0, 'timestamp': 1476640644},
    #     {'userid': 1000, 'movieid': 589, 'rating': 4.5, 'timestamp': 1476640644},
    #     {'userid': 1000, 'movieid': 480, 'rating': 4.5, 'timestamp': 1476640644}
    # ]
    # submit_movies_ratings_bulk(additional_ratings) # Make sure to execute this once and at the correct moment
    # Question 10b:
    print "\nQuestion 10b: rating history user 1000."
    # s, history = rating_history_user(1000)
    # for rating in history:
    #     s, metadata = get_metadata_movie(rating.itemid)
    #     genres = ""
    #     for genre in metadata.category:
    #         if genres is "":
    #             genres = "{0}".format(genre)
    #         else:
    #             genres = "{0}, {1}".format(genres, genre)
    #     print "\t\t| Movie id =", rating.itemid, ":: Title =", metadata.title, ":: Genre(s) =", genres, ":: Rating =", utils.decode_stars(rating.detail)
    # Question 12:
    print "\nQuestion 12: top 10 collaborative filtering recommendations user 1000."
    # s, top10 = topN_recommendations_user(1000, 10)
    # for rec in top10:
    #     genres = ""
    #     for genre in rec.item.category:
    #         if genres is "":
    #             genres = "{0}".format(genre)
    #         else:
    #             genres = "{0}, {1}".format(genres, genre)
    #     print "\t\t| Movie id =", rec.item.id, ":: Title =", rec.item.title, ":: Genre(s) =", genres, ":: Score =", rec.score
    # Question 14:
    print "\nQuestion 14: top 10 content based recommendations user 1000."
    # s, top10 = topN_recommendations_user(1000, 10)
    # for rec in top10:
    #     genres = ""
    #     for genre in rec.item.category:
    #         if genres is "":
    #             genres = "{0}".format(genre)
    #         else:
    #             genres = "{0}, {1}".format(genres, genre)
    #     print "\t\t| Movie id =", rec.item.id, ":: Title =", rec.item.title, ":: Genre(s) =", genres, ":: Score =", rec.score
    # Question 15:
    print "\nQuestion 15: additional rating by user 1000."
    # s = submit_rating_single_movie(6587, {'userid': 1000, 'movieid': 6587, 'rating': 1.0, 'timestamp': 1476640644})
    # s, metadata = get_metadata_movie(6587)
    # genres = ""
    # for genre in metadata.category:
    #     if genres is "":
    #         genres = "{0}".format(genre)
    #     else:
    #         genres = "{0}, {1}".format(genres, genre)
    # print "\t\t| Movie title =", metadata.title, ":: Genre(s) =", genres
    # Question 17:
    print "\nQuestion 17: top 10 content based recommendations user 1000."
    # s, top10 = topN_recommendations_user(1000, 10)
    # for rec in top10:
    #     genres = ""
    #     for genre in rec.item.category:
    #         if genres is "":
    #             genres = "{0}".format(genre)
    #         else:
    #             genres = "{0}, {1}".format(genres, genre)
    #     print "\t\t| Movie id =", rec.item.id, ":: Title =", rec.item.title, ":: Genre(s) =", genres, ":: Score =", rec.score
    # Question 18:
    print "\nQuestion 18: delete all consumptions user 1000."
    # utils.delete_all_consumptions_user(1000)


def test():
    """
    This function is used as a test-bed.
    Just for TESTING purposes. It shouldn't be used for production code.
    :return:
    """
    print "HelloWorldTEST!"

    # -------------------------------
    # Testing library against Sugestio API:

    # client = sugestio.Client(ACCOUNT, SECRET)
    # status, content = client.get_recommendations(1, 5)
    # if status == 200:
    #     print("Title\tScore")
    #     for recommendation in content:
    #         print(recommendation.item.title + "\t" + str(recommendation.score))
    # else:
    #     print("server response code:", status)

    # -------------------------------
    # Testing own implemented methods:

    # Data:
    movies_pkl = data.load_pickle(MOVIE_PICKLE_LOCATION)
    ratings_pkl = data.load_pickle(RATINGS_PICKLE_LOCATION)
    # Testing methods:
    submit_metadata_single_movie(83829, movies_pkl['83829'])
    submit_rating_single_movie(8, ratings_pkl[3500])
    update_rating_single_movie(8, ratings_pkl[200])
    s, recommendations = topN_recommendations_user(1, N=5)
    for i, rec in enumerate(recommendations):
        print "\t\t Recommendation#",i,": ", rec
    s, consumptions = rating_history_user(1)
    for i, con in enumerate(consumptions):
        print "\t\t Consumptions#",i,": ", con
    s, mov = get_metadata_movie(2)
    print "Movie details: ", mov
    submit_movies_metadata_bulk(movies_pkl.values())
    submit_movies_ratings_bulk(ratings_pkl)


if __name__ == '__main__':
    main()
    # test()
