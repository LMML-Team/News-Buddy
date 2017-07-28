import pickle
from collections import Counter


def chunks_to_db(doc_id, chunks, database):
    """
    Takes in chunks that represent keywords from a document and updates a dictionary that associates
    document IDs with a Counter of their entities.

    Parameters
    ----------
    doc_id:
        String of the document ID containing the chunks.
    chunks: iter[str]
        Iterable of chunks from the document "doc_id"
    database: defaultdict{str: Counter}
        Dictionary containing count of entities per each document

    Returns
    -------
    entity_db: defaultdict{str: Counter}
        Dictionary containing count of entities per each document
    """
    database[doc_id].update(chunks)

    return database


def store_database(database, filename="entity_db"):
    """
    Given a database, stores it in a pickle file in binary mode as filename.pickle.

    Parameters
    ----------
    database: dict
        Entity database.
    filename: str
        Path to and file name of the desired save location.
    """
    pickle.dump(database, open(filename + ".pickle", "wb"))


def read_database(filename):
    """
    Takes a file of a database and returns a Counter.

    Parameters
    ----------
    filename: str
        Path and file name of database save location.

    Returns
    -------
    defaultdict{str: Counter}
        Entity database.

    """
    return pickle.load(open(filename, "rb"))


def get_top_associations(entity, database, k=2):
    """
    Returns the top k associations for a given entity. Currently requires exact spelling and cases.

    Parameters
    ----------
    entity: str
        Entity for associations to be returned.
    database: dict{str: Counter}
        Database of associations between entities.
    k: int
        Number of top associations desired.

    Returns
    -------
    Tuple(str):
        Tuple of top associations with entity.
    """

    associations = Counter()
    for counter in database.values():
        if entity in counter.keys():
            associations.update(counter)

    associations.pop(entity)
    return list(zip(*associations.most_common(k)))[0]


def get_top_associations_document(doc_id, database, k=2):
    """
    Returns the top k entities from one given documents

    Parameters
    ----------
    doc_id: str
        Desired document ID
    database: defaultdict{str: Counter}
        Database of entities in document ids

    Returns
    -------
    Tuple(str):
        Tuple of the top k entities of a document
    """
    return list(database[doc_id].most_common(k))