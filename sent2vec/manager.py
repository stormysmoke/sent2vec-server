import numpy
from scipy.spatial.distance import cdist
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

    def query(self, sentence, k):
        """
        Given a sentence, get its k nearest neighbours among the previously
        indexed sentences.
        """
        vector = self.__encoder.encode([sentence])
        distances = cdist(vector, self.__vectors)[0]
        k_indices = distances.argsort()[:k]
        k_sentences = map(util.unicode2str, self.__sentences[k_indices])
        k_distances = distances[k_indices].tolist()
        return [k_sentences, k_distances]
