"""this is a model to produce an SVM classifier."""

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from keras.preprocessing.text import one_hot

from typing import Optional, NamedTuple
import pandas as pd
import numpy as np
import random
import string
import pickle
from lexos.models.base_model import BaseModel
from lexos.receivers.matrix_receiver import DocumentLabelMap
from lexos.receivers.classifier_reciever import ClassifierOption
from sklearn.svm import SVC


"""
import nltk
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from sklearn.feature_extraction.text import CountVectorizer,
TfidfVectorizer
from sklearn.preprocessing import LabelBinarizer
from lexos.models.matrix_model import MatrixModel
from lexos.models.file_manager_model import FileManagerModel
import lexos.managers.utility as utility
ClassifierReciver
"""


class ClassifierTestOption(NamedTuple):
    """A named tuple to hold test options."""

    doc_term_matrix: pd.DataFrame
    document_label_map: DocumentLabelMap
    front_end_option: ClassifierOption
    token_type_str: str


class ClassifierModel(BaseModel):
    """The Classifer model inherits from the base model."""

    def __init__(self, test_options: Optional[ClassifierTestOption] = None):
        """Generate a classification model.

        :param test_options: The input used in testing to override the
                             dynamically loaded option.
        """
        super().__init__()
        if test_options is not None:
            self._test_dtm = test_options.doc_term_matrix
            self._test_token_type_str = test_options.token_type_str
            self._test_front_end_option = test_options.front_end_option
            self._test_document_label_map = test_options.document_label_map
        else:
            self._test_dtm = None
            self._test_token_type_str = None
            self._test_front_end_option = None
            self._test_document_label_map = None

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:
        """:return: The document term matrix."""
        return self._test_dtm if self._test_dtm is not None \
            else ().get_matrix()

    def sentencize(self, min_char):
        """Convert text file to a list of sentences.

        Args:
        filepath: string. Filepath of text file.
        min_char: int. Minimum number of characters required
        for a sentence to be included.
        Returns:
        sentences: list of strings.
        List of sentences containined in the text file.
        """
        """
        # Load data into string variable and remove new line characters
        # Split text into a list of sentences
        sentences = tokenize.sent_tokenize(text)
        # Remove sentences that are less than min_char long
        sentences = [sent for sent in sentences if len(sent) >= min_char]

        return list(sentences)
        """
        return 1

    def combine_data(self, text_dict, author_name):
        """Combine data.

        Args:
        text_dict: a dictionary of the text.
        author_name: the author's name.

        This funntion is more than likely deprecated.
        This service will be performed by other parts of Leoxs.
        TODO: Delete or rework
        """
        np.random.seed(1)

        # Set length parameter
        max_len = 8500

        """Select sentences
        names = [subject_data, other]
        """
        names = []
        combined = []

        for name in names:
            name = np.random.choice(name, max_len, replace=False)
            combined += list(name)

        labels = [author_name]*max_len + ['Other']*max_len
        random.seed(3)

        # Randomly shuffle data
        zipped = list(zip(combined, labels))
        random.shuffle(zipped)
        combined, labels = zip(*zipped)

        out_data = pd.DataFrame()
        out_data['text'] = combined
        out_data['author'] = labels
        out_data.to_csv('author_data.csv', index=False)

    def preprocess_data(self, filename):
        """Preprocessing for data.

        Args:
        filename: name of the file to get the data from.

        TODO: Remove this. This fucntion is completely deprecated.
        The things that it does are done by Lexos.
        Make notes on what it does and find out how to replicate.
        """
        data = pd.read_csv(filename, encoding="utf-8")
        text = list(data['text'].values)
        author = list(data['author'].values)
        """Counter(author)"""

        word_count = []
        char_count = []

        for i in range(len(text)):
            word_count.append(len(text[i].split()))
            char_count.append(len(text[i]))

        # Convert lists to numpy arrays
        word_count = np.array(word_count)
        char_count = np.array(char_count)

        # Calculate average word lengths

        text = [excerpt.replace('\xa0', '') for excerpt in text]
        new_text = []

        for excerpt in text:
            while "  " in excerpt:
                excerpt = excerpt.replace("  ", " ")
            new_text.append(excerpt)

        text = new_text
        normed_text = []

        for i in range(len(text)):
            new = text[i].lower()
            new = new.translate(str.maketrans('', '', string.punctuation))
            new = new.replace('“', '').replace('”', '')
            normed_text.append(new)
        return_dict = {"Normed_text": normed_text, "Author": author}
        return return_dict

    def process_data(self, excerpt_list):
        """Stem data, remove stopwords and split into word lists.

        Args:
        excerpt_list: list of strings. List of normalized text excerpts.
        Returns:
        processed: list of strings.
        List of lists of processed text excerpts
        (stemmed and stop words removed).
        """
        stop_words = set(stopwords.words('english'))
        porter = PorterStemmer()

        processed = []

        for excerpt in excerpt_list:
            new = excerpt.split()
            word_list = [porter.stem(w) for w in new if w not in stop_words]
            word_list = " ".join(word_list)
            processed.append(word_list)

        return processed

    def create_n_grams(self, excerpt_list, n, vocab_size, seq_size):
        """Create a list of n-gram sequences.

        Args:
        excerpt_list: list of strings. List of normalized text excerpts.
        n: int. Length of n-grams.
        vocab_size: int. Size of n-gram vocab (used in one-hot encoding)
        seq_size: int. Size of n-gram sequences
        Returns:
        n_gram_array: array. Numpy array of one-hot encoded n-grams.
        """
        n_gram_list = []

        for excerpt in excerpt_list:
            # Remove spaces
            excerpt = excerpt.replace(" ", "")

            # Extract n-grams
            n_grams = [excerpt[i:i + n] for i in range(len(excerpt) - n + 1)]

            # Convert to a single string with spaces between n-grams
            new_string = " ".join(n_grams)

            # One hot encode
            hot = one_hot(new_string, round(vocab_size*1.3))

            # Pad hot if necessary
            hot_len = len(hot)
            if hot_len >= seq_size:
                hot = hot[0:seq_size]
            else:
                diff = seq_size - hot_len
                extra = [0]*diff
                hot = hot + extra

            n_gram_list.append(hot)

        n_gram_array = np.array(n_gram_list)

        return n_gram_array

    def get_vocab_size(self, excerpt_list, n, seq_size):
        """Calculate size of n-gram vocab.

        Args:
        excerpt_list: list of strings. List of normalized text excerpts.
        n: int. Length of n-grams.
        seq_size: int. Size of n-gram sequences.

        Returns:
        vocab_size: int. Size of n-gram vocab.
        """
        n_gram_list = []

        for excerpt in excerpt_list:
            # Remove spaces
            excerpt = excerpt.replace(" ", "")

            # Extract n-grams
            n_grams = [excerpt[i:i + n] for i in range(len(excerpt) - n + 1)]

            # Create list of n-grams
            gram_len = len(n_grams)
            if gram_len >= seq_size:
                n_grams = n_grams[0:seq_size]
            else:
                diff = seq_size - gram_len
                extra = [0]*diff
                n_grams = n_grams + extra

            n_gram_list.append(n_grams)

        # Flatten n-gram list
        n_gram_list = list(np.array(n_gram_list).flat)

        # Calculate vocab size
        n_gram_cnt = 1  # Counter(n_gram_list)
        vocab_size = len(n_gram_cnt)

        return vocab_size

    def fit_model(self, words, author):
        """Fits an SVM model for the specified author.

        Args:
        words: List of words to be used as features.
        author: string of the author's name.

        Returns:
        svm: the fitted SVM model.
        """
        svm = SVC(C=1, kernel='linear')
        # Fit bag of words svm
        np.random.seed(6)
        svm.fit(words, author)
        return svm

    def predict_model(self, model, data):
        """Make predictions on a dataset with the model.

        Args:
        model: the model for predictions.
        data: the dataset for predictions.

        Returns:
        predections: the predections made by the model.
        """
        predictions = model.predict(data)
        return predictions

    def save_model(self, model, author_name):
        """Save a model to disk.

        Args:
        model: the model for saving the.
        author_name: the author name for accuratly naming the file.
        """
        filename = author_name + "_finalized_model.sav"
        pickle.dump(model, open(filename, 'wb'))

    def load_model(self, author_name):
        """Load a model from disk.

        Args:
        author_name: the name of the author for loading the model.
        """
        filename = author_name + "_finalized_model.sav"
        loaded_model = pickle.load(open(filename, 'rb'))
        return loaded_model
