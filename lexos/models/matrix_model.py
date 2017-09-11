from typing import List

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from lexos.models.filemanager_model import FileManagerModel


class TokenOption:
    def __init__(self, n_gram_size: int, token_type: str):
        """A struct to represent token option.

        :param n_gram_size: the size of each token
        :param token_type: the token type to send into CountVectorizer
        """
        self._n_gram_size = n_gram_size
        self._token_type = token_type

    @property
    def n_gram_size(self) -> int:
        """The size of each token.

        the number of words or char in each token
        :return: an int to indicate above information
        """
        return self._n_gram_size

    @property
    def token_type(self) -> str:
        """The type of the token.

        The token type to be send into CountVectorizer.
        Available options are 'word', 'char', 'char_wb'.
        :return: a string to indicate above information.
        """
        return self._token_type


class NormOption:
    def __init__(self, use_freq: bool, use_tf_idf: bool,
                 tf_idf_norm_option: str):
        """A struct to keep the normalize option.

        :param use_freq: True if we are using proportional count
                         False if we are using raw count
        :param use_tf_idf: whether to apply TF-IDF transformation
        :param tf_idf_norm_option: the normalize option in TF-IDF
        """
        self._use_freq = use_freq
        self._use_tf_idf = use_tf_idf
        self._tf_idf_norm_option = tf_idf_norm_option

    @property
    def use_freq(self) -> bool:
        """Whether to use proportional count in our doc term matrix.

        :return: True if we are using proportional count
                 False if we are using raw count
        """
        return self._use_freq

    @property
    def use_tf_idf(self) -> bool:
        """Whether to apply TF-IDF transformation to the matrix

        :return: a boolean to indicate above information
        """
        return self._use_tf_idf

    @property
    def tf_idf_norm_option(self) -> str:
        """The normalize option for TF-IDF transformation

        :return: a string to indicate above information
        """
        return self._tf_idf_norm_option


class CullingOption:
    def __init__(self, most_frequent_word: bool, mfw_lowest_rank: int,
                 culling: bool, cull_least_seg: int):
        """A struct to represent all the culling option

        :param most_frequent_word: Whether to apply most frequent word
        :param mfw_lowest_rank: the lowest word rank to keep in passage
        :param culling: whether to apply culling option
        :param cull_least_seg: the least number of passage that the word
            needs to be in.
        """
        self._mfw = most_frequent_word
        self._mfw_lower = mfw_lowest_rank
        self._culling = culling
        self._cull_lower = cull_least_seg

    @property
    def most_frequent_word(self) -> bool:
        """Whether to apply most frequent word

        :return: A boolean to indicate the above information
        """
        return self._mfw

    @property
    def mfw_lowest_rank(self) -> int:
        """The lowest word rank to keep in passage

        :return: a int to indicate the above information
        """
        return self._mfw_lower

    @property
    def culling(self) -> bool:
        """Whether to apply the culling option

        :return: a boolean to indicate the above information
        """
        return self._culling

    @property
    def cull_least_passage(self) -> int:
        """The least a number of passage the words needs to be in

        :return: a int to indicate the above information
        """
        return self._cull_lower


class MatrixOption:
    def __init__(self, token_option: TokenOption, norm_option: NormOption,
                 culling_option: CullingOption, temp_labels: np.ndarray):
        """A struct to represent all the matrix option.

        :param token_option: the token options
        :param norm_option: the normalize options
        :param culling_option: the culling options
        :param temp_labels: all the temp labels in an np array
        """
        self._token_option = token_option
        self._norm_option = norm_option
        self._culling_option = culling_option
        self._temp_label = temp_labels

    @property
    def token_option(self) -> TokenOption:
        """All the token option

        :return: a TokenOption type
        """
        return self._token_option

    @property
    def norm_option(self) -> NormOption:
        """All the normalize options

        :return: a NormOption Type
        """
        return self._norm_option

    @property
    def culling_option(self) -> CullingOption:
        """All the culling options.

        :return: a CullingOption type
        """
        return self._culling_option

    @property
    def temp_labels(self) -> np.ndarray:
        """All the temp labels

        :return: an np array with all the labels
        """
        return self._temp_label


