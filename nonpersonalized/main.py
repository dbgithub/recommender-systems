"""
This module is the main module. The non-personalized recommender system starts here.

"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

import data
import utils
import operator  # used to sort the (key,value) pairs of a dictionary

MOVIE_PICKLE_LOCATION = "movies_pickle_26-02-2018--20-19-52.pkl"
RATINGS_PICKLE_LOCATION = "ratings_pickle_26-02-2018--17-55-35.pkl"


def calculate_simple_association(movieX, movieY):
    """
    Calculates the simple association value for movieX with respect movieY.
    :param movieX: ID of movie X
    :param movieY: ID of movie Y
    :return: the value computed by the simple association
    """

def calculate_advanced_association(movieX, movieY):
    """
    Calculates the advanced association value for movieX with respect movieY.
    :param movieX: ID of movie X
    :param movieY: ID of movie Y
    :return: the value computed by the advanced association
    """

def topN_movies_simple_association(movieX_ID):
    """
    Retrieves a list of movie IDs with the highest simple association value with respect movieX.
    In case of a tie, the movie with the higher ID is ranked before the movie with lower ID.
    :param movieX_ID: ID of movie X
    :return: a list of movie IDs
    """

def topN_movies_advanced_association(movieX_ID):
    """
    Retrieves a list of movie IDs with the highest advanced association value with respect movieX.
    In case of a tie, the movie with the higher ID is ranked before the movie with lower ID.
    :param movieX_ID: ID of movie X
    :return: a list of movie IDs
    """

def topN_most_rated_movies():
    """
    Retrieves a list of movie names and another list with their corresponding ratings which are the
    most rated movies.
    :return: a list of (most rated) movie names AND a list of their ratings as well. Ordered from BIG to SMALL.
    """
    aggregated_ratings = {}
    top10_movies = []
    top10_ratings = []
    # First, let's load the data:
    movies = data.load_pickle(MOVIE_PICKLE_LOCATION)
    ratings = data.load_pickle(RATINGS_PICKLE_LOCATION)
    # Now, we will iterate over all ratings and we will aggregate/count all ratings for every movie:
    for elem in ratings:
        if not elem['movieid'] in aggregated_ratings:
            aggregated_ratings[elem['movieid']] = 1
        else:
            aggregated_ratings[elem['movieid']] += 1
    # print "Num elements (aggregated dictionary): ", len(aggregated_ratings)
    # 'sorted' function sorts the dictionary from small to big, returns a list:
    mysorted = sorted(aggregated_ratings.items(), key=operator.itemgetter(1))
    # We take the last 10 elements from the tail:
    mysorted = mysorted[-10:]
    # We reverse the order of the items within the list. Now the first item in the list is the most rated movie ID.
    mysorted.reverse()
    # print mysorted
    # Instead of returning movie IDs, we will return movie NAMES:
    for elem in mysorted:
        top10_movies.append(movies[elem[0]]['title'])
        top10_ratings.append(elem[1])
    return top10_movies, top10_ratings

def main():
    # Load data and parse it:
    # mymovies = load_dat("movies.dat")
    # myratings = load_dat("ratings.dat")
    # Dump the parsed data to pickles into the file system:
    # dump_pickle(mymovies, generate_file_name("movies", "pkl"))
    # dump_pickle(myratings, generate_file_name("ratings", "pkl"))
    # Load the pickles (much faster than loading and parsing again the raw data):
    movies_pkl = data.load_pickle(MOVIE_PICKLE_LOCATION)
    ratings_pkl = data.load_pickle(RATINGS_PICKLE_LOCATION)
    print len(movies_pkl)
    print len(ratings_pkl)
    print movies_pkl['3196']
    print ratings_pkl[0]
    # Show top10 rated movies:
    top10_movies, top10_ratings = topN_most_rated_movies()
    utils.plot_top10_rated_distribution(top10_movies, top10_ratings)


if __name__ == '__main__':
    main()