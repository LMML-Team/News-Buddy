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
    entity_list = []
    pos = nltk.pos_tag(tokens)
    named_entities_chunk = nltk.ne_chunk(pos, binary=True)

    for i in range(0, len(named_entities_chunk)):
        ents = named_entities_chunk.pop()
        if getattr(ents, 'label', None) != None and ents.label() == "NE":
            entity_list.append([ne for ne in ents])

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
    tokens = tokenize(doc)
    return (chunk(tokens))