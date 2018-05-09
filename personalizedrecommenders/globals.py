"""
This file stores global variables that can be used across different modules or other Python files.
Normally all required variables or information is obtained/retrieved in the corresponding function, method etc.
However, there are some occasions where due to a large loops, it is recommendable to avoid repetitive jobs/tasks,
such as: reading pickles, calculating a value which is the same for every iteration and doesn't change etc.
"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

LOG_STATUS = True  # bool to indicate whether we want verbose output or not
RATINGS_BY_USER = None  # dictionary with "Key=userID" and "Value=list of ratings by user". A dictionary that hols the ratings by all users