class MatrixModel(FileManagerModel):

    def __init__(self, matrix_option: MatrixOption = None):
        """Class to generate and manipulate dtm."""
        super().__init__()
        self._active_files = self.file_manager.get_active_files()

        # get the matrix option
        self._opt = matrix_option if matrix_option else \
            self._get_matrix_option_from_front_end()

        self._dtm = self._get_matrix()

    @property
    def doc_term_matrix(self) -> pd.DataFrame:
        """the document term matrix

        :return: a panda data frame:
            - columns headers are words
            - index (row) headers are segment names
        """
        return self._dtm

    def _get_token_option_from_front_end(self) -> TokenOption:
        """get the token option from front end

        :return: a token option struct
        """
        # get the token type
        if self.get_front_end_data('tokenType') == 'word':
            token_type = 'word'
        elif self.get_front_end_data('tokenType') == 'char':
            if self.data_exists_in_requests('inWordsOnly'):
                # onlyCharGramsWithinWords will always be false (since in the
                # GUI we've hidden the 'inWordsOnly' in request.form )
                token_type = 'char_wb'
            else:
                token_type = 'char'
        else:
            raise ValueError('invalid token type from front end')

        # get the n_gram_size
        n_gram_size = int(self.get_front_end_data('tokenSize'))

        return TokenOption(token_type=token_type, n_gram_size=n_gram_size)

    def _get_normalize_option_from_front_end(self) -> NormOption:
        """Get the normalize option from front end.

        :return: a normalize option struct
        """
        use_freq = self.get_front_end_data('normalizeType') == 'freq'

        # if use TF/IDF
        use_tfidf = self.get_front_end_data('normalizeType') == 'tfidf'

        # only applicable when using "TF/IDF", set default value to N/A
        if self.get_front_end_data('norm') == 'l1':
            norm_option = 'l1'
        elif self.get_front_end_data('norm') == 'l2':
            norm_option = 'l2'
        else:
            norm_option = None

        return NormOption(use_freq=use_freq, use_tf_idf=use_tfidf,
                          tf_idf_norm_option=norm_option)

    def _get_culling_option_from_front_end(self) -> CullingOption:
        """Get the culling option from the front end

        :return: a culling option struct
        """
        most_frequent_word = self.data_exists_in_requests('mfwcheckbox')
        culling = self.data_exists_in_requests('cullcheckbox')
        least_num_seg = self.get_front_end_data('cullnumber')
        lower_rank_bound = self.get_front_end_data('mfwnumber')

        return CullingOption(culling=culling, cull_least_seg=least_num_seg,
                             most_frequent_word=most_frequent_word,
                             mfw_lowest_rank=lower_rank_bound)

    def _get_temp_labels_from_front_end(self) -> np.array:
        """Get all the temp labels from front end

        :return: get all the temp labels from the web
        """
        try:
            return np.array([self.get_front_end_data("file_" + str(file.id))
                             for file in self._active_files])
        except KeyError:
            return np.array([file.label for file in self._active_files])

    def _get_matrix_option_from_front_end(self) -> MatrixOption:
        """Get all the matrix option from front end.

        :return: all the option packed together into a matrix option class
        """
        return MatrixOption(
            token_option=self._get_token_option_from_front_end(),
            norm_option=self._get_normalize_option_from_front_end(),
            culling_option=self._get_culling_option_from_front_end(),
            temp_labels=self._get_temp_labels_from_front_end()
        )

    def _get_all_content(self) -> List[str]:
        """Helper method to get_matrix.

        :return: get all the file content from the file_manager
        """
        return [file.load_contents() for file in self._active_files]

    def _get_matrix(self)-> pd.DataFrame:
        """Get the document term matrix (DTM) of all the active files

        :return:
            a panda data frame with:
            - the index (row) header are the segment names (temp_labels)
            - the column header are words
        """

        all_contents = self._get_all_content()

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
            analyzer=self._opt.token_option.token_type,
            token_pattern=r'(?u)[\S]+', lowercase=False,
            ngram_range=(self._opt.token_option.token_type,
                         self._opt.token_option.token_type),
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

        if self._opt.norm_option.use_tf_idf:  # if use TF/IDF
            transformer = TfidfTransformer(
                norm=self._opt.norm_option.tf_idf_norm_option,
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
                                      index=self._opt.temp_labels,
                                      columns=words)

        # change the dtm to proportion
        if self._opt.norm_option.use_freq:
            # apply the proportion function to each row
            dtm_data_frame = dtm_data_frame.apply(lambda row: row / row.sum(),
                                                  axis=1)

        # apply culling to dtm
        if self._opt.culling_option.culling:

            dtm_data_frame = self._get_culled_matrix(
                least_num_seg=self._opt.culling_option.cull_least_passage,
                dtm_data_frame=dtm_data_frame
            )

        # only leaves the most frequent words in dtm
        if self._opt.culling_option.most_frequent_word:

            dtm_data_frame = self._get_most_frequent_word(
                lower_rank_bound=self._opt.culling_option.mfw_lowest_rank,
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
