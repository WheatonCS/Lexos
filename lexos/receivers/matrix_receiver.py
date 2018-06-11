"""This is the receiver for the matrix model."""

import re
from typing import NamedTuple, Optional, Dict

from lexos.receivers.base_receiver import BaseReceiver

IdTempLabelMap = Dict[int, str]


class TokenOption(NamedTuple):
    """A typed tuple to represent token option."""

    # the size of each token
    n_gram_size: int

    # the token type to send to CountVerctorizer
    # available options are 'word', 'char_wb', and 'char'
    token_type: str


class NormOption(NamedTuple):
    """A typed tuple to keep the normalize option."""

    # True if we are using proportional count, False if we are using raw count
    use_freq: bool

    # True if we are using proportional count, False if we are using raw count
    use_tf_idf: bool

    # the normalize option in TF-IDF
    # available options are 'l1' and 'l2'. nice naming, SciPy!
    tf_idf_norm_option: str


class CullingOption(NamedTuple):
    """A typed tuple to represent all the culling options."""

    # the lowest word rank to keep in DTM
    # if none, then don't apply most frequent word
    mfw_lowest_rank: Optional[int]

    # the least number of passage that the word needs to be in
    # if none, then don't apply culling
    cull_least_seg: Optional[int]


class MatrixFrontEndOption(NamedTuple):
    """A typed tuple to represent all the matrix options."""

    # the token options
    token_option: TokenOption

    # the normalize options
    norm_option: NormOption

    # the culling options
    culling_option: CullingOption

    # all the temp labels of segments
    id_temp_label_map: IdTempLabelMap


class MatrixReceiver(BaseReceiver):
    """This class receives the front end options."""

    def __init__(self):
        """Get all the matrix options using the receiver."""
        super().__init__()

    def _get_token_option_from_front_end(self) -> TokenOption:
        """Get the token option from front end.

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
        """Get the culling option from the front end.

        :return: a culling option struct
        """
        if 'mfwcheckbox' in self._front_end_data:
            lower_rank_bound = int(self._front_end_data['mfwnumber'])
        else:
            lower_rank_bound = None

        if 'cullcheckbox' in self._front_end_data:
            least_num_seg = int(self._front_end_data['cullnumber'])
        else:
            least_num_seg = None

        return CullingOption(cull_least_seg=least_num_seg,
                             mfw_lowest_rank=lower_rank_bound)

    def _get_id_temp_label_map_from_front_end(self) -> Dict[int, str]:
        """Get all the file id maps to temp labels from front end.

        :return: a dict maps id to temp labels
        """
        label_key_regex = re.compile(r"file_(\d+)")

        def parse_temp_label_data(label_key: str) -> (int, str):
            """Parse the key of the temp label into a tuple.

            Get the id from the label key and find the label corresponding to
            the label key, then return a tuple of id and the label.
            :param label_key: key of the label in _front_end_data
            :return: a tuple where the first element is the file id
                     and the second element is the temp label
            """
            # extract the file id
            match_obj = label_key_regex.match(label_key)
            file_id = int(match_obj.group(1))

            # find the label
            label = self._front_end_data[label_key]

            return file_id, label

        # a list of tuple where
        # the first element is the key, the second element is the value
        id_temp_label_list = [parse_temp_label_data(key)
                              for key in self._front_end_data.keys()
                              if label_key_regex.match(key)]

        return dict(id_temp_label_list)

    def options_from_front_end(self) -> MatrixFrontEndOption:
        """Get all the matrix options from front end.

        :return: all the options packed together into a matrix option class
        """
        return MatrixFrontEndOption(
            token_option=self._get_token_option_from_front_end(),
            norm_option=self._get_normalize_option_from_front_end(),
            culling_option=self._get_culling_option_from_front_end(),
            id_temp_label_map=self._get_id_temp_label_map_from_front_end()
        )
