import nltk
from nltk.tokenize import word_tokenize

def tokenize(doc):
    """
    
    
    
    """

    tokens = nltk.word_tokenize(doc)
    return tokens()

def chunk(tokens):
    """
    
    
    
    """
    entity_list = []
    pos = nltk.pos_tag(tokens)
    named_entities_chunk = nltk.ne_chunk(pos, binary=True)

    for i in range(0, len(named_entities)):
        ents = named_entities_chunk.pop()
        if getattr(ents, 'label', None) != None and ents.label() == "NE":
            entity_list.append([ne for ne in ents])

    return [' '.join(next(zip(*l))) for l in entity_list]

def add_entities(doc):
    tokens = tokenize(doc)
    return (chunk(tokens))
