import re
from typing import Dict

from lexos.receivers.base_receiver import BaseReceiver


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
                 culling_option: CullingOption,
                 id_temp_label_map: Dict[int, str]):
        """A struct to represent all the matrix option.

        :param token_option: the token options
        :param norm_option: the normalize options
        :param culling_option: the culling options
        :param id_temp_label_map: all the temp labels in an np array
        """
        self._token_option = token_option
        self._norm_option = norm_option
        self._culling_option = culling_option
        self._temp_label = id_temp_label_map

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
    def id_temp_label_map(self) -> Dict[int, str]:
        """All the temp labels

        :return: an np array with all the labels
        """
        return self._temp_label


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
            lower_rank_bound = self._front_end_data['mfwnumber']
        else:
            most_frequent_word = False
            lower_rank_bound = None

        if 'cullcheckbox' in self._front_end_data:
            culling = True
            least_num_seg = self._front_end_data['cullnumber']
        else:
            culling = False
            least_num_seg = None

        return CullingOption(culling=culling, cull_least_seg=least_num_seg,
                             most_frequent_word=most_frequent_word,
                             mfw_lowest_rank=lower_rank_bound)

    def _get_id_temp_label_map_from_front_end(self) -> Dict[int, str]:
        """Get all the file id maps to temp labels from front end

        :return: a dict maps id to temp labels
        """
        label_key_regex = re.compile(r"file_(\d+)")

        def parse_temp_label_data(label_key: str) -> (int, str):
            """parse the key of the temp label into a tuple

            get the id from the label key and find the label correspond to
            the label key.
            then return a tuple of id and the label
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

    def options_from_front_end(self) -> MatrixOption:
        """Get all the matrix option from front end.

        :return: all the option packed together into a matrix option class
        """
        return MatrixOption(
            token_option=self._get_token_option_from_front_end(),
            norm_option=self._get_normalize_option_from_front_end(),
            culling_option=self._get_culling_option_from_front_end(),
            id_temp_label_map=self._get_id_temp_label_map_from_front_end()
        )
