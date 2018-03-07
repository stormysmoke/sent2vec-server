import numpy
import nltk.tokenize
nltk.download('punkt')

def tokenize(text):
    """
    Tokenize a text into its individual sentences.

    Arguments:
        text:  a unicode object.

    Return:
        A NumPy array of unicode objects.
    """
    return numpy.array(nltk.tokenize.sent_tokenize(text))
