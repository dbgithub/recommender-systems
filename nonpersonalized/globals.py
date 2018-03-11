"""
This file stores global variables that can be used across different modules or other Python files.
Normally all required variables or information is obtained/retrieved in the corresponding function, method etc.
However, there are some occasions where due to a large loop, it is recommendable to avoid repetive jobs/taks,
such as: reading pickles, calculating a value which is the same for every iteration and doesn't change etc.
"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

AMOUNT_RATED_X = None
RATINGS_BY_USER = None
