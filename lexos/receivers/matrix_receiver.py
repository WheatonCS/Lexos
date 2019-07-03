"""This is the receiver for the matrix model."""

from typing import NamedTuple, Optional, Dict

from lexos.receivers.base_receiver import BaseReceiver

DocumentLabelMap = Dict[int, str]


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


class MatrixReceiver(BaseReceiver):
    """This class receives the front end options."""

    def __init__(self):
        """Get all the matrix options using the receiver."""
        super().__init__()

    def _get_token_option_from_front_end(self) -> TokenOption:
        """Get the token option from front end.

        :return: a token option struct
        """
        token_type_is_word = self._front_end_data['token_type'] == 'Tokens'
        token_type_is_char = self._front_end_data['token_type'] == 'Characters'
        char_within_word = False

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
        n_gram_size = int(self._front_end_data['token_size'])

        return TokenOption(token_type=token_type, n_gram_size=n_gram_size)

    def _get_normalize_option_from_front_end(self) -> NormOption:
        """Get the normalize option from front end.

        :return: a normalize option struct
        """
        use_freq = self._front_end_data['normalization_method'] == \
            'Proportional'

        # if use TF/IDF
        use_tfidf = self._front_end_data['normalization_method'] == 'TF-IDF'

        return NormOption(use_freq=use_freq, use_tf_idf=use_tfidf,
                          tf_idf_norm_option='l2')

    def _get_culling_option_from_front_end(self) -> CullingOption:
        """Get the culling option from the front end.

        :return: a culling option struct
        """
        if 'enable_most_frequent_words' in self._front_end_data:
            lower_rank_bound = int(self._front_end_data['most_frequent_words'])
        else:
            lower_rank_bound = None

        if 'enable_minimum_occurrences' in self._front_end_data:
            least_num_seg = int(self._front_end_data['minimum_occurrences'])
        else:
            least_num_seg = None

        return CullingOption(cull_least_seg=least_num_seg,
                             mfw_lowest_rank=lower_rank_bound)

    def options_from_front_end(self) -> MatrixFrontEndOption:
        """Get all the matrix options from front end.

        :return: all the options packed together into a matrix option class
        """
        return MatrixFrontEndOption(
            token_option=self._get_token_option_from_front_end(),
            norm_option=self._get_normalize_option_from_front_end(),
            culling_option=self._get_culling_option_from_front_end()
        )
