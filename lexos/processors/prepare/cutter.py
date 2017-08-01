import re
from queue import Queue
from typing import List

from lexos.helpers.constants import WHITESPACE
from lexos.helpers.error_messages import NEG_OVERLAP_LAST_PROP_MESSAGE, \
    LARGER_CHUNK_SIZE_MESSAGE, SEG_NON_POSITIVE_MESSAGE, \
    OVERLAP_LARGE_MESSAGE, PROP_NEGATIVE_MESSAGE, OVERLAP_NEGATIVE_MESSAGE, \
    INVALID_CUTTING_TYPE_MESSAGE, NON_POSITIVE_SEGMENT_MESSAGE, \
    EMPTY_MILESTONE_MESSAGE


def split_keep_whitespace(string) -> List[str]:
    """Splits the string on whitespace.

    Splitting while keeping the tokens on which the string was split.
    :param string: The string to split.
    :return The split string with the whitespace kept.
    """
    return re.split('([\u3000\n \t])', string)
    # Note: Regex in capture group keeps the delimiter in the resultant list


def count_words(text_list) -> int:
    """Counts the "words" in a list of tokens.

    The words are anything but not in the WHITESPACE global. In other words,
    ignoring WHITESPACE as being "not words".
    :param text_list: A list of tokens in the text.
    :return The number of words in the list.
    """
    return len([x for x in text_list if x not in WHITESPACE])


def strip_leading_white_space(word_queue: Queue):
    """Strips the leading whitespace

    This Stripping takes in the queue representation of the text.
    :param word_queue: The text in a Queue object separated by words.
    """
    if not word_queue.empty():
        while word_queue.queue[0] in WHITESPACE:
            word_queue.get()

            if word_queue.empty():
                break


def strip_leading_blank_lines(word_queue: Queue):
    """Strips the leading blank lines.

    This stripping takes in the queue representation of the text.
    :param word_queue: The text in a Queue object separated by words.
    """
    if not word_queue.empty():
        while word_queue.queue[0] == '':
            word_queue.get()

            if word_queue.empty():
                break


def strip_leading_characters(char_queue: Queue, num_chars: int):
    """Strips the leading characters by the value of num_chars.

    This stripping takes in the queue representation of the text.
    :param char_queue: The text in a Queue object.
    :param num_chars: The number of characters to remove.
    """
    for i in range(num_chars):
        char_queue.get()


def strip_leading_words(word_queue: Queue, num_words: int):
    """strips the leading words by the value of num_words.

    This stripping takes in the queue representation of the text.
    :param word_queue: The text in a Queue object.
    :param num_words: The number of words to remove.
    """
    for i in range(num_words):
        strip_leading_white_space(word_queue)
        word_queue.get()

    strip_leading_white_space(word_queue)


def strip_leading_lines(line_queue: Queue, num_lines: int):
    """strips the leading lines by the value of num_lines.

    This stripping takes in the queue representation of the text.
    :param line_queue: The text in a Queue object.
    :param num_lines: The number of lines to remove.
    """
    for i in range(num_lines):
        strip_leading_blank_lines(line_queue)
        line_queue.get()

    strip_leading_blank_lines(line_queue)


