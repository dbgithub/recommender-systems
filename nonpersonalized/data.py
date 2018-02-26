"""
This module is in charge of, among other things: loading the data, creating pickles,
dumping data to pickles, reading from pickles etc.
"""

try:
  import cPickle as pickle
except:
  print "Warning: Couldn't import cPickle, using native pickle instead."
  import pickle
import os
import time
import utils

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

def load_dat(path):
    """
    Loads the data file provided by parameter
    :param path: the path to the file or just the file name
    :return: a list of dictionaries with the corresponding data type
    """
    # First, let's read the .dat file
    try:
        with open(path, 'r') as datfile:
            # We parse the data according to/depending on the data file read:
            if "movies" in path:
                lmovies = {}
                for line in datfile:
                    movie = {}
                    # We split the line based on a delimeter
                    attributes = line.split('::')
                    # We assign the values to a dictionary and insert it in the list of items:
                    movie['id'] = attributes[0]
                    movie['title'] = attributes[1]
                    movie['genre'] = attributes[2].rstrip() # '.rstrip()' removes the trailing '\n' character
                    # print movie['id'], "::", movie['title'], "::", movie['genre']
                    lmovies[attributes[0]] = movie
                return lmovies
            # if "movies" in path:
            #     lmovies = []
            #     for line in datfile:
            #         movie = {}
            #         # We split the line based on a delimeter
            #         attributes = line.split('::')
            #         # We assign the values to a dictionary and insert it in the list of items:
            #         movie['id'] = attributes[0]
            #         movie['title'] = attributes[1]
            #         movie['genre'] = attributes[2].rstrip() # '.rstrip()' removes the trailing '\n' character
            #         # print movie['id'], "::", movie['title'], "::", movie['genre']
            #         lmovies.append(movie)
            #     return lmovies
            elif "ratings" in path:
                lratings = []
                for line in datfile:
                    rating = {}
                    # We split the line based on a delimeter
                    attributes = line.split('::')
                    # We assign the values to a dictionary and insert it in the list of items:
                    rating['userid'] = attributes[0]
                    rating['movieid'] = attributes[1]
                    rating['rating'] = attributes[2]
                    rating['timestamp'] = attributes[3].rstrip() # '.rstrip()' removes the trailing '\n' character
                    # print rating['userid'], "::", rating['movieid'], "::", rating['rating'], "::", rating['timestamp']
                    lratings.append(rating)
                return lratings
    except IOError, err:
        print "[Error] Error while accessing the file (", path, "): ", err
    except Exception, err:
        print "[Error] An error occurred: ", err


def dump_pickle(data, path):
    """
    Creates a pickle with the data provided by parameter
    :param data: data object to pickle
    :param path: file name of the pickle
    :return: nothing
    """
    # First, we check if there is some data to be pickled, otherwise it's no sense to proceed.
    if data is not None:
        if path is "":
            raise ValueError("[Error] A path or file name should be provided, cannot be empty")
        elif not path.endswith(".pkl"):
            raise ValueError("[Error] The provided path should end with: '.pkl' but got %s instead" % path)
        # After checking some requirements of the method, now we check if a file with that name already exists:
        if not os.path.exists(path):
            with open(path, 'wb') as pkl_file:
                pickle.dump(data, pkl_file, pickle.HIGHEST_PROTOCOL)
        else:
            raise IOError("[Error] The provided path or file name already exists. Operation aborted.")


def load_pickle(path_to_pickle):
    if path_to_pickle is "":
        raise ValueError("[Error] A path or file name should be provided, cannot be empty")
    elif not path_to_pickle.endswith(".pkl"):
        raise ValueError("[Error] The provided path should end with: '.pkl' but got %s instead" % path_to_pickle)
    # After checking some requirements of the method, now we check if a file with that name already exists:
    if os.path.exists(path_to_pickle):
        with open(path_to_pickle, 'rb') as pkl_file:
            return pickle.load(pkl_file)
    else:
        raise IOError("[Error] The provided path or file name doesn't exist.")


def generate_file_name(name, file_ext):
    """
    Generates a path with the provided name and extension by parameter plus some unique text
    :param name: desired file name
    :param file_ext: file extension e.g. pkl, txt, csv (WITHOUT THE DOT!)
    :return: a path consisting of a name, unique text and file extension
    """
    if name is "":
        raise ValueError("[Error] A path or file name should be provided, cannot be empty")
    return name + "_pickle_" + time.strftime("%d-%m-%Y--%H-%M-%S", time.localtime()) + "." + file_ext

def main():
    # Load data and parse it:
    # mymovies = load_dat("movies.dat")
    # myratings = load_dat("ratings.dat")
    # Dump the parsed data to pickles into the file system:
    # dump_pickle(mymovies, generate_file_name("movies", "pkl"))
    # dump_pickle(myratings, generate_file_name("ratings", "pkl"))
    # Load the pickles (much faster than loading and parsing again the raw data):
    # mymovies2 = load_pickle("movies_pickle_26-02-2018--17-55-35.pkl")
    mymovies2= load_pickle("movies_pickle_26-02-2018--20-19-52.pkl")
    myratings2 = load_pickle("ratings_pickle_26-02-2018--17-55-35.pkl")
    print len(mymovies2)
    print len(myratings2)
    print mymovies2['3196']
    print myratings2[0]
    utils.plot_top10_rated_distribution(mymovies2,myratings2)

if __name__ == '__main__':
    main()