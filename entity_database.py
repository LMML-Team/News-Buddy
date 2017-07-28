import pickle
from collections import Counter


def chunks_to_db(chunks, database):
    """
    Takes in chunks that represent keywords from a document and creates/updates a dictionary that associates entities
    with keywords.

    Parameters
    ----------
    chunks: iter[str]
        Iterable of chunks from a single document
    database: list[Counter]
        Existing database of list of counts of entities per each document.

    Returns
    -------
    entity_db: list[Counter]
        Database of entities' associations.
    """
    database.append(Counter(chunks))

    return database


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


def read_database(filename):
    """
    Takes a file of a database and returns a Counter.

    Parameters
    ----------
    filename: str
        Path and file name of database save location

    Returns
    -------
    list[Counter]:
        Entity database

    """
    return pickle.load(open(filename, "rb"))