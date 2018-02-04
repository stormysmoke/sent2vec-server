import nltk.tokenize


"""
Various utility functions.
"""

def str2unicode(s):
    """
    Convert a string to a UTF-8 Unicode object.

    If the passed object is already unicode, then it is returned unchaged.
    """
    if isinstance(s, unicode):
        return s
    else:
        return s.decode('utf-8')

def unicode2str(u):
    """
    Convert a UTF-8 Unicode object to a string.

    If the passed object is already a string, then it is returned unchanged.
    """
    if isinstance(u, str):
        return u
    else:
        return u.encode('utf-8')

def get_sentences(text):
    """
    Tokenize a text into a list of sentences.

    Arguments:
        text:  a string or unicode object

    Returns:
        A list of UTF-8 unicode objects.
    """
    # Note: the implementation of this function loads a PunktSentenceTokenizer
    # with nltk.data.load('tokenizers/punkt/english.pickle'). This requires
    # the 'punk' corpus of NLTK Data to be installed.
    return nltk.tokenize.sent_tokenize(str2unicode(text))
