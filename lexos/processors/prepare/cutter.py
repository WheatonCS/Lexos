import re
from queue import Queue
from typing import List
from lexos.helpers.error_messages import NON_POSITIVE_NUM_MESSAGE, \
    NEG_NUM_MESSAGE, LARGER_CHUNK_SIZE_MESSAGE
from lexos.helpers.constants import WHITESPACE


def split_keep_whitespace(string):
    """Splits the string on whitespace.

    Splitting while keeping the tokens on which the
    string was split.
    :param string: The string to split.
    :return The split string with the whitespace kept.
    """
    return re.split('(\u3000|\n| |\t)', string)
    # Note: Regex in capture group keeps the delimiter in the resultant list


def count_words(text_list):
    """Counts the "words" in a list of tokens.

    The words are anything but not in the WHITESPACE global. In other words,
    ignoring WHITESPACE as being "not words".
    :param text_list: A list of tokens in the text.
    :return The number of words in the list.
    """
    return len([x for x in text_list if x not in WHITESPACE])


def strip_leading_white_space(q):
    """Strips the leading whitespace

    This Stripping takes in the queue representation of the text.
    :param q: The text in a Queue object.
    """
    if not q.empty():
        while q.queue[0] in WHITESPACE:
            q.get()

            if q.empty():
                break


def strip_leading_blank_lines(q):
    """Strips the leading blank lines.

    This stripping takes in the queue representation of the text.
    :param q: The text in a Queue object.
    """
    while q.queue == '':
        q.get()

        if q.empty():
            break


def strip_leading_characters(char_queue, num_chars):
    """Strips the leading characters by the value of num_chars.

    This stripping takes in the queue representation of the text.
    :param char_queue: The text in a Queue object.
    :param num_chars: The number of characters to remove.
    """
    for i in range(num_chars):
        char_queue.get()


def strip_leading_words(word_queue, num_words):
    """strips the leading words by the value of num_words.

    This stripping takes in the queue representation of the text.
    :param word_queue: The text in a Queue object.
    :param num_words: The number of words to remove.
    """
    for i in range(num_words):
        strip_leading_white_space(word_queue)
        word_queue.get()

    strip_leading_white_space(word_queue)


def strip_leading_lines(line_queue, num_lines):
    """strips the leading lines by the value of num_lines.

    This stripping takes in the queue representation of the text.
    :param line_queue: The text in a Queue object.
    :param num_lines: The number of lines to remove.
    """
    for i in range(num_lines):
        strip_leading_blank_lines(line_queue)
        line_queue.get()

    strip_leading_blank_lines(line_queue)


def cut_by_characters(text, chunk_size, overlap, last_prop):
    """Cuts the text into equally sized chunks.

    where the segment size is measured
    by counts of characters,
    with an option for an amount of overlap between chunks and a minimum
    proportion threshold for the last chunk.

    Args:
        text: The string with the contents of the file.
        chunk_size: The size of the chunk, in characters.
        overlap: The number of characters to overlap between chunks.
        last_prop: The minimum proportional size that the last chunk has to be.

    Returns:
        A list of string that the text has been cut into.
    """
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


def cut_by_words(text, chunk_size, overlap, last_prop):
    """
    Cuts the text into equally sized chunks, where the segment size is measured
     by counts of words,
    with an option for an amount of overlap between chunks and a minimum
    proportion threshold for the last chunk.

    Args:
        text: The string with the contents of the file.
        chunk_size: The size of the chunk, in words.
        overlap: The number of words to overlap between chunks.
        last_prop: The minimum proportional size that the last chunk has to be.

    Returns:
        A list of string that the text has been cut into.
    """
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


def cut_by_lines(text: str, chunk_size: int, overlap: int, last_prop: int) -> \
        List[str]:
    """Cuts the text into equally sized chunks.

    The size of the segment is measured by counts of lines,
    with an option for an amount of overlap between chunks and a minimum
    proportion threshold for the last chunk.
    :param text: The string with the contents of the file.
    :param chunk_size: The size of the chunk, in lines.
    :param overlap: The number of lines to overlap between chunks.
    :param last_prop: The minimum proportional size that the last chunk
           has to be.
    :return A list of string that the text has been cut into.
    """
    # pre-conditional assertion
    assert chunk_size > 0, NON_POSITIVE_NUM_MESSAGE
    assert overlap >= 0 and last_prop >= 0, NEG_NUM_MESSAGE
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
            chunk_so_far.put(token)

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


def cut_by_number(text, num_chunks):
    """
    Cuts the text into equally sized chunks, where the size of the chunk is
    determined by the number of desired chunks.

    Args:
        text: The string with the contents of the file.
        num_chunks: The number of chunks to cut the text into.

    Returns:
        A list of string that the text has been cut into.
    """
    # The list of the chunks (a.k.a. a list of list of strings)
    chunk_list = []
    # The rolling window representing the (potential) chunk
    chunk_so_far = Queue()

    split_text = split_keep_whitespace(text)

    text_length = count_words(split_text)
    chunk_sizes = []
    for i in range(num_chunks):
        chunk_sizes.append(text_length / num_chunks)

    for i in range(text_length % num_chunks):
        chunk_sizes[i] += 1

    # Index keeping track of whether or not it's time to make a chunk out of
    # the window
    curr_chunk_size = 0
    chunk_index = 0
    chunk_size = chunk_sizes[chunk_index]

    # Create list of chunks (chunks are lists of words and whitespace) by
    # using a queue as a rolling window
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


def cut_by_milestone(text, cutting_value):
    """
    Cuts the file into as many chunks as there are instances of the
        substring cuttingValue.  Chunk boundaries are made wherever
        the string appears.
    Args: text -- the text to be chunked as a single string

    Returns: A list of strings which are to become the new chunks.
    """
    chunk_list = []  # container for chunks
    len_milestone = len(cutting_value)  # length of milestone term
    cutting_value = cutting_value

    if len(cutting_value) > 0:
        chunk_stop = text.find(cutting_value)  # first boundary
        # trap for error when first word in file is Milestone
        while chunk_stop == 0:
            text = text[len_milestone:]
            chunk_stop = text.find(cutting_value)

        # while next boundary != -1 (while next boundary exists)
        while chunk_stop >= 0:
            # print chunkstop
            # new chunk  = current text up to boundary index
            next_chunk = text[:chunk_stop]
            # text = text left after the boundary
            text = text[chunk_stop + len_milestone:]
            chunk_stop = text.find(cutting_value)  # first boundary

            # trap for error when first word in file is Milestone
            while chunk_stop == 0:
                if chunk_stop == 0:
                    text = text[len_milestone:]
                    chunk_stop = text.find(cutting_value)
            chunk_list.append(next_chunk)  # append this chunk to chunk list

        if len(text) > 0:
            chunk_list.append(text)
    else:
        chunk_list.append(text)

    return chunk_list


def cut(text, cutting_value, cutting_type, overlap, last_prop):
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
    cutting_type = str(cutting_type)
    if cutting_type != 'milestone':
        cutting_value = int(cutting_value)
    overlap = int(overlap)
    last_prop = float(last_prop.strip('%')) / 100

    if cutting_type == 'letters':
        string_list = cut_by_characters(text, cutting_value, overlap,
                                        last_prop)
    elif cutting_type == 'words':
        string_list = cut_by_words(text, cutting_value, overlap, last_prop)
    elif cutting_type == 'lines':
        string_list = cut_by_lines(text, cutting_value, overlap, last_prop)
    elif cutting_type == 'milestone':
        string_list = cut_by_milestone(text, cutting_value)
    else:
        string_list = cut_by_number(text, cutting_value)

    return string_list
