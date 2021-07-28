"""This is a model to produce an SVM classifier."""

from typing import Optional, NamedTuple
import pandas as pd
import numpy as np
import random
import string
import pickle
import lexos.managers.utility as utility
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.tokenize import TweetTokenizer

from lexos.models.base_model import BaseModel
from lexos.receivers.matrix_receiver import DocumentLabelMap
from lexos.receivers.classifier_reciever import ClassifierOptions, \
    ClassifierReceiver
from lexos.receivers.matrix_receiver import MatrixReceiver
from lexos.processors.prepare.cutter import cut
from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.helpers.languages import LanguageModel
from lexos.models.matrix_model import MatrixModel

import plotly.graph_objs as go
from flask import jsonify
from plotly.offline import plot

class ClassifierTestOption(NamedTuple):
    """A named tuple to hold test options."""

    doc_term_matrix: pd.DataFrame
    document_label_map: DocumentLabelMap
    front_end_option: ClassifierOptions
    token_type_str: str


class ClassifierResult(NamedTuple):
    """A typed tuple to hold classification results."""
    header: str
    score: int
    author: str


class ClassifierModel(BaseModel):
    """The Classifer model inherits from the base model."""

    def __init__(self, test_options: Optional[ClassifierTestOption] = None):
        """Generate a classification model.

        :param test_options: The input used in testing to override the
                             dynamically loaded option.
        """
        super().__init__()
        self.model = None
        self.author_data = None
        if test_options is not None:
            self._test_dtm = test_options.doc_term_matrix
            self._test_token_type_str = test_options.token_type_str
            self._test_front_end_option = test_options.front_end_option
            self._test_document_label_map = test_options.document_label_map
            self._test_class_division_map = test_options.division_map
        else:
            self._test_dtm = None
            self._test_token_type_str = None
            self._test_front_end_option = None
            self._test_document_label_map = None
            self._test_class_division_map = None

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:
        """:return: The document term matrix."""
        classifier_option = self._classifier_option
        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel()._get_raw_count_matrix(\
            Vocabulary=LanguageModel._get_func_word(\
            language = classifier_option.language))

    @property
    def _test_data(self):
        """:return the dtm of the training data"""
        classifier_option = self._classifier_option
        drac_path = "../../test/test_suite/classifier/\
            PersistentData/Dracula_0"
        huck_path = "../../test/test_suite/classifier/\
            PersistentData/Huckleberry_Finn_0"
        pride_path = "../../test/test_suite/classifier/\
            PersistentData/Pride_and_Prejudice_0"
        
        drac_text = []
        huck_text = []
        pride_text = []
        for i in range(1,10):
            with open(drac_path+str(i)+".txt") as f:
                drac_text.append(f.read())
            with open(huck_path+str(i)+".txt") as f:
                huck_text.append(f.read())
            with open(pride_path+str(i)+".txt") as f:
                pride_text.append(f.read())
        train_list = []
        train_list.extend(drac_text,huck_text,pride_text)
        tk = TweetTokenizer()

        count_vector = CountVectorizer(
        input='content', encoding='utf-8', min_df=1,
        analyzer=self._opts.token_option.token_type,
        vocabulary = Vocabulary, lowercase=False,
        ngram_range=(self._opts.token_option.n_gram_size,
                        self._opts.token_option.n_gram_size),
        stop_words=[], dtype=float, max_df=1.0,
        tokenizer=tk.tokenize)

        transformer = TfidfTransformer(smooth_idf=False)
        
        dtm_before_tfidf = count_vector.fit_transform(file_contents)
        dtm = transformer.fit_transform(dtm_before_tfidf) 
        return dtm
    
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

    @property
    def _class_division_map(self) -> pd.DataFrame:
        """:return: a pandas data frame that holds the class division map."""
        return self._test_class_division_map \
            if self._test_class_division_map is not None else \
            FileManagerModel().load_file_manager().get_class_division_map()

    def _get_author_name(self) -> list:
        """:return: a list of the targets"""
        try:
            class_labels = self._class_division_map.index
            return class_labels
        except lable in class_labels == "Untitled":
            raise ValueError('Make sure all documents have their class set to\
             the author\'s name')

    def words_graph(self) -> go.Figure:

        result_plot = [
            go.Scattergl(
                x=np.arange(len(row)),
                y=row,
                name=token,
                mode="markers",
                line=dict(color=self._get_scatter_color(index=index)),
                marker=dict(color=self._get_scatter_color(index=index))
            )
            for index, (token, row) in
            enumerate(token_average_data_frame.iterrows())
        ]
        return go.Figure(
            data=result_plot,
            layout=go.Layout(
                dragmode="pan",
                margin=dict(
                    l=75,  # nopep8
                    r=0,
                    b=30,
                    t=0,
                    pad=4
                ),
                paper_bgcolor="rgba(0, 0, 0, 0)",
                plot_bgcolor="rgba(0, 0, 0, 0)",
                font=dict(
                    color=self._options.text_color,
                    size=16
                ),
                xaxis=dict(
                    zeroline=False,
                    showgrid=False,
                    tickcolor=self._options.text_color
                ),
                yaxis=dict(
                    zeroline=False,
                    showgrid=False,
                    tickcolor=self._options.text_color
                ),
                legend=dict(
                    x=1.01,
                    y=0
                )
            )
        )
    def _fit_model(self):
        """Fits an SVM model for the specified author.

        Args:
        data: DTM word counts of the function words in each doc.
        margin_softener: The value of the C constant.
        kernel: The kernel type of the model.
        gamma: The value of gamma.
        
        Returns:
        predictions: a list of the prediction results.

        Notes:
        C = .01 was found to be the best margin softener.
        This took a lot of testing with a grid SVC.
        It is possible that a different C is better.
        If someone wants to see if that's true go ahead.
        I'm choosing to leave it as is.

        RBF kernel is essentially required for the one class svm.
        This is because we are in essence creating a pen around the points.
        For more reading on One Class SVMs,
        https://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html
        To see what their decision boundary looks like and why RBF is needed,
        https://scikit-learn.org/stable/_images/sphx_glr_plot_oneclass_001.png

        gamma = 10 was also found through grid testing.
        Note that when changing the value of gamma the value of nu is related. 
        I have chose to stay with the default nu = 0.5.
        I am not fully informed on what the value of nu does however,
        and so it is likely that a different value would serve better. 
        Keep in mind as I've said that if nu is changed,
        then the gamma value will have to be checked to see if it is still best.

        For more reading on SVM classifiers and how to select settings,
        https://scikit-learn.org/stable/modules/svm.html

        To understand the data that is being used, eg. function words
        sets for the different documents, see the comment in helpers/languages.py
        :TODO: add graphing 
        """
        # For testing the model we are using data
        # from the books Dracula by Bram Stoker,
        # The Adventures of Huckleberry Finn by Mark Twain
        # and Pride and Prejudice by Jane Austen
        options = self._classifier_option
        test_data = self._test_data
        self.auth_data = self._doc_term_matrix
        self.model = svm.OneClassSVM(C= options.margin_softener, 
            kernel= "rbf", 
            gamma= options.gamma)
        self.model.fit(train_data)
        predictions = self.model.predict(test_data)
        return jsonify({
            "graph": plot(self.words_graph(),
                          filename="show-legend",
                          show_link=False,
                          output_type="div",
                          include_plotlyjs=False,
                          config=config),

            "predictions":  predictions
        })

    def _predict_model(self):

        """Call the right method based on user selection

        :return: a list of predictions for the author data.

        :TODO: add graphing.
        """
        data = self._doc_term_matrix
        model = self.model
        predictions = self.model.predict(data)

        """
        need to make two functions not one as here
        fit_model which makes the graph and the model
        predict_model which make the graph, the predictions and sets the class of the doc to the author's name if it returns true
        for predicting we should still split the doc up to get cross validity
        get the data to predict and split up 
        use the model to predict it
        give the prediction to the more populated side of true false
        eg. 6/10 are -1 then we are 60% confident that it is not the right author
        make the graph of the predicted documents data points and the data it was fit on to compare


        for fitting
        get the data from the Author
        fit the model on it 
        create a graph of the data vs these data points
        predict these data points to show to the user that it works
        save the data of the docs used to predict and the model

        need warning for <500 words and should not accept less than 250(for now these are guesses)
        
        """
            