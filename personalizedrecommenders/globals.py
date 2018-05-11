"""
This file stores global variables that can be used across different modules or other Python files.
Normally all required variables or information is obtained/retrieved in the corresponding function, method etc.
However, there are some occasions where due to a large loops, it is recommendable to avoid repetitive jobs/tasks,
such as: reading pickles, calculating a value which is the same for every iteration and doesn't change etc.
"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

LOG_STATUS = False  # bool to indicate whether we want verbose output or not
RATINGS_BY_USER = None  # dictionary with "Key=userID" and "Value=list of ratings by user". A dictionary that hols the ratings by all users
RATINGS_BY_USER_MAP = None  # dictionary with "Key=userID" and "Value=a Dictionary with 'Key=itemID' and 'Value=rating (stars)'"
RATINGS_X_BY_USERS = None  # dictionary with "Key=itemID" and "Value=list of ratings for that item by all users who rated it"
MEAN_RATINGS_ITEM = None  # dictionary with "Key=itemID" and "Value=average of the ratings of all users who rated this item"
IICF_MODEL = None  # this is the model built corresponding to IICF. It's a dictionary with "Key={-1,1}" depending on positive or negative values. "Value=a dictionary with 'Key=itemID' and 'Value=a dictionary with 'Key=itemID' and 'Value=similarity value''"
#                    ____________________IICF_MODEL____________________
#                   |                                                  |
#             -1 (negatives)                                     1 (positives)
#                   |                                                  |
#              (dictionary)                                       (dictionary)
#        ____________________                               ____________________
#       |       |            |                             |       |            |
#    item#1   item#2 ...  item#N                        item#1   item#2 ...  item#N
#       |       |            |                             |       |            |
#      ... (dictionary)     ...                          ...  (dictionary)     ...
#        ____________________                               ____________________
#       |       |            |                             |       |            |
#    item#1   item#2 ...  item#N                        item#1   item#2 ...  item#N
#               |                                                  |
#        similarity value                                   similarity value

class SimilarityType:
    def __init__(self):
        self.__simtype = "POSITIVE"  # by default, the type for similarities is set to "POSITIVE"

    def positive(self):
        if self.__simtype == "BOTH":  # Being 'both' implies that is also 'positive'
            return self.both()
        return "POSITIVE"

    def negative(self):
        if self.__simtype == "BOTH":  # Being 'both' implies that is also 'negative'
            return self.both()
        return "NEGATIVE"

    def both(self):
        return "BOTH"

    def setPositive(self):
        self.__simtype = "POSITIVE"

    def setNegative(self):
        self.__simtype = "NEGATIVE"

    def setBoth(self):
        self.__simtype = "BOTH"

    def type(self):
        return self.__simtype


SIMILARITY_TYPE = None  # this class object defines the similarity type desired. It can either be positive, negative or both.
