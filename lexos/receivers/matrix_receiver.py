from typing import NamedTuple, Optional

import numpy as np

from lexos.receivers.base_receiver import BaseReceiver


class TokenOption(NamedTuple):
    """A struct to represent token option."""
    # the size of each token
    n_gram_size: int

    # the token type to send to CountVerctorizer
    # available options are 'word', 'char_wb', and 'char'
    token_type: str


class NormOption(NamedTuple):
    """A struct to keep the normalize option."""
    # True if we are using proportional count, False if we are using raw count
    use_freq: bool

    # True if we are using proportional count, False if we are using raw count
    use_tf_idf: bool

    # the normalize option in TF-IDF
    # available options are 'l1' and 'l2'. nice naming, SciPy!
    tf_idf_norm_option: str


class CullingOption(NamedTuple):
    """A struct to represent all the culling option."""
    # Whether to apply most frequent word
    most_frequent_word: bool

    # the lowest word rank to keep in DTM
    mfw_lowest_rank: Optional[int]

    # Whether to apply culling option
    culling: bool

    # the least number of passage that the word needs to be in
    cull_least_seg: Optional[int]


class MatrixOption(NamedTuple):
    """A struct to represent all the matrix option."""
    # the token options
    token_option: TokenOption

    # the normalize options
    norm_option: NormOption

    # the culling options
    culling_option: CullingOption

    # all the temp labels of segments
    temp_labels: np.ndarray


class MatrixReceiver(BaseReceiver):

    def __init__(self):
        """The receiver to the all the matrix option"""
        super().__init__()

    def _get_token_option_from_front_end(self) -> TokenOption:
        """get the token option from front end

        :return: a token option struct
        """
        token_type_is_word = self._front_end_data['tokenType'] == 'word'
        token_type_is_char = self._front_end_data['tokenType'] == 'char'
        char_within_word = 'inWordsOnly' in self._front_end_data

        # get the token type
        if token_type_is_word:
            token_type = 'word'
        elif token_type_is_char and char_within_word:
            token_type = 'char_wb'
        elif token_type_is_char and not char_within_word:
            token_type = 'char'
        else:
            raise ValueError('invalid token type from front end')

        # get the n_gram_size
        n_gram_size = int(self._front_end_data['tokenSize'])

        return TokenOption(token_type=token_type, n_gram_size=n_gram_size)

    def _get_normalize_option_from_front_end(self) -> NormOption:
        """Get the normalize option from front end.

        :return: a normalize option struct
        """
        use_freq = self._front_end_data['normalizeType'] == 'freq'

        # if use TF/IDF
        use_tfidf = self._front_end_data['normalizeType'] == 'tfidf'

        # only applicable when using "TF/IDF", set default value to N/A
        if self._front_end_data['norm'] == 'l1':
            norm_option = 'l1'
        elif self._front_end_data['norm'] == 'l2':
            norm_option = 'l2'
        else:
            norm_option = None

        return NormOption(use_freq=use_freq, use_tf_idf=use_tfidf,
                          tf_idf_norm_option=norm_option)

    def _get_culling_option_from_front_end(self) -> CullingOption:
        """Get the culling option from the front end

        :return: a culling option struct
        """
        if 'mfwcheckbox' in self._front_end_data:
            most_frequent_word = True
            lower_rank_bound = int(self._front_end_data['mfwnumber'])
        else:
            most_frequent_word = False
            lower_rank_bound = None

        if 'cullcheckbox' in self._front_end_data:
            culling = True
            least_num_seg = int(self._front_end_data['cullnumber'])
        else:
            culling = False
            least_num_seg = None

        return CullingOption(culling=culling, cull_least_seg=least_num_seg,
                             most_frequent_word=most_frequent_word,
                             mfw_lowest_rank=lower_rank_bound)

    def _get_temp_labels_from_front_end(self) -> np.array:
        """Get all the temp labels from front end

        :return: get all the temp labels from the web
        """
        label_keys = [key for key in self._front_end_data.keys()
                      if key.startswith('file_')]

        return np.array([self._front_end_data[key] for key in label_keys])

    def options_from_front_end(self) -> MatrixOption:
        """Get all the matrix option from front end.

        :return: all the option packed together into a matrix option class
        """
        return MatrixOption(
            token_option=self._get_token_option_from_front_end(),
            norm_option=self._get_normalize_option_from_front_end(),
            culling_option=self._get_culling_option_from_front_end(),
            temp_labels=self._get_temp_labels_from_front_end()
        )
