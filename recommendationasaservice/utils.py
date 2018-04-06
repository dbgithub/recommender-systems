"""
This module is called 'utils' because it owns miscellaneous methods that can come in handy
in different scenarios throughout the project/application.

For instance, statistics methods, subroutines for main methods in main, etc.
"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

import sugestio


def delete_all_consumptions_user(userID):
    """
    Deletes all consumptions made by user identified by userID.
    :param userID: int number of the user identifier
    :return:
    """