def cut_by_characters(text: str, chunk_size: int, overlap: int,
                      last_prop: float):
    """Cuts the text into equally sized chunks.

    where the segment size is measured by counts of characters, with an option
    for an amount of overlap between chunks and a minimum proportion threshold
    for the last chunk.
    :param text: The string with the contents of the file.
    :param chunk_size: The size of the chunk, in characters.
    :param overlap: The number of characters to overlap between chunks.
    :param last_prop: The min proportional size that the last chunk has to be.
    :return: A list of string that the text has been cut into.
    """
    # Chunk size has to be bigger than 0
    assert chunk_size > 0, NON_POSITIVE_SEGMENT_MESSAGE
    # The number of characters to overlap has to be bigger or equal to 0
    assert overlap >= 0, NEG_OVERLAP_LAST_PROP_MESSAGE
    # The proportional size of last chunk has to be bigger or equal to 0
    assert last_prop >= 0, NEG_OVERLAP_LAST_PROP_MESSAGE
    # Chunk size has to be bigger than overlap size
    assert chunk_size > overlap, LARGER_CHUNK_SIZE_MESSAGE

    # The list of the chunks (a.k.a a list of list of strings)
    chunk_list = []
    # The rolling window representing the (potential) chunk
    chunk_so_far = Queue()
    # Index keeping track of whether or not it's time to make a chunk out of
    # the window
    curr_chunk_size = 0
    # The distance between the starts of chunks
    till_next_chunk = chunk_size - overlap

    for token in text:
        curr_chunk_size += 1

        if curr_chunk_size > chunk_size:
            chunk_list.append(list(chunk_so_far.queue))

            strip_leading_characters(
                char_queue=chunk_so_far,
                num_chars=till_next_chunk)

            curr_chunk_size -= till_next_chunk

        chunk_so_far.put(token)

    # Making sure the last chunk is of a sufficient proportion
    last_chunk = list(chunk_so_far.queue)

    if (float(len(last_chunk)) / chunk_size) < last_prop:
        if len(chunk_list) == 0:
            chunk_list.extend(last_chunk)
        else:
            chunk_list[-1].extend(last_chunk)
    else:
        chunk_list.append(last_chunk)

    # Make the list of lists of strings into a list of strings
    count_sub_list = 0
    string_list = []
    for sub_list in chunk_list:
        string_list.extend([''.join(sub_list)])
        if isinstance(sub_list, list):
            count_sub_list += 1

    # Prevent there isn't sub_list inside chunk_list
    if count_sub_list == 0:
        string_list = []
        string_list.extend([''.join(chunk_list)])

    return string_list


def cut_by_words(text: str, chunk_size: int, overlap: int,
                 last_prop: float) -> List[str]:
    """Cuts the text into documents with the same number of words

    Cuts the text into equally sized chunks, where the segment size is measured
    by counts of words, with an option for an amount of overlap between chunks
    and a minimum proportion threshold for the last chunk.
    :param text: The string with the contents of the file.
    :param chunk_size: The size of the chunk, in words.
    :param overlap: The number of words to overlap between chunks.
    :param last_prop: The minimum proportional size that the last chunk has to
    be.
    :return: A list of string that the text has been cut into.
    """
    # PRE-conditions:
    assert chunk_size >= 1, SEG_NON_POSITIVE_MESSAGE
    assert chunk_size > overlap, OVERLAP_LARGE_MESSAGE
    assert last_prop >= 0, PROP_NEGATIVE_MESSAGE
    assert overlap >= 0, OVERLAP_NEGATIVE_MESSAGE

    # The list of the chunks (a.k.a a list of list of strings)
    chunk_list = []
    # The rolling window representing the (potential) chunk
    chunk_so_far = Queue()
    # Index keeping track of whether or not it's time to make a chunk out of
    # the window
    curr_chunk_size = 0
    # The distance between the starts of chunks
    till_next_chunk = chunk_size - overlap

    split_text = split_keep_whitespace(text)

    # Create list of chunks (chunks are lists of words and whitespace) by
    # using a queue as a rolling window
    for token in split_text:
        if token in WHITESPACE:
            chunk_so_far.put(token)

        else:
            curr_chunk_size += 1

            if curr_chunk_size > chunk_size:
                chunk_list.append(list(chunk_so_far.queue))

                strip_leading_words(word_queue=chunk_so_far,
                                    num_words=till_next_chunk)

                curr_chunk_size -= till_next_chunk

            chunk_so_far.put(token)

    # Making sure the last chunk is of a sufficient proportion
    last_chunk = list(chunk_so_far.queue)  # Grab the final (partial) chunk

    # If the proportion of the last chunk is too low
    if (float(count_words(last_chunk)) / chunk_size) < last_prop:
        if len(chunk_list) == 0:
            chunk_list.extend(last_chunk)
        else:
            chunk_list[-1].extend(last_chunk)
    else:
        chunk_list.append(last_chunk)

    # Make the list of lists of strings into a list of strings
    count_sub_list = 0
    string_list = []
    for sub_list in chunk_list:
        string_list.extend([''.join(sub_list)])
        if isinstance(sub_list, list):
            count_sub_list += 1

    # Prevent there isn't sub_list inside chunk_list
    if count_sub_list == 0:
        string_list = []
        string_list.extend([''.join(chunk_list)])

    return string_list


