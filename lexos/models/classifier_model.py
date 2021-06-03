
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelBinarizer
from sklearn.svm import SVC

from keras.preprocessing.text import one_hot

from typing import Optional, NamedTuple
import pandas as pd


import pickle

from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import DocumentLabelMap
from lexos.models.file_manager_model import FileManagerModel
import lexos.managers.utility as utility
from lexos.receivers.classifier_reciever import ClassifierOption, ClassifierReceiver

"""

Programmer: Torin Praeger, tpraeger@gmail.com
If some future Lexos group winds up working on this tool, please only contact me
for help on it if you actually have tried to understand it and haven't been able to.

Explination of this code dated 2021/4/11:
As it stands, Lexos is not a useful framework for what this tool is attempting
to do. That is subject to change, and if it does I will try to walk you
through what I did.

Lexos only allows tokenization of the corpus by words and characters. This is
because Lexos uses the sklearn CountVectorizer() (scikit ver. 0.24.1) to tokenize.
To create a good classifier for author atribution we want to tokenize by sentences.
Lexos also creates a DTM every time a tool runs, meaning the DTM is not a
persistent object throughout the Lexos tools. The same is true for vocabulary sizes
and n-grams, the tools that generate them do it each time they are called, and not
in a persistent or overarching way.

With all of this in mind I have elected to create a group of functions that are
insular, in that they are not connected to Lexos in any way other than that they
use it as a vehicle to recive the text data and return the model's work on it.
This gives me far more control over what I can do with the text processing,
with almost no preformance impact as Lexos already does this kind of work
every time an analyze tool is used.

Libraries:
-nltk ver. 3.6 for: Sentence tokenizing
-keras from TensorFlow2 for: one-hot encoding
-scikit-learn ver. 0.24.1 for: creating SVM model, training model, predicting
with model, getting average score
-pickle ver. 3.9 for: saving and loading models


Know issues:
-Feature counts are non-standard between models, right now sklearn will not
allow a model to predict on data it wasn't trained on. This is obviously a
massive blow to the usefulness of the tool, top priority fix.

-pickle is not a safe or prefered library for saving models, you can learn
why on your own. It would be far better to learn the actual form of an
sklearn model and save it as a JSON array

"""

class ClassifierTestOption(NamedTuple):
    doc_term_matrix: pd.DataFrame
    document_label_map: DocumentLabelMap
    front_end_option: ClassifierOption
    token_type_str: str

class ClassifierModel(BaseModel):

    def __init__(self, test_options: Optional[ClassifierTestOption] = None):

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
            else    ().get_matrix()

    
    def sentencize(min_char):
        """Convert text file to a list of sentences.
        
        Args:
        filepath: string. Filepath of text file.
        min_char: int. Minimum number of characters required for a sentence to be
        included.

        Returns:
        sentences: list of strings. List of sentences containined in the text file.
        """
        # Load data into string variable and remove new line characters
        
        
        # Split text into a list of sentences
        sentences = tokenize.sent_tokenize(text)
        
        # Remove sentences that are less than min_char long
        sentences = [sent for sent in sentences if len(sent) >= min_char]

        return list(sentences)

    def combine_data(text_dict,author_name):
        np.random.seed(1)

        # Set length parameter
        max_len = 8500

        # Select sentences
        names = [subject_data, other]
        combined = []

        for name in names:
            name = np.random.choice(name, max_len, replace = False)
            combined += list(name)

        print('The length of the combined list is:', len(combined))

        labels = [author_name]*max_len + ['Other']*max_len

        print('The length of the labels list is:', len(labels))

        random.seed(3)

        # Randomly shuffle data
        zipped = list(zip(combined, labels))
        random.shuffle(zipped)
        combined, labels = zip(*zipped)

        out_data = pd.DataFrame()
        out_data['text'] = combined
        out_data['author'] = labels

        print(out_data.head())

        out_data.to_csv('author_data.csv', index=False)

    def preprocess_data(filename):
        data = pd.read_csv(filename, encoding="utf-8")
        text = list(data['text'].values)
        author = list(data['author'].values)
        Counter(author)

        word_count = []
        char_count = []

        for i in range(len(text)):
            word_count.append(len(text[i].split()))
            char_count.append(len(text[i]))

        # Convert lists to numpy arrays
        word_count = np.array(word_count)
        char_count = np.array(char_count)

        # Calculate average word lengths
        text_string = ''

        text = [excerpt.replace('\xa0', '') for excerpt in text]

        new_text = []

        for excerpt in text:
            while "  " in excerpt:
                excerpt = excerpt.replace("  "," ")
            new_text.append(excerpt)

        text = new_text
        normed_text = []

        for i in range(len(text)):
            new = text[i].lower()
            new = new.translate(str.maketrans('','', string.punctuation))
            new = new.replace('“', '').replace('”', '')
            normed_text.append(new)
        return_dict = {"Normed_text" : normed_text, "Author" : author}
        return return_dict

    def process_data(excerpt_list):
        """Stem data, remove stopwords and split into word lists
        
        Args:
        excerpt_list: list of strings. List of normalized text excerpts.
        
        Returns:
        processed: list of strings. List of lists of processed text excerpts (stemmed and stop words removed).
        """
        stop_words = set(stopwords.words('english'))
        porter = PorterStemmer()
        
        processed = []
        
        for excerpt in excerpt_list:
            new = excerpt.split()
            word_list = [porter.stem(w) for w in new if not w in stop_words]
            word_list = " ".join(word_list)
            processed.append(word_list)
        
        return processed

    def create_n_grams(excerpt_list, n, vocab_size, seq_size):
        """Create a list of n-gram sequences
        
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
        
    def get_vocab_size(excerpt_list, n, seq_size):
        """Calculate size of n-gram vocab
        
        Args:
        excerpt_list: list of strings. List of normalized text excerpts.
        n: int. Length of n-grams.
        seq_size: int. Size of n-gram sequences
        
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
        n_gram_cnt = Counter(n_gram_list)
        vocab_size = len(n_gram_cnt)
        
        return vocab_size

    def fit_model(words,author):
        svm = SVC(C = 1, kernel = 'linear')
        # Fit bag of words svm
        np.random.seed(6)
        svm.fit(words, author)
        return svm

    def predict_model(model,data):
        predictions = model.predict(data)
        return predictions

    def save_model(model,author_name):
        filename = author_name+"_finalized_model.sav"
        pickle.dump(model, open(filename, 'wb'))

    def load_model(author_name):
        filename = author_name+"_finalized_model.sav"
        loaded_model = pickle.load(open(filename, 'rb'))
        return loaded_model
