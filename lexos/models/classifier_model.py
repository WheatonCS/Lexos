"""This is a model to produce an SVM classifier."""

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
from lexos.receivers.classifier_reciever import ClassifierOptions, \
    ClassifierReceiver
from lexos.receivers.matrix_receiver import MatrixReceiver
from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.models.matrix_model import MatrixModel
import lexos.managers.utility as utility
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


"""
import nltk
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from sklearn.feature_extraction.text import CountVectorizer,
TfidfVectorizer
from sklearn.preprocessing import LabelBinarizer
from lexos.models.file_manager_model import FileManagerModel

"""


class ClassifierTestOption(NamedTuple):
    """A named tuple to hold test options."""

    doc_term_matrix: pd.DataFrame
    document_label_map: DocumentLabelMap
    front_end_option: ClassifierOptions
    token_type_str: str


class ClassifierResult(NamedTuple):
    """A typed tuple to hold topword results."""
    header: str
    score: int
    author: str


class ClassifierModel(BaseModel):
    """The Classifer model inherits from the base model.

    Note: Feature count is set to top 100 words currently.
    If this is changed the training data will need to be remade.
    With the correct number of features.
    To do this, simply run the data generation code offline.
    Then, save the new training data and list in the test folder.
    MAKE SURE to use a novel text from an obscure author.
    The classifier needs to learn against someone distinct.
    If you give it the same author twice, it will perform terribly.
    Choose an author who, reasonably, no one else will ever  model.
    A good choice is yourself, or a friend, with no publications."""


    feature_count = 100

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
            else MatrixModel().get_matrix()
            # the get_matrix function returns the normalized dtm
            # need to set the correct normalization options on front
            # other than that it's taken care of

    @property
    def _document_label_map(self) -> DocumentLabelMap:
        """:return: a map takes an id to temp labels."""
        return self._test_document_label_map \
            if self._test_document_label_map is not None \
            else utility.get_active_document_label_map()

    @property
    def _classifier_option(self) -> ClassifierOptions:
        """:return: the front end option of bootstrap consensus tree."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else ClassifierReceiver().options_from_front_end()

    @property
    def _token_type_str(self) -> str:
        """:return: A string that represents the token type used."""
        if self._test_token_type_str is not None:
            return self._test_token_type_str
        else:
            # Get dtm front end options.
            dtm_options = MatrixReceiver().options_from_front_end()
            # Get the correct current type.
            token_type = dtm_options.token_option.token_type
            return "Terms" if token_type == "Tokens" else "Characters"

    def _get_file_col_dtm(self) -> pd.DataFrame:
        """Get DTM with documents as columns and terms/characters as rows.

        :return: A pandas data frame that contains the DTM where each document
                 is a column with total and average added to the original DTM.
        """
        # Check if empty DTM is received.
        assert not self._doc_term_matrix.empty, EMPTY_DTM_MESSAGE

        labels = [self._document_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Transpose the dtm for easier calculation.
        file_col_dtm = self._doc_term_matrix.transpose()

        file_col_dtm.columns = labels

        # Find total and average of each row's data.
        file_col_dtm.insert(loc=0, column="Total",
                            value=file_col_dtm.sum(axis=1))

        file_col_dtm.insert(loc=1, column="Average",
                            value=file_col_dtm["Total"] /
                            self._doc_term_matrix.shape[0])

        return file_col_dtm.round(4)

    def _trim_data_set(self) -> pd.DataFrame:
        """Trim the DTM down to the top 100 words."""
        # get the DTM
        dtm = self._get_file_col_dtm()

        # sort DTM by word count from highest to lowest
        dtm_sorted = dtm.sort_values(
            by=[dtm.columns[self._front_end_option.sort_column-1]],
            ascending=self._front_end_option.sort_method
        ) if self._front_end_option.sort_column != 0 \
            else dtm.sort_index(ascending=self._front_end_option.sort_method)

        # return sliced down DTM
        sliced_dtm = dtm_sorted.iloc[0: feature_count]
        return sliced_dtm


    def _get_auth_list(self, author_name: str):
        "return a list of the author"
        return name_list = [author_name] * feature_count


    def _fit_model(self, word_list, authors_list, margin_softener, kernel):
        """Fits an SVM model for the specified author.

        Args:
        words: List of words to be used as features.
        author: string of the author's name.

        Returns:
        svm: the fitted SVM model.

        Notes:
        C = 2 was found to be the best margin softener.
        This took a lot of testing with a grid SVC.
        It is possible that a non-integer C is better.
        If someone wants to see if that's true go ahead.
        I'm choosing to leave it as an integer.
        If a float is better it will likely be 1<C<2.
        This is as 1 was the second best performing int.

        The Linear kernel was a compromise but is the best choice.
        An RBF kernel provides up to a 4% increase in predictive power.
        However, it is 334% slower for fittings.
        This time cost is preventative in a web context.
        To accomodate this, accuracy was sacrificed.
        """
        svm = SVC(C= margin_softener, kernel= kernel)
        # Fit bag of words svm
        svm.fit(word_list, authors_list)
        return svm

    def _predict_model(self, model, data):
        """Make predictions on a dataset with the model.

        Args:
        model: the model for predictions.
        data: the dataset for predictions.

        Returns:
        predections: the predections made by the model.
        """
        predictions = model.predict(data)
        return predictions

    def _save_model(self, model, author_name):
        """Save a model to disk.

        Args:
        model: the model for saving the.
        author_name: the author name for accuratly naming the file.
        """
        filename = author_name + "_finalized_model.sav"
        pickle.dump(model, open(filename, 'wb'))

    def _load_model(self, author_name):
        """Load a model from disk.

        Args:
        author_name: the name of the author for loading the model.
        """
        filename = author_name + "_finalized_model.sav"
        loaded_model = pickle.load(open(filename, 'rb'))
        return loaded_model

    def _get_result(self) -> ClassifierResult:
        """Call the right method based on user selection

        :return: a namedtuple that holds the classifier result, which contains a
            header and a list of pandas series.

        :TODO: add in loading models.
        """
        # Starting the model as none for error checking.
        model = None

        # Randomly chose 1 of 3 persistent datsets
        # Stored at that path
        choice = str(random.randint(1, 3)) + ".txt"
        path = '../test/Classifier/PersistentData/'
        data_path = path + choice
        auth_path = path + 'auth.txt'

        # Create a base for the data and authors
        # To be trained and tested against
        # Both are hardset at len(100)
        base_data = pd.read_csv(data_path, header= None)
        base_auth = pd.read_csv(auth_path, header= None)
        
        classifier_option = self._classifier_option

        # Get the top 100 words from the TF/IDF
        # normed DTM and the author's name 100 times
        # and append them to the base sets
        data = self._trim_data_set()
        data = data.append(base_data)
        author = self._get_auth_list(classifier_option.author_name)
        author = author.append(base_auth)

        # Zip the data and author sets and 
        # randomly shuffle them, then unzip them
        zipped = list(zip(data, author))
        random.shuffle(zipped)
        data, author = zip(*zipped)

        # Create an 80/20 test/train split of both sets
        data_train, data_test, author_train, author_test = \
            train_test_split(data, author, test_size = 0.2, random_state = 5)

        # Fit a model on the training data
        if classifier_option.fit_model and classifier_option.kernel is not None \
            and classifier_option.margin_softener is not None:
            model = self._fit_model(data_train, author_train, 
                classifier_option.margin_softener, classifier_option.kernel)
        
        # Predict on the test data and score the predictions
        if classifier_option.predict and classifier_option.trial_count is not None \
            and model is not None:
            pred_list = []
            acc_list = []

            for i in range(classifier_option.trial_count):
                results.self._predict_model(model, data_test)

            for pred in pred_list:
                acc_list.append(accuracy_score(author_test, pred))

            accuracy = average(acc_list)
            max_acc = max(acc_list)
            min_acc = min(acc_list)

        else:
            raise ValueError("Missing model for predictions.")