import pickle
from collections import defaultdict, Counter

def chunks_to_db(chunks, database=None):
    """
    Takes in chunks that represent keywords from a document and creates/updates a dictionary that associates entities
    with keywords.

    Parameters
    ----------


    """
    pass


def store_database(database, filename="entity_db"):
    """
    Given a database, stores it in a pickle file in binary mode as filename.pickle.

    Parameters
    ----------
    database: dict
        Entity database
    filename: str
        Path to and file name of the desired save location
    """
    pickle.dump(database, open(filename + ".pickle", "wb"))