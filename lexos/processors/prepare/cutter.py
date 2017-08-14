import re
import math
from typing import List

from lexos.helpers.error_messages import NON_POSITIVE_SEGMENT_MESSAGE, \
    NEG_OVERLAP_LAST_PROP_MESSAGE, LARGER_SEG_SIZE_MESSAGE, \
    EMPTY_MILESTONE_MESSAGE, INVALID_CUTTING_TYPE_MESSAGE


def cut_list_with_overlap(input_list: list, norm_seg_size: int, overlap: int,
                          last_prop: float) -> List[list]:
    """Cut the split list of text


    :param last_prop: the last segment size / other segment size.
    :param input_list: the segment list that split the contents of the file.
    :param norm_seg_size: the size of the segment.
    :param overlap: the min proportional size that the last segment has to be.
    :return a list of list(segment) that the text has been cut into, which has
    not go through the last proportion size calculation.
    """

    start_point_distance = norm_seg_size - overlap

    input_list_length = len(input_list)
    num_stop_point = \
        (input_list_length - norm_seg_size * last_prop) / start_point_distance

    if num_stop_point > 0:
        num_segment = int(math.ceil(num_stop_point) + 1)
    else:
        num_segment = 1

    def get_single_seg(index: int, is_last_prop: bool) -> List[list]:
        """Helper to get one single segment with index: index.

        :param is_last_prop:
        :param index: the index of the segment in the final segment list.
        :return single segment in the input_list based on index.
        """
        if is_last_prop:
            cur_seg_size = int(norm_seg_size * last_prop)
        else:
            cur_seg_size = norm_seg_size

        return input_list[start_point_distance * index:
                          start_point_distance * index + cur_seg_size]

    return [get_single_seg(index, True if index == num_segment - 1 else False)
            for index in range(num_segment)]


def join_sublist_element(input_list: list) -> List[str]:
    """Helper to join elements in each sublist into string.

    The sublist will turned into a string with all the same elements as before.
    :param input_list: the returned list after cut
    :return: the list that contains all the segments as strings.
    """

    return ["".join(chars) for chars in input_list]


def cut_by_characters(text: str, seg_size: int, overlap: int,
                      last_prop: float) ->List[str]:
    """Cut the input text into segments by characters.

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
    assert seg_size > 0, NON_POSITIVE_SEGMENT_MESSAGE
    assert overlap >= 0 and last_prop >= 0, NEG_OVERLAP_LAST_PROP_MESSAGE
    assert seg_size > overlap, LARGER_SEG_SIZE_MESSAGE

    # split all the chars while keeping all the whitespace
    seg_list = re.findall("\S", text)

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
    """Cut the input text into segments by words.

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
    assert seg_size > 0, NON_POSITIVE_SEGMENT_MESSAGE
    assert overlap >= 0 and last_prop >= 0, NEG_OVERLAP_LAST_PROP_MESSAGE
    assert seg_size > overlap, LARGER_SEG_SIZE_MESSAGE

    # split text by words while keeping all the whitespace
    seg_list = re.findall("\S+\s*", text)

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
    """Cut the input text into segments by lines.

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
    assert seg_size > 0, NON_POSITIVE_SEGMENT_MESSAGE
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
    assert num_segment > 0, NON_POSITIVE_SEGMENT_MESSAGE

    # split text by words while stripping all the whitespace
    seg_list = re.findall("\S+\s*", text)
    # the length of every chunk
    seg_size = len(seg_list) / (num_segment + 1)
    int_seg_size = int(math.ceil(seg_size))

    # add sub-lists(chunks) to final list
    if seg_size != 0:
        final_seg_list = cut_list_with_overlap(
            input_list=seg_list, norm_seg_size=int_seg_size, overlap=0,
            last_prop=1)
    else:
        final_seg_list = seg_list

    # check for last_prop
    if len(final_seg_list) > num_segment:
        final_seg_list[-2].extend(final_seg_list[-1])
        final_seg_list.pop()

    # join words in each sublist
    final_seg_list = join_sublist_element(input_list=final_seg_list)

    return final_seg_list


def cut_by_milestone(text: str, milestone: str) -> List[str]:
    """Cuts the file by milestones

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
    assert cutting_type == "milestone" or cutting_type == "letters" or \
        cutting_type == "words" or cutting_type == "lines" or \
        cutting_type == "number", INVALID_CUTTING_TYPE_MESSAGE

    # standardize parameters
    cutting_type = str(cutting_type)
    overlap = int(overlap)
    last_prop_percent = float(last_prop_percent.rstrip('%')) / 100

    # distribute cutting method by input cutting value
    if cutting_type != 'milestone':
        cutting_value = int(cutting_value)

    if cutting_type == 'letters':
        string_list = cut_by_characters(text=text, seg_size=cutting_value,
                                        overlap=overlap,
                                        last_prop=last_prop_percent)
    elif cutting_type == 'words':
        string_list = cut_by_words(text=text, seg_size=cutting_value,
                                   overlap=overlap,
                                   last_prop=last_prop_percent)
    elif cutting_type == 'lines':
        string_list = cut_by_lines(text=text, seg_size=cutting_value,
                                   overlap=overlap,
                                   last_prop=last_prop_percent)
    elif cutting_type == 'milestone':
        string_list = cut_by_milestone(text=text, milestone=cutting_value)
    elif cutting_type == 'number':
        string_list = cut_by_number(text=text, num_segment=cutting_value)

    # noinspection PyUnboundLocalVariable
    return string_list
