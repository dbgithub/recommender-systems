"""
This file is in charge, among other things, of: loading the data, creating pickles,
dumping data to pickles, reading from pickles etc.
"""

try:
    import cPickle as pickle
except:
    print "Warning: Couldn't import cPickle, using native pickle instead."
    import pickle
import os
import time
import csv

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

def load_dat(path):
    """
    Loads the data file provided by parameter.
    :param path: the path to the file or just the file name
    :return: a list of dictionaries or a dictionary with the corresponding data type
    """
    # First, let's try reading the .dat file. Then we will parse it.
    try:
        with open(path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)  # creation of a CSV reader
            fields = []
            for i, row in enumerate(csvreader):
                print "i=",i," -> ", row
                if "127164" in row:
                    fields = row
            for elem in fields:
                print elem
            # We parse the data according to/depending on the data file read (it can either be movies or ratings):
            # if "movies" in path:
            #     lmovies = {}  # A dictionary indexed by movie ID containing the movie object itself.
            #     for line in csvfile:
            #         movie = {}
            #         # We split the line based on a delimeter
            #         attributes = line.split('::')
            #         # We assign the values to a dictionary and insert it in the list of items:
            #         movie['id'] = attributes[0]
            #         movie['title'] = attributes[1]
            #         movie['genre'] = attributes[2].rstrip() # '.rstrip()' removes the trailing '\n' character
            #         # print movie['id'], "::", movie['title'], "::", movie['genre']
            #         lmovies[attributes[0]] = movie
            #     return lmovies
            # elif "ratings" in path:
            #     lratings = []  # A collection of ratings with their corresponding fields.
            #     for line in csvfile:
            #         rating = {}
            #         # We split the line based on a delimeter
            #         attributes = line.split('::')
            #         # We assign the values to a dictionary and insert it in the list of items:
            #         rating['userid'] = attributes[0]
            #         rating['movieid'] = attributes[1]
            #         rating['rating'] = attributes[2]
            #         rating['timestamp'] = attributes[3].rstrip()  # '.rstrip()' removes the trailing '\n' character
            #         # print rating['userid'], "::", rating['movieid'], "::", rating['rating'], "::", rating['timestamp']
            #         lratings.append(rating)
            #     return lratings
    except IOError, err:
        print "[Error] Error while accessing the file (", path, "): ", err
    except Exception, err:
        print "[Error] An error occurred: ", err


def dump_pickle(data, path):
    """
    Creates a pickle with the data provided by parameter and the name/path of the file.
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
        # After checking some requirements (error checking), now we check if a file with that name already exists:
        if not os.path.exists(path):
            with open(path, 'wb') as pkl_file:
                pickle.dump(data, pkl_file, pickle.HIGHEST_PROTOCOL)
        else:
            raise IOError("[Error] The provided path or file name already exists. Operation aborted.")


def load_pickle(path_to_pickle):
    """
    Loads a pickle and returns it. The path of the location of the pickle is provided by parameter.
    :param path_to_pickle: path to the pickle
    :return:
    """
    if path_to_pickle is "":
        raise ValueError("[Error] A path or file name should be provided, cannot be empty")
    elif not path_to_pickle.endswith(".pkl"):
        raise ValueError("[Error] The provided path should end with: '.pkl' but got %s instead" % path_to_pickle)
    # After checking some requirements (error checking), now we check if a file with that name already exists:
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
