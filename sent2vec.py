import sent_tokenizer
import skipthoughts.skipthoughts as skipthoughts
from scipy.spatial.distance import cdist

_encoder = None

def init():
    """
    Initialise the Sent2Vec encoder.

    This includes loading the model, which may take several minutes! This
    function must be called before any other function in this module.
    """
    global _encoder
    model = skipthoughts.load_model()
    _encoder = skipthoughts.Encoder(model)


def encode(text):
    """
    Encode all the sentences of a text as vectors.

    Arguments:
        text:  a unicode object containing multiple sentences.

    Return:
        A dict with the keys 'sent' and 'vec'. The value of 'sent' is a NumPy
        array with the individual sentences of the provided text (as unicode
        objects). The value of 'vec' is a NumPy array of numerical vectors, one
        vector for each sentence in 'sent'.
    """
    sent = sent_tokenizer.tokenize(text)
    vec = _encoder.encode(sent)
    return dict(sent=sent, vec=vec)


def knn(query, vec_arr, k=3):
    """
    Given a query sentence and the vector encodings of a previously encoded
    text, get the k-nearest-neighbours to the query sentence in the provided
    array of vectors.

    Arguments:
        query:    a unicode object representing a sentence.
        vec_arr:  a NumPy array of vectors as returned by encode()
        k:        an integer specifying the number of nearest neighbours

    Return:
        A dict with the keys 'i' and 'dist'. The value of 'i' is a list of
        integers indicating the indices of the k nearest neighbours in the
        provided array of vectors. The value of 'dist' is a list of floats
        indicating the distances of these k nearest neighbours to the query
        sentence (smaller values mean "closer together").
    """
    vec_query = _encoder.encode([query])
    dist_arr = cdist(vec_query, vec_arr)[0]
    i = dist_arr.argsort()[:k].tolist()
    dist = dist_arr[i].tolist()
    return dict(i=i, dist=dist)
