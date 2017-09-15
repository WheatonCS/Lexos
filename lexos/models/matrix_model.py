import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from lexos.helpers import definitions
from lexos.managers.file_manager import FileManager
from lexos.models.base_model import BaseModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.receivers.matrix_receiver import MatrixOption, MatrixReceiver


class MatrixModel(BaseModel):

    def __init__(self, test_matrix_option: MatrixOption = None,
                 test_file_manager: FileManager = None):
        """Class to generate and manipulate dtm.

        :param test_file_manager: (fake parameter)
                                the file manger used for testing
        :param test_matrix_option: (fake parameter)
                                the matrix options used for testing
        """
        super().__init__()
        file_manager_model = FileManagerModel()
        matrix_receiver = MatrixReceiver()

        # the result form higher level class
        self._file_manager = test_file_manager if test_file_manager \
            else file_manager_model.load_file_manager()

        # the front end option from receiver
        self._opts = test_matrix_option if test_matrix_option \
            else matrix_receiver.options_from_front_end()

    def get_matrix(self)-> pd.DataFrame:
        """Get the document term matrix (DTM) of all the active files

        :return:
            a panda data frame with:
            - the index (row) header are the segment names (temp_labels)
            - the column header are words
        """

        all_contents = self._file_manager.get_content_of_active()

        # heavy hitting tokenization and counting options set here

        # CountVectorizer can do
        #       (a) preprocessing
        #           (but we don't need that);
        #       (b) tokenization:
        #               analyzer=['word', 'char', or 'char_wb';
        #               Note: char_wb does not span across two words,
        #                   but will include whitespace at start/end of ngrams)
        #                   not an option in UI]
        #               token_pattern (only for analyzer='word'):
        #               cheng magic regex:
        #                   words include only NON-space characters
        #               ngram_range
        #                   (presuming this works for both word and char??)
        #       (c) culling:
        #           min_df..max_df
        #           (keep if term occurs in at least these documents)
        #       (d) stop_words handled in scrubber
        #       (e) lowercase=False (we want to leave the case as it is)
        #       (f) dtype=float
        #           sets type of resulting matrix of values;
        #           need float in case we use proportions

        # for example:
        # word 1-grams
        #   ['content' means use strings of text,
        #   analyzer='word' means features are "words";
        # min_df=1 means include word if it appears in at least one doc, the
        # default;

        # [\S]+  :
        #   means tokenize on a word boundary where boundary are \s
        #   (spaces, tabs, newlines)

        count_vector = CountVectorizer(
            input='content', encoding='utf-8', min_df=1,
            analyzer=self._opts.token_option.token_type,
            token_pattern=definitions.WORD_REGEX, lowercase=False,
            ngram_range=(self._opts.token_option.token_type,
                         self._opts.token_option.token_type),
            stop_words=[], dtype=float, max_df=1.0
        )

        # make a (sparse) Document-Term-Matrix (DTM) to hold all counts
        doc_term_sparse_matrix = count_vector.fit_transform(all_contents)

        # ==== Parameters TfidfTransformer (TF/IDF) ===

        # Note: by default, idf use natural log
        #
        # (a) norm: 'l1', 'l2' or None, optional
        #     {USED AS THE LAST STEP: after getting the result of tf*idf,
        #       normalize the vector (row-wise) into unit vector}
        #     l1': Taxicab / Manhattan distance (p=1)
        #          [ ||u|| = |u1| + |u2| + |u3| ... ]
        #     l2': Euclidean norm (p=2), the most common norm;
        #           typically called "magnitude"
        #           [ ||u|| = sqrt( (u1)^2 + (u2)^2 + (u3)^2 + ... )]
        #     *** user can choose the normalization method ***
        #
        # (b) use_idf:
        #       boolean, optional ;
        #       "Enable inverse-document-frequency reweighting."
        #           which means: True if you want to use idf (times idf)
        #       False if you don't want to use idf at all,
        #           the result is only term-frequency
        #       *** we choose True here because the user has already chosen
        #           TF/IDF, instead of raw counts ***
        #
        # (c) smooth_idf:
        #       boolean, optional;
        #       "Smooth idf weights by adding one to document frequencies,
        #           as if an extra
        #       document was seen containing every term in the collection
        #            exactly once. Prevents zero divisions.""
        #       if True,
        #           idf = log(number of doc in total /
        #                       number of doc where term t appears) + 1
        #       if False,
        #           idf = log(number of doc in total + 1 /
        #                       number of doc where term t appears + 1 ) + 1
        #       *** we choose False, because denominator never equals 0
        #           in our case, no need to prevent zero divisions ***
        #
        # (d) sublinear_tf:
        #       boolean, optional ; "Apply sublinear tf scaling"
        #       if True,  tf = 1 + log(tf) (log here is base 10)
        #       if False, tf = term-frequency
        #       *** we choose False as the normal term-frequency ***

        if self._opts.norm_option.use_tf_idf:  # if use TF/IDF
            transformer = TfidfTransformer(
                norm=self._opts.norm_option.tf_idf_norm_option,
                use_idf=True,
                smooth_idf=False,
                sublinear_tf=False)
            doc_term_sparse_matrix = transformer.fit_transform(
                doc_term_sparse_matrix)

        # need to get at the entire matrix and not sparse matrix
        raw_count_matrix = doc_term_sparse_matrix.toarray()
        # snag all features (e.g., word-grams or char-grams) that were counted
        words = count_vector.get_feature_names()
        # pack the data into a data frame
        dtm_data_frame = pd.DataFrame(data=raw_count_matrix,
                                      index=self._opts.temp_labels,
                                      columns=words)

        # change the dtm to proportion
        if self._opts.norm_option.use_freq:
            # apply the proportion function to each row
            dtm_data_frame = dtm_data_frame.apply(lambda row: row / row.sum(),
                                                  axis=1)

        # apply culling to dtm
        if self._opts.culling_option.culling:

            dtm_data_frame = self._get_culled_matrix(
                least_num_seg=self._opts.culling_option.cull_least_passage,
                dtm_data_frame=dtm_data_frame
            )

        # only leaves the most frequent words in dtm
        if self._opts.culling_option.most_frequent_word:

            dtm_data_frame = self._get_most_frequent_word(
                lower_rank_bound=self._opts.culling_option.mfw_lowest_rank,
                dtm_data_frame=dtm_data_frame,
                count_matrix=raw_count_matrix
            )

        return dtm_data_frame

    @staticmethod
    def _get_most_frequent_word(lower_rank_bound: int,
                                count_matrix: np.ndarray,
                                dtm_data_frame: pd.DataFrame) -> pd.DataFrame:
        """ Gets the most frequent words in final_matrix and words.

        The new count matrix will consists of only the most frequent words in
        the whole corpus.
        :param lower_rank_bound: the lowest rank to remain in the matrix
                                 (the rank is determined by the word's number
                                 of appearance in the whole corpus)
                                 (ranked from high to low)
        :param count_matrix: the raw count matrix,
                                the row are for each segments
                                the column are for each words
        :param dtm_data_frame: the dtm in the form of panda data frame.
                                the indices(rows) are segment names
                                the columns are words.
        :return:
            dtm data frame with only the most frequent words
        """

        # get the word counts for corpus (1D array)
        corpus_word_count_list = count_matrix.sum(axis=0)

        # get the index to sort those words
        sort_index_array = corpus_word_count_list.argsort()

        # get the total number of unique words
        total_num_words = corpus_word_count_list.size

        # strip the index to leave the most frequent ones
        # those are the index of the most frequent words
        most_frequent_index = sort_index_array[
            total_num_words - lower_rank_bound, lower_rank_bound]

        # use the most frequent index to get out most frequent words
        # this feature is called index array:
        # https://docs.scipy.org/doc/numpy/user/basics.indexing.html
        dtm_data_frame = dtm_data_frame.iloc[most_frequent_index]

        return dtm_data_frame

    @staticmethod
    def _get_culled_matrix(least_num_seg: int,
                           dtm_data_frame: pd.DataFrame) -> pd.DataFrame:
        """Gets the culled final_matrix and culled words.

        Gives a matrix that only contains the words that appears in more than
        `least_num_seg` segments.
        :param least_num_seg: least number of segment the word needs to appear
                                in to be kept.
        :param dtm_data_frame: the dtm in forms of panda data frames.
                                the indices(rows) are segment names
                                the columns are words.
        :return:
             the culled dtm data frame
        """

        # create a bool matrix to indicate whether a word is in a segment
        # at the line of segment s and the column of word w,
        # if the value is True, then means w is in s
        # otherwise means w is not in s
        is_in_data_frame = dtm_data_frame.astype(bool)

        # summing the boolean array gives an int, which indicates how many
        # True there are in that array.
        # this is an series, indicating each word is in how many segments
        # this array is a parallel array of words
        # noinspection PyUnresolvedReferences
        words_in_num_seg_series = is_in_data_frame.sum(axis=0)

        # get the index of all the words needs to remain
        # this is an array of int
        dtm_data_frame = dtm_data_frame.loc[
            words_in_num_seg_series >= least_num_seg
            ]

        return dtm_data_frame
