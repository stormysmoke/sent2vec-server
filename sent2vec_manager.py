import numpy
import uuid
from scipy.spatial.distance import cdist
from scipy.linalg import norm
import skipthoughts.skipthoughts as skipthoughts
import util

__model = None
__encoder = None
__sentences = None
__vectors = None

def init():
    """
    Initialise the Sent2Vec encoder.

    Must be called before calling any of the other functions.
    """
    global __model
    global __encoder
    __model = skipthoughts.load_model()
    __encoder = skipthoughts.Encoder(__model)

def index_string(text):
    """
    Index all the sentences of a block of text string as vectors.
    """
    global __sentences
    global __vectors
    id = str(uuid.uuid4())
    __sentences = numpy.array(util.get_sentences(text))
    __vectors = __encoder.encode(__sentences)
    return id

def index_file(filename):
    """
    Index all the sentences in a text file as vectors.
    """
    f = open(filename, 'r')
    id = index_string(f.read())
    f.close()
    return id

def query(sentence, k, type="dist"):
    """
    Given a sentence, get its k nearest neighbours among the previously
    indexed sentences.

    Arguments:
        sentence:  string
        k:         the number of nearest neighbours to return
        type:      kNN algorithm, either 'dist' (default) or 'score'

    Returns:
        A list with two elements: the first element is a list with the k
        nearest neighbour sentences (strings), and the second element is
        a list of floats with the "distances" or "scores", respectively,
        of the query sentence w.r.t. the k nearest neighbour sentences.
        The latter depends on the value of 'type', i.e. 'dist' or 'score'.
    """
    if type == "dist":
        return __query_dist(sentence, k)
    elif type == "score":
        return __query_score(sentence, k)
    else:
        m = "'" + type +"' is not a valid argument for parameter 'type'."
        raise Exception(m)

def __query_dist(sentence, k):
    """
    Query k nearest neighbours with direct distances between vectors.

    The calculated metric is a distance where smaller means nearer.
    """
    vector = __encoder.encode([util.str2unicode(sentence)])
    distances = cdist(vector, __vectors)[0]
    k_indices = distances.argsort()[:k]
    k_sentences = map(util.unicode2str, __sentences[k_indices])
    k_distances = distances[k_indices].tolist()
    return [k_sentences, k_distances]

def __query_score(sentence, k):
    """
    Query k nearest neighbours with original skip-thoughts approach.

    The calculated metric is a "score" where higher means nearer.
    """
    # Note: the following is taken from function "nn" in "skipthoughts.py"
    vector = __encoder.encode([util.str2unicode(sentence)])
    # Divide vector by scalar
    vector /= norm(vector)
    # Dot product of query vector with transposition of index vectors.
    # Gives array of scalars, one for each index vector (highest is best).
    scores = numpy.dot(vector, __vectors.T).flatten()
    # Indices of k highest "scores" ([::-1] reverses order of array) 
    k_indices = numpy.argsort(scores)[::-1][:k]
    k_sentences = map(util.unicode2str, __sentences[k_indices])
    k_scores = scores[k_indices].tolist()
    return [k_sentences, k_scores]
