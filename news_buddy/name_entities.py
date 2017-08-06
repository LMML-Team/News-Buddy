import nltk
from nltk.tokenize import word_tokenize


def tokenize(doc):
    """
    Takes in a document, returns the individual words (no punctuation) in it

    Parameters
    --------------
    doc[str]: One document as a long string

    Returns
    --------------
    tokens[list[str]]: Document broken up into individual words

    """

    # Calls NLTK function to tokenize the document. Broken into individual words, cleans out punctuation
    tokens = nltk.word_tokenize(doc)

    return tokens


def chunk(tokens):
    """
    Takes in tokens, marks them by POS, finds NEs, returns consolidated list of NEs

    Parameters
    --------------
    tokens[list[str]]: Document broken up into individual words

    Returns
    --------------
    NEs[list[str]]: Named entities as items in a list of strings

    """

    # Uses NLTK function to pair each token with its Part Of Speech
    entity_list = []
    pos = nltk.pos_tag(tokens)
    named_entities_chunk = nltk.ne_chunk(pos, binary=True)

    # Finds named entities in tokens, stores in list of strings
    for i in range(0, len(named_entities_chunk)):
        ents = named_entities_chunk.pop()
        if getattr(ents, 'label', None) is not None and ents.label() == "NE":
            entity_list.append([ne for ne in ents])

    # Combines named entity components, pulls off the POF labels
    return [' '.join(next(zip(*l))) for l in entity_list]


def add_entities(doc):
    """
    Takes in a document, returns the named entities in that document

    Parameters
    --------------
    doc[str]: One document as a long string

    Returns
    --------------
    NEs[list[str]]: Named entities as items in a list of strings

    """

    # Calls function to tokenize the document, stores as list of strings
    tokens = tokenize(doc)

    # Calls function to find named entities in the tokens, stores as list of strings
    chunks = chunk(tokens)

    return chunks