def cut_by_lines(text: str, chunk_size: int, overlap: int, last_prop: float) \
        ->List[str]:
    """Cuts the text into equally sized chunks.

    The size of the segment is measured by counts of lines, with an option for
    an amount of overlap between chunks and a minimum proportion threshold for
    the last chunk.
    :param text: The string with the contents of the file.
    :param chunk_size: The size of the chunk, in lines.
    :param overlap: The number of lines to overlap between chunks.
    :param last_prop: The minimum proportional size that the last chunk
           has to be.
    :return A list of string that the text has been cut into.
    """
    # pre-conditional assertion
    assert chunk_size > 0, NON_POSITIVE_SEGMENT_MESSAGE
    assert overlap >= 0 and last_prop >= 0, NEG_OVERLAP_LAST_PROP_MESSAGE
    assert chunk_size > overlap, LARGER_CHUNK_SIZE_MESSAGE
    # The list of the chunks (a.k.a. a list of list of strings)
    chunk_list = []
    # The rolling window representing the (potential) chunk
    chunk_so_far = Queue()
    # Index keeping track of whether or not it's time to make a chunk out of
    # the window
    curr_chunk_size = 0
    # The distance between the starts of chunks
    till_next_chunk = chunk_size - overlap

    split_text = text.splitlines(True)

    # Create list of chunks (chunks are lists of words and whitespace) by
    # using a queue as a rolling window
    for token in split_text:
        if token == '':
            raise AttributeError("there should not be empty string after "
                                 "splitlines")

        else:
            curr_chunk_size += 1

            if curr_chunk_size > chunk_size:
                chunk_list.append(list(chunk_so_far.queue))

                strip_leading_lines(line_queue=chunk_so_far,
                                    num_lines=till_next_chunk)

                curr_chunk_size -= till_next_chunk

            chunk_so_far.put(token)

    # Making sure the last chunk is of a sufficient proportion
    last_chunk = list(chunk_so_far.queue)  # Grab the final (partial) chunk

    # If the proportion of the last chunk is too low
    if (float(count_words(last_chunk)) / chunk_size) < last_prop:
        if len(chunk_list) == 0:
            chunk_list.extend(last_chunk)
        else:
            chunk_list[-1].extend(last_chunk)

    else:
        chunk_list.append(last_chunk)

    # Make the list of lists of strings into a list of strings
    count_sub_list = 0
    string_list = []
    for sub_list in chunk_list:
        string_list.extend([''.join(sub_list)])
        if isinstance(sub_list, list):
            count_sub_list += 1

    # Prevent there isn't sub_list inside chunk_list
    if count_sub_list == 0:
        string_list = []
        string_list.extend([''.join(chunk_list)])

    return string_list


