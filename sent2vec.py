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


def knn(query, record, k):
    """
    Find k-nearest-neighbours to a query sentence in a previously encoded text.

    Arguments:
        query:    the query sentence as a unicode object
        record:   a dict with keys 'sent' and 'vec' as returned by 'encode'
        k:        number of nearest neighbours to return

    Return:
        A dict with the keys 'sent' and 'dist'. The value of 'sent' is a list
        of the k nearest sentences to the query sentence. The value of 'dist'
        is a list of the distances of these sentences to the query sentence.
    """
    query_vec = _encoder.encode([query])
    distances = cdist(query_vec, record['vec'])[0]
    knn_indices = distances.argsort()[:k].tolist()
    s = record['sent'][knn_indices].tolist()
    d = distances[knn_indices].tolist()
    return dict(sent=s, dist=d)
