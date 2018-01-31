from nltk.tokenize import PunktSentenceTokenizer
import util

# TODO: some texts omit the periods at the end of bullet point list entries.
# Solve this problem by e.g. recognising blank lines as sentence delimiters.

class SentenceTokenizer:
    """
    Sentence tokenizer for Sent2Vec.

    Split a block of text into a list of sentences in a "smart" way. For example,
    recognise the periods in "i.e." not as ends of sentences, but as part of an
    abbreviation.
    """

    __tokenizer = None


    def __init__(self):
        self.__tokenizer = PunktSentenceTokenizer()


    def tokenize(self, text):
        """
        Split a string into a list of sentences.

        Arguments:
            text:  a string

        Returns:
             A list of UTF-8 Unicode objects.
        """
        return self.__tokenizer.tokenize(util.str2unicode(text))
