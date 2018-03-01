"""
This module is the main module. The non-personalized recommender system starts here.

"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

import data
import utils

def calculate_simple_association(movieX, movieY):
    """
    Calculates the simple association value for movieX with respect movieY.
    :param movieX: ID of movie X
    :param movieY: ID of movie Y
    :return:
    """

def calculate_advanced_association(movieX, movieY):
    """
    Calculates the advanced association value for movieX with respect movieY.
    :param movieX: ID of movie X
    :param movieY: ID of movie Y
    :return:
    """

def topN_movies_simple_association(movieX_ID):
    """
    Retrieves a list of movie IDs with the highest simple association value with respect movieX
    :param movieID:
    :return:
    """

def main():
    # Load data and parse it:
    # mymovies = load_dat("movies.dat")
    # myratings = load_dat("ratings.dat")
    # Dump the parsed data to pickles into the file system:
    # dump_pickle(mymovies, generate_file_name("movies", "pkl"))
    # dump_pickle(myratings, generate_file_name("ratings", "pkl"))
    # Load the pickles (much faster than loading and parsing again the raw data):
    # mymovies2 = load_pickle("movies_pickle_26-02-2018--17-55-35.pkl") # This pickle has another data structure for Movies.
    mymovies2 = data.load_pickle("movies_pickle_26-02-2018--20-19-52.pkl")
    myratings2 = data.load_pickle("ratings_pickle_26-02-2018--17-55-35.pkl")
    print len(mymovies2)
    print len(myratings2)
    print mymovies2['3196']
    print myratings2[0]
    # Show topN rated movies:
    utils.plot_top10_rated_distribution(mymovies2, myratings2)


if __name__ == '__main__':
    main()