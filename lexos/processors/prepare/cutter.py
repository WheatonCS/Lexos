import re
from typing import List

from lexos.helpers.error_messages import SEG_NON_POSITIVE_MESSAGE, \
    NEG_OVERLAP_LAST_PROP_MESSAGE, LARGER_SEG_SIZE_MESSAGE, \
    EMPTY_MILESTONE_MESSAGE, INVALID_CUTTING_TYPE_MESSAGE


def cut_list_with_overlap(input_list: list, norm_seg_size: int, overlap: int,
                          last_prop: float) -> List[list]:
    """Cut the split list of text into list that contains sub-lists.

    This function takes care of both overlap and last proportion with the input
    list and the segment size. The function calculates the number of segment
    with the overlap value and then use it as indexing to capture all the
    sub-lists with the get_single_seg helper function.
    :param last_prop: the last segment size / other segment size.
    :param input_list: the segment list that split the contents of the file.
    :param norm_seg_size: the size of the segment.
    :param overlap: the min proportional size that the last segment has to be.
    :return a list of list(segment) that the text has been cut into, which has
    not go through the last proportion size calculation.
    """

    # get the distance between starts of each two adjacent segments
    seg_start_distance = norm_seg_size - overlap

    # the length of the list excluding the last segment
    length_exclude_last = len(input_list) - norm_seg_size * last_prop

    # the total number of segments after cut
    # the `+ 1` is to add back the last segments
    num_segment = \
        int(length_exclude_last / seg_start_distance) + 1

    # need at least one segment
    if num_segment < 1:
        num_segment = 1

    def get_single_seg(index: int, is_last_prop: bool) -> list:
        """Helper to get one single segment with index.

        This function first evaluate whether the segment is the last one and
        grab different segment according to the result, and returns sub-lists
        while index is in the range of number of segment.
        :param is_last_prop: the bool value that determine whether the segment
        is the last one.
        :param index: the index of the segment in the final segment list.
        :return single segment in the input_list based on index.
        """

        # define current segment size based on whether it is the last segment
        if is_last_prop:
            return input_list[seg_start_distance * index:]
        else:
            return input_list[seg_start_distance * index:
                              seg_start_distance * index + norm_seg_size]

    # return the whole list of segment while evaluating whether is last segment
    return [get_single_seg(
            index=index,
            is_last_prop=True if index == num_segment - 1 else False
            ) for index in range(num_segment)]


def join_sublist_element(input_list: List[List[str]]) -> List[str]:
    """Join each sublist of chars into string.

    This function joins all the element(chars) in each sub-lists together, and
    turns every sub-lists to one element in the overall list.
    The sublist will turned into a string with all the same elements as before.
    :param input_list: the returned list after cut
    :return: the list that contains all the segments as strings.
    """

    return ["".join(chars) for chars in input_list]


def cut_by_characters(text: str, seg_size: int, overlap: int,
                      last_prop: float) -> List[str]:
    """Cut the input text into segments by number of chars in each segment.

    Where the segment size is measured by counts of characters, with an option
    for an amount of overlap between segments and a minimum proportion
    threshold for the last segment.
    :param text: the string with the contents of the file.
    :param seg_size: the segment size, in characters.
    :param overlap: the number of characters to overlap between segments.
    :param last_prop: the last segment size / other segment size.
    :return: a list of list(segment) that the text has been cut into.
    """

    # pre-condition assertion
    assert seg_size > 0, SEG_NON_POSITIVE_MESSAGE
    assert overlap >= 0 and last_prop >= 0, NEG_OVERLAP_LAST_PROP_MESSAGE
    assert seg_size > overlap, LARGER_SEG_SIZE_MESSAGE

    # chop up the string by characters (keeping whitespace)
    seg_list = [char for char in text]

    # add sub-lists(segment) to final list
    final_seg_list = cut_list_with_overlap(input_list=seg_list,
                                           norm_seg_size=seg_size,
                                           overlap=overlap,
                                           last_prop=last_prop)

    # join characters in each sublist
    final_seg_list = join_sublist_element(input_list=final_seg_list)

    return final_seg_list


def cut_by_words(text: str, seg_size: int, overlap: int,
                 last_prop: float) -> List[str]:
    """Cut the input text into segments by number of words in each segment.

    Cuts the text into equally sized segments, where the segment size is
    measured by counts of words, with an option for an amount of overlap
    between segments and a minimum proportion threshold for the last segment.
    :param text: the string with the contents of the file.
    :param seg_size: the segment size, in words.
    :param overlap: the number of words to overlap between segments.
    :param last_prop: the last segment size / other segment size.
    :return: a list of list(segment) that the text has been cut into.
    """

    # pre-condition assertion
    assert seg_size > 0, SEG_NON_POSITIVE_MESSAGE
    assert overlap >= 0 and last_prop >= 0, NEG_OVERLAP_LAST_PROP_MESSAGE
    assert seg_size > overlap, LARGER_SEG_SIZE_MESSAGE

    # split text by words while keeping all the whitespace
    seg_list = re.findall(r"\S+\s*", text)

    # add sub-lists(segment) to final list
    final_seg_list = cut_list_with_overlap(input_list=seg_list,
                                           norm_seg_size=seg_size,
                                           overlap=overlap,
                                           last_prop=last_prop)

    # join words in each sublist
    final_seg_list = join_sublist_element(input_list=final_seg_list)

    return final_seg_list


