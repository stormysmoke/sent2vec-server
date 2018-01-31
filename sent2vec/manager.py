import numpy
from scipy.spatial.distance import cdist
from scipy.linalg import norm
import skipthoughts.skipthoughts as skipthoughts
from tokenizer import SentenceTokenizer
import util

class Sent2VecManager:
    """
    Manager class for the Sent2Vec semantic sentence search.
    """
    
    __instance = None

    __model = None
    __encoder = None
    __sentences = None
    __vectors = None
    __tokenizer = SentenceTokenizer()

    @staticmethod
    def get_instance():
        """
        Get the unique instance of this singleton class.
        """
        if Sent2VecManager.__instance == None:
            Sent2VecManager()
        return Sent2VecManager.__instance 

    def __init__(self):
        """
        Private, never call this constructor, use "get_instance" instead.
        """
        if Sent2VecManager.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Sent2VecManager.__instance = self

    def load_model(self):
        """
        Load the Sent2Vec encoding model.

        Must be called before calling any of the other instance methods.
        """
        self.__model = skipthoughts.load_model()
        self.__encoder = skipthoughts.Encoder(self.__model)
    
    def read_string(self, text):
        """
        Index all the sentences in a string as vectors.
        """
        self.__sentences = numpy.array(self.__tokenizer.tokenize(text))
        self.__vectors = self.__encoder.encode(self.__sentences)

    def read_file(self, filename):
        """
        Index all the sentences in text file as vectors.
        """
        f = open(filename, 'r')
        self.read_string(f.read())
        f.close()

    def query(self, sentence, k, type="dist"):
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
            return self.__query_dist(sentence, k)
        elif type == "score":
            return self.__query_score(sentence, k)
        else:
            m = "'" + type +"' is not a valid argument for parameter 'type'."
            raise Exception(m)

    def __query_dist(self, sentence, k):
        """
        Query k nearest neighbours with direct distances between vectors.

        The calculated metric is a distance where smaller means nearer.
        """
        vector = self.__encoder.encode([util.str2unicode(sentence)])
        distances = cdist(vector, self.__vectors)[0]
        k_indices = distances.argsort()[:k]
        k_sentences = map(util.unicode2str, self.__sentences[k_indices])
        k_distances = distances[k_indices].tolist()
        return [k_sentences, k_distances]

    def __query_score(self, sentence, k):
        """
        Query k nearest neighbours with original skip-thoughts approach.

        The calculated metric is a "score" where higher means nearer.
        """
        # Note: the following is taken from function "nn" in "skipthoughts.py"
        vector = self.__encoder.encode([util.str2unicode(sentence)])
        # Divide vector by scalar
        vector /= norm(vector)
        # Dot product of query vector with transposition of index vectors.
        # Gives array of scalars, one for each index vector (highest is best).
        scores = numpy.dot(vector, self.__vectors.T).flatten()
        # Indices of k highest "scores" ([::-1] reverses order of array) 
        k_indices = numpy.argsort(scores)[::-1][:k]
        k_sentences = map(util.unicode2str, self.__sentences[k_indices])
        k_scores = scores[k_indices].tolist()
        return [k_sentences, k_scores]