def cut_by_number(text: str, num_chunks: int) -> List[str]:
    """Cuts the text into the desired number of chunks.

    The chunks created will be equal in terms of word count, or line count if
    the text does not have words separated by whitespace (see Chinese).
    :param text: The string with the contents of the file.
    :param num_chunks: The number of chunks to cut the text into.
    :return: A list of strings that the text has been cut into.
    """

    # Precondition: the number of segments requested must be non-zero, positive
    assert num_chunks > 0, NON_POSITIVE_SEGMENT_MESSAGE

    # The list of the chunks (a.k.a. a list of list of strings)
    chunk_list = []
    # The rolling window representing the (potential) chunk
    chunk_so_far = Queue()

    # Splits the string into tokens, including whitespace characters, which
    # will be between two non-whitespace tokens
    # For example, split_keep_whitespace(" word word ") returns:
    # ["", " ", "word", " ", "word", " ", ""]
    split_text = split_keep_whitespace(text)

    text_length = count_words(split_text)
    chunk_sizes = []

    # All chunks will be at least this long in terms of words/lines
    for i in range(num_chunks):
        chunk_sizes.append(text_length / num_chunks)

    # If the word count is not evenly divisible, the remainder is spread over
    # the chunks starting from the first one
    for i in range(text_length % num_chunks):
        chunk_sizes[i] += 1

    # Index keeping track of whether or not it's time to make a chunk out of
    # the window
    curr_chunk_size = 0
    chunk_index = 0
    chunk_size = chunk_sizes[chunk_index]

    # Create list of chunks (concatenated words and whitespace) by using a
    # queue as a rolling window
    for token in split_text:
        if token in WHITESPACE:
            chunk_so_far.put(token)

        else:
            curr_chunk_size += 1

            if curr_chunk_size > chunk_size:
                chunk_list.append(list(chunk_so_far.queue))

                chunk_so_far.queue.clear()
                curr_chunk_size = 1
                chunk_so_far.put(token)

                chunk_index += 1
                chunk_size = chunk_sizes[chunk_index]

            else:
                chunk_so_far.put(token)

    last_chunk = list(chunk_so_far.queue)  # Grab the final (partial) chunk
    chunk_list.append(last_chunk)

    # Make the list of lists of strings into a list of strings
    string_list = [''.join(subList) for subList in chunk_list]

    return string_list


def cut_by_milestone(text: str, cutting_value: str) -> List[str]:
    """Cuts the file into chunks by milestones and made chunk boundaries

    Chunk boundaries should be created when every milestone appears.
    :param text: the text to be chunked as a single string
    :param cutting_value: the value by which to cut the texts by.
    :return: A list of strings which are to become the new chunks.
    """
    # pre-condition assertion
    assert len(cutting_value) > 0, EMPTY_MILESTONE_MESSAGE

    chunk_list = text.split(cutting_value)

    return chunk_list


def cut(text: str, cutting_value: str, cutting_type: str, overlap: str,
        last_prop: str) -> List[str]:
    """Cuts each text string into various segments.

    Cutting according to the options chosen by the user.
    :param text: A string with the text to be split
    :param cutting_value: The value by which to cut the texts by.
    :param cutting_type: A string representing which cutting method to use.
    :param overlap: A unicode string representing the number of words to be
           overlapped between each text segment.
    :param last_prop: A unicode string representing the minimum proportion
           percentage the last chunk has to be to not get assimilated by
           the previous.
    :return A list of strings, each representing a chunk of the original.
    """
    # pre-condition assertion
    assert cutting_type == "milestone" or cutting_type == "letters" or \
        cutting_type == "words" or cutting_type == "lines" or \
        cutting_type == "number", INVALID_CUTTING_TYPE_MESSAGE
    cutting_type = str(cutting_type)
    overlap = int(overlap)
    last_prop = float(last_prop.strip('%')) / 100
    if cutting_type != 'milestone':
        cutting_value = int(cutting_value)

    if cutting_type == 'letters':
        string_list = cut_by_characters(text, cutting_value, overlap,
                                        last_prop)
    elif cutting_type == 'words':
        string_list = cut_by_words(text, cutting_value, overlap, last_prop)
    elif cutting_type == 'lines':
        string_list = cut_by_lines(text, cutting_value, overlap, last_prop)
    elif cutting_type == 'milestone':
        string_list = cut_by_milestone(text, cutting_value)
    elif cutting_type == 'number':
        string_list = cut_by_number(text, cutting_value)

    return string_list
