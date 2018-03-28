"""
This file is the main file. The interaction with the recommender service starts here.

"""

__author__ = "Aitor De Blas Granja"
__email__ = "aitor.deblas@ugent.be"

# import data
# import utils
import sugestio

ACCOUNT = 'sandbox'
SECRET = 'demo'
# ACCOUNT = 's2018debla'
# SECRET = 'Dzkux4G9k1AZzVCA'

def main():
    print "HelloWorld!"


def test():
    """
    This function is used as a test-bed.
    Just for TESTING purposes. It shouldn't be used for production code.
    :return:
    """
    print "HelloWorldTEST!"
    client = sugestio.Client(ACCOUNT, SECRET)
    status, content = client.get_recommendations(1, 5)

    if status == 200:
        print("Title\tScore")
        for recommendation in content:
            print(recommendation.item.title + "\t" + str(recommendation.score))
    else:
        print("server response code:", status)


if __name__ == '__main__':
    # main()
    test()
