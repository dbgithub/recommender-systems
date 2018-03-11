"""
This module is the main module. The non-personalized recommender system starts here.

"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

import data
import utils
import operator  # used to sort the (key,value) pairs of a dictionary
import globals  # a file to store global variables to use them across all Python files

MOVIE_PICKLE_LOCATION = "movies_pickle_26-02-2018--20-19-52.pkl"
RATINGS_PICKLE_LOCATION = "ratings_pickle_26-02-2018--17-55-35.pkl"


def calculate_simple_association(movieX, movieY, ratings=None):
    """
    Calculates the simple association value for movieX with respect movieY.
    :param movieX: ID of movie X
    :param movieY: ID of movie Y
    :param ratings: collection of all ratings. If available at calling time, then it can be used, otherwise it will be
    locally retrieved.
    :return: the value computed by the simple association
    """
    # First get the data (preferably by parameter otherwise from pickles):
    if ratings is None:
        ratings = data.load_pickle(RATINGS_PICKLE_LOCATION)  # Movies data-set not needed, just ratings.
    XY = float(utils.how_many_X_and_Y(movieX, movieY, ratings))
    X = globals.AMOUNT_RATED_X
    if X is None:
        X = utils.how_many_Z(movieX, ratings)
    value = XY/X
    return value

def calculate_advanced_association(movieX, movieY, ratings=None):
    """
    Calculates the advanced association value for movieX with respect movieY.
    :param movieX: ID of movie X
    :param movieY: ID of movie Y
    :param ratings: collection of all ratings. If available at calling time, then it can be used, otherwise it will be
    locally retrieved.
    :return: the value computed by the advanced association
    """
    # First get the data (preferably by parameter otherwise from pickles):
    if ratings is None:
        ratings = data.load_pickle(RATINGS_PICKLE_LOCATION)  # Movies data-set not needed, just ratings.
    X = globals.AMOUNT_RATED_X
    if X is None:
        X = utils.how_many_Z(movieX, ratings)
    Y = utils.how_many_Z(movieY, ratings)
    XY = utils.how_many_X_and_Y(movieX, movieY, ratings)
    notX = len(ratings) - X
    notXY = Y - XY
    try:
        value = (float(XY)/X)/(float(notXY)/notX)
        return value
    except ZeroDivisionError, err:
        print "[ERROR] ", err
        print "X = ", X
        print "XY = ", XY
        print "notXY = ", notXY
        print "notX = ", notX
        return 0.0

def topN_movies_simple_association(movieX_ID, N=10):
    """
    Retrieves a list of movie IDs with the highest simple association value with respect movieX.
    In case of a tie, the movie with the higher ID is ranked before the movie with lower ID.
    :param movieX_ID: ID of movie X
    :param N: number of movies to put in the returned list (topN)
    :return: a list of movie IDs
    """
    # First get the data (preferably from pickles):
    movies = data.load_pickle(MOVIE_PICKLE_LOCATION)
    ratings = data.load_pickle(RATINGS_PICKLE_LOCATION)
    # To SPEED UP the execution of the algorithm and avoid repetitive jobs/tasks, we will obtain/retrieve now:
    # - How many times movie X was rated
    # - A collection of all ratings indexed by user
    # Normally you would obtain this info in another more appropriate (inner) methods, but since we are now iterating
    # over all movies, there are some variables or data that is common to every iteration, thus we obtain it outside the
    # loop. These are global variables that can be consulted from other modules or Python files.
    globals.AMOUNT_RATED_X = utils.how_many_Z(movieX_ID, ratings)
    globals.RATINGS_BY_USER = utils.extract_ratings_by_user(ratings)

    # Now, we will iterate over all movies to calculate their respective simple association value given the movieX ID.
    sa_values = []  # A list of tuples with the following form: "(movieID, association value)"

    for i, movieY_ID in enumerate(movies.keys()):  # movies.keys()[:100]
        sa_values.append((int(movieY_ID), calculate_simple_association(movieX_ID, movieY_ID, ratings)))
        print "(i=", i, ")Appended movie: ", movieY_ID
    mysorted = sorted(sa_values, key=operator.itemgetter(1, 0), reverse=True)  # tuples sorted from BIG to SMALL association value
    mysorted = mysorted[:N]  # we are interested just in the top N tuples
    topN = []
    for elem in mysorted:
        topN.append((elem[0], elem[1], movies[str(elem[0])]['title']))
    return topN


def topN_movies_advanced_association(movieX_ID, N=10):
    """
    Retrieves a list of movie IDs with the highest advanced association value with respect movieX.
    In case of a tie, the movie with the higher ID is ranked before the movie with lower ID.
    :param movieX_ID: ID of movie X
    :param N: number of movies to put in the returned list (topN)
    :return: a list of movie IDs
    """
    # First get the data (preferably from pickles):
    movies = data.load_pickle(MOVIE_PICKLE_LOCATION)  # Ratings data-set is not needed in this case.
    ratings = data.load_pickle(RATINGS_PICKLE_LOCATION)
    # To SPEED UP the execution of the algorithm and avoid repetitive jobs/tasks, we will obtain/retrieve now:
    # - How many times movie X was rated
    # - A collection of all ratings indexed by user
    # Normally you would obtain this info in another more appropriate (inner) methods, but since we are now iterating
    # over all movies, there are some variables or data that is common to every iteration, thus we obtain it outside the
    # loop. These are global variables that can be consulted from other modules or Python files.
    globals.AMOUNT_RATED_X = utils.how_many_Z(movieX_ID, ratings)
    globals.RATINGS_BY_USER = utils.extract_ratings_by_user(ratings)

    # Now, we will iterate over all movies to calculate their respective simple association value given the movieX ID.
    aa_values = []  # A list of tuples with the following form: "(movieID, association value)"

    for i, movieY_ID in enumerate(movies.keys()):  # movies.keys()[:100]
        aa_values.append((int(movieY_ID), calculate_advanced_association(movieX_ID, movieY_ID, ratings)))
        print "(i=", i, ")Appended movie: ", movieY_ID
    mysorted = sorted(aa_values, key=operator.itemgetter(1, 0), reverse=True)  # tuples sorted from BIG to SMALL association value
    mysorted = mysorted[:N]  # we are interested just in the top N tuples
    topN = []
    for elem in mysorted:
        topN.append((elem[0], elem[1], movies[str(elem[0])]['title']))
    return topN


def topN_most_rated_movies(N=10, stars=None):
    """
    Retrieves a list of movie names and another list with their corresponding ratings which are the
    most rated movies.
    :param N: number of movies to put in the returned list (topN)
    :param stars: number of stars (integer) for which movies will be extracted for the topN
    :return: a list of (most rated) movie names AND a list of their ratings as well. Ordered from BIG to SMALL.
    """
    aggregated_ratings = {}
    topN_movies = []
    topN_ratings = []
    # First, let's load the data:
    movies = data.load_pickle(MOVIE_PICKLE_LOCATION)
    ratings = data.load_pickle(RATINGS_PICKLE_LOCATION)
    # Now, we will iterate over all ratings and we will aggregate/count all ratings for every movie:
    for elem in ratings:
        if stars is not None and int(elem['rating']) >= stars:
            continue
        if not elem['movieid'] in aggregated_ratings:
            aggregated_ratings[elem['movieid']] = 1
        else:
            aggregated_ratings[elem['movieid']] += 1
    # print "Num elements (aggregated dictionary): ", len(aggregated_ratings)
    # 'sorted' function sorts the dictionary from SMALL to BIG, returns a list:
    mysorted = sorted(aggregated_ratings.items(), key=operator.itemgetter(1), reverse=True)
    # We take the first N elements (Top N):
    mysorted = mysorted[:N]
    # Instead of returning movie IDs, we will return movie NAMES:
    for elem in mysorted:
        topN_movies.append(movies[elem[0]]['title'])
        topN_ratings.append(elem[1])
    return topN_movies, topN_ratings


def main():
    # Load data and parse it:
    # mymovies = data.load_dat("movies.dat")
    # myratings = data.load_dat("ratings.dat")
    # Dump the parsed data to pickles into the file system:
    # data.dump_pickle(mymovies, generate_file_name("movies", "pkl"))
    # data.dump_pickle(myratings, generate_file_name("ratings", "pkl"))
    # Load the pickles (much faster than loading and parsing again the raw data):
    movies_pkl = data.load_pickle(MOVIE_PICKLE_LOCATION)
    ratings_pkl = data.load_pickle(RATINGS_PICKLE_LOCATION)


def test():
    """
    This function is used as a test-bed.
    Just for TESTING purposes. It shouldn't be used for production code.
    :return:
    """
    # Load data and parse it:
    # mymovies = data.load_dat("movies.dat")
    # myratings = data.load_dat("ratings.dat")
    # Dump the parsed data to pickles into the file system:
    # data.dump_pickle(mymovies, generate_file_name("movies", "pkl"))
    # data.dump_pickle(myratings, generate_file_name("ratings", "pkl"))
    # Load the pickles (much faster than loading and parsing again the raw data):
    movies_pkl = data.load_pickle(MOVIE_PICKLE_LOCATION)
    ratings_pkl = data.load_pickle(RATINGS_PICKLE_LOCATION)
    print "len(movies_pkl): ", len(movies_pkl)
    print "len(ratings_pkl): ", len(ratings_pkl)
    # print movies_pkl['3196']
    # print ratings_pkl[0]

    # Plot top10 rated movies with/without stars:
    # top10_movies, top10_ratings = topN_most_rated_movies(10)
    # utils.plot_top10_rated_distribution(top10_movies, top10_ratings)

    # Get top10 rated movies with/without stars:
    # top10_movies, top10_ratings = topN_most_rated_movies(10, 4)
    # for movietitle in top10_movies:
    #     print movietitle

    # How many instances rated X and Y at the same time:
    # result = utils.how_many_X_and_Y(1, 2858, ratings_pkl)
    # print result, "times were movie '1' and movie '2858' rated by users"

    # How many times was movie X ranked:
    # result = utils.how_many_Z(3941, ratings_pkl)
    # print "How many times was movie X rated? = ", result

    # Calculate simple association value example:
    # value = calculate_simple_association(1,1064)
    # print "Simple association value of movie 1 w.r.t to movie 1064: ", value

    # Calculate advanced association value example:
    # value = calculate_advanced_association(1,1064)
    # print "Advanced association value of movie 1 w.r.t to movie 1064: ", value

    # Retrieve topN movies with highest simple association value w.r.t ID 3941:
    # print "topN movies with highest simple association value w.r.t ID 3941:"
    # topn = topN_movies_simple_association(3941)
    # for item in topn:
    #     print item

    # Retrieve topN movies with highest advanced association value w.r.t ID 3941:
    # print "topN movies with highest advanced association value w.r.t ID 3941"
    # topn = topN_movies_advanced_association(3941)
    # for item in topn:
    #     print item


if __name__ == '__main__':
    # main()
    test()