def cut_by_lines(text: str, seg_size: int, overlap: int,
                 last_prop: float) -> List[str]:
    """Cut the input text into segments by number of lines in each segment.

    The size of the segment is measured by counts of lines, with an option for
    an amount of overlap between segments and a minimum proportion threshold
    for the last segment.
    :param text: the string with the contents of the file.
    :param seg_size: the segment size, in lines.
    :param overlap: the number of lines to overlap between segments.
    :param last_prop: the last segment size / other segment size.
    :return: a list of list(segment) that the text has been cut into.
    """

    # pre-condition assertion
    assert seg_size > 0, SEG_NON_POSITIVE_MESSAGE
    assert overlap >= 0 and last_prop >= 0, NEG_OVERLAP_LAST_PROP_MESSAGE
    assert seg_size > overlap, LARGER_SEG_SIZE_MESSAGE

    # split text by new line while keeping all the whitespace
    seg_list = text.splitlines(keepends=True)

    # add sub-lists(segment) to final list
    final_seg_list = cut_list_with_overlap(input_list=seg_list,
                                           norm_seg_size=seg_size,
                                           overlap=overlap,
                                           last_prop=last_prop)

    # join lines in each sublist
    final_seg_list = join_sublist_element(input_list=final_seg_list)

    # remove empty lines
    final_seg_list = [line for line in final_seg_list if line.strip()]

    return final_seg_list


def cut_by_number(text: str, num_segment: int) -> List[str]:
    """Cut the text by the input number of segment (equally sized).

    The chunks created will be equal in terms of word count, or line count if
    the text does not have words separated by whitespace (see Chinese).
    :param text: the string with the contents of the file.
    :param num_segment: number of segments to cut the text into.
    :return a list of list(segment) that the text has been cut into.
    """

    # pre-condition assertion
    assert num_segment > 0, SEG_NON_POSITIVE_MESSAGE

    # split text by words while stripping all the whitespace
    words_list = re.findall(r"\S+\s*", text)
    total_num_words = len(words_list)

    # the length of normal chunk
    norm_seg_size = int(total_num_words / num_segment)

    # long segment will have one more words in them than norm_seg_size
    num_long_seg = total_num_words % num_segment
    long_seg_size = norm_seg_size + 1

    def get_single_seg(index: int) -> List[str]:
        """Helper to get one single segment with index.

        This function first evaluate whether the segment is the last one and
        grab different segment according to the result, and returns sub-lists
        while index is in the range of number of segment.
        :param index: the index of the segment in the final segment list.
        :return single segment in the input_list based on index.
        """

        if index < num_long_seg:

            return words_list[long_seg_size * index:
                              long_seg_size * index + long_seg_size]
        else:

            num_norm_seg_in_front = index - num_long_seg

            start = long_seg_size * num_long_seg + \
                norm_seg_size * num_norm_seg_in_front

            return words_list[start: start + norm_seg_size]

    seg_list = [get_single_seg(index) for index in range(num_segment)]

    # join words in each sublist
    final_seg_list = join_sublist_element(input_list=seg_list)

    return final_seg_list


def cut_by_milestone(text: str, milestone: str) -> List[str]:
    """Cuts the file by milestones.

    :param text: the string with the contents of the file.
    :param milestone: the milestone word that to cut the text by.
    :return: a list of segment that the text has been cut into.
    """

    # pre-condition assertion
    assert len(milestone) > 0, EMPTY_MILESTONE_MESSAGE

    # split text by milestone string
    final_seg_list = text.split(sep=milestone)

    return final_seg_list


def cut(text: str, cutting_value: str, cutting_type: str, overlap: str,
        last_prop_percent: str) -> List[str]:
    """Cuts each text string into various segments.

    Cutting according to the options chosen by the user.
    :param text: A string with the text to be split.
    :param cutting_value: The value by which to cut the texts by.
    :param cutting_type: A string representing which cutting method to use.
    :param overlap: A unicode string representing the number of words to be
           overlapped between each text segment.
    :param last_prop_percent: A unicode string representing the minimum
           proportion percentage the last segment has to be to not get
           assimilated by the previous.
    :return A list of strings, each representing a segment of the original.
    """

    # pre-condition assertion
    assert cutting_type == "Milestones" or cutting_type == "Characters" or \
        cutting_type == "Tokens" or cutting_type == "Lines" or \
        cutting_type == "Segments", INVALID_CUTTING_TYPE_MESSAGE

    # standardize parameters
    cutting_type = str(cutting_type)
    overlap = int(overlap)
    last_prop_percent = float(last_prop_percent.rstrip('%')) / 100

    # distribute cutting method by input cutting value
    if cutting_type != 'Milestones':
        cutting_value = int(cutting_value)

    if cutting_type == 'Characters':
        string_list = cut_by_characters(text=text, seg_size=cutting_value,
                                        overlap=overlap,
                                        last_prop=last_prop_percent)
    elif cutting_type == 'Tokens':
        string_list = cut_by_words(text=text, seg_size=cutting_value,
                                   overlap=overlap,
                                   last_prop=last_prop_percent)
    elif cutting_type == 'Lines':
        string_list = cut_by_lines(text=text, seg_size=cutting_value,
                                   overlap=overlap,
                                   last_prop=last_prop_percent)
    elif cutting_type == 'Milestones':
        string_list = cut_by_milestone(text=text, milestone=cutting_value)
    elif cutting_type == 'Segments':
        string_list = cut_by_number(text=text, num_segment=cutting_value)

    # noinspection PyUnboundLocalVariable
    return string_list
