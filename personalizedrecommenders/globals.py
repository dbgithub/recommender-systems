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
IICF_MODEL = None  # this is the model built corresponding to IICF
