import pickle
from collections import Counter, defaultdict


class EntityDatabase:
    def __init__(self):
        self.database = defaultdict(Counter)

    def chunks_to_db(self, doc_id, chunks):
        """
        Takes in chunks that represent keywords from a document and updates a dictionary that associates
        document IDs with a Counter of their entities.

        Parameters
        ----------
        doc_id:
            String of the document ID containing the chunks.
        chunks: iter[str]
            Iterable of chunks from the document "doc_id"
        """
        self.database[doc_id].update(chunks)

    def store_database(self, filename="entity_db"):
        """
        Stores the database in a pickle file in binary mode as filename.pickle.

        Parameters
        ----------
        filename: str
            Path to and file name of the desired save location.
        """
        pickle.dump(self.database, open(filename + ".pickle", "wb"))

    def read_database(self, filename):
        """
        Returns a Counter of the database that was store in a pickle file.

        Parameters
        ----------
        filename: str
            Path and file name of database save location.

        """
        self.database = pickle.load(open(filename, "rb"))

    def get_top_associations(self, entity, k=2):
        """
        Returns the top k associations for a given entity. Currently requires exact spelling and cases.

        Parameters
        ----------
        entity: str
            Entity for associations to be returned.
        k: int
            Number of top associations desired.

        Returns
        -------
        Tuple(str):
            Tuple of top associations with entity.
        """

        associations = Counter()
        for counter in self.database.values():
            if entity in counter.keys():
                associations.update(counter)

        associations.pop(entity)
        return list(zip(*associations.most_common(k)))[0]

    def get_top_associations_document(self, doc_id, k=2):
        """
        Returns the top k entities from one given documents

        Parameters
        ----------
        doc_id: str
            Desired document ID

        Returns
        -------
        Tuple(str):
            Tuple of the top k entities of a document
        """
        return list(self.database[doc_id].most_common(k))