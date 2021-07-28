"""This is a model to return function word sets for
the classifier."""

class LanguageModel():
    def __init__(self):
        eng_func_words = ['a', 'all', 'and', 'as', 'at', 'be', 'but', 
        'by', 'could', 'for', 'from', 'had', 'he', 'her', 'his', 'in', 
        'it', 'not', 'of', 'on', 'said', 'she', 'that', 'the', 'to', 
        'was', 'were', 'which', 'with']
        # Function words are words that serve to carry context
        # without independent meaning. We use this type of word
        # for classification as they allow us to avoid missing
        # the authorship of a document due to overfitting the 
        # model on unique words pertaining to the document's topic. 
        # For more information, and help finding useful function 
        # words sets for additional languages refer to,
        # https://sites.ualberta.ca/~dmiall/Computing/Readings/Burrows_1989.pdf

        self.func_word_dict = {"English":eng_func_words}

    def _get_func_word(self, language:str) -> list:
        """:return: a list of function words for the chosen language"""
        return self.func_word_dict[language]
