import re


# function key:
#     def __1__+__2__+__3__
#     1 = a or r for average or ratio
#     2 = keyword, (string (string includes regex) or word)
#     3 = windowtype, (letter, wordline, word or line)

# works regex
def a_string_letter(file_string, key_letter, window_size, token_type):
    """
    Computes the rolling average of one letter over a certain window
    (size in characters). aka. Letter average in a window of letters.

    Args:
        file_string: the text from file
        key_letter: the letter to count and average
        window_size: the number of letters to have in the window

    Returns:
        List of averages, each index representing the window number
    """
    window_start = 0
    window_end = window_start + window_size

    # Rolling count, to be divided for average
    averages = []

    if token_type == 'string':
        literal = re.escape(key_letter)
        search_term = re.compile(literal)
    else:
        search_term = re.compile(key_letter, re.UNICODE)

    while window_end < len(file_string) + 1:
        # make slice corresponding to current window boundaries
        current_window = file_string[window_start:window_end]
        # find all occurrences of term in slice
        hits = search_term.findall(current_window)

        if not hits:
            count = 0
        else:  # if iterable is not empty
            count = len(hits)
        averages.append(float(count) / window_size)
        # move window boundaries forward and reset count to 0
        window_end += 1
        window_start += 1

    return averages


# works regex
def a_string_word_line(split_list, key_letter, window_size, token_type):
    """
    Computes the rolling average of one letter over a certain window
    (size in words or lines) aka, Letter average in a window of words or lines.

    Args:
        split_list: the text already split by words or lines, as chosen
        key_letter: the letter to count and average
        window_size: the number of words or lines to have in the window

    Returns:
        List of averages, each index representing the window number
    """
    window_start = 0
    window_end = window_start + window_size

    averages = []

    if token_type == 'string':
        literal = re.escape(key_letter)
        search_term = re.compile(literal)
    else:
        search_term = re.compile(key_letter, re.UNICODE)

    while window_end < len(split_list) + 1:
        # make one string out of all words or lines
        current_window = ' '.join(split_list[window_start: window_end])
        # find all instances of search term and return iterator
        hits = search_term.findall(current_window)

        if not hits:
            count = 0
        else:
            count = len(hits)
        averages.append(float(count) / window_size)

        window_end += 1
        window_start += 1

    return averages


def a_word_word(split_list, keyword, window_size):
    """
    Computes the rolling average of one word over a certain window
    (size in words). aka. Word average in a window of words.

    Args:
        split_list: the text already split by words or lines, as chosen
        keyword: the word to count and average
        window_size: the number of words to have in the window

    Returns:
        List of averages, each index representing the window number
    """
    window_start = 0
    window_end = window_start + window_size

    # Rolling count, to be divided for average
    count = 0

    # Count the initial window (counts the number of matches in the starting
    # window)
    for i in range(window_start, window_end):
        if split_list[i] == keyword:
            count += 1

    # Create list with initial value
    averages = [float(count) / window_size]

    while window_end < len(split_list):
        # Adds one to count if a new match enters the window
        if split_list[window_end] == keyword:
            count += 1
        # Subtracts one from count if a match moves out of the window
        if split_list[window_start] == keyword:
            count -= 1

        # Compute average for window
        averages.append(float(count) / window_size)

        # Increment window indices
        window_end += 1
        window_start += 1

    return averages


def a_word_line(split_list, keyword, window_size):
    """
    Computes the rolling average of one word over a certain window
    (size in lines). aka. Word average in a window of lines.

    Args:
        split_list: the text already split by words or lines, as chosen
        keyword: the word to count and average
        window_size: the number of lines to have in the window

    Returns:
        List of averages, each index representing the window number
    """
    window_start = 0
    window_end = window_start + window_size

    # Rolling count, to be divided for average
    count = 0

    window_word_length = 0  # window length (in # of words)

    lines = []

    # Split the lines into words for comparison and counting
    for i in range(len(split_list)):
        lines.append(split_list[i].split())

    # Count the initial window
    for i in range(window_start, window_end):
        window_word_length += len(lines[i])
        for word in lines[i]:
            if word == keyword:
                count += 1

    # Create list with initial value
    averages = [float(count) / window_word_length]

    while window_end < len(lines):
        # Adds one to count if a new match enters the window
        for word in lines[window_end]:
            if word == keyword:
                count += 1
        # Subtracts one from count if a match moves out of the window
        for word in lines[window_start]:
            if word == keyword:
                count -= 1

        # Adjust window size
        window_word_length += len(lines[window_end])
        window_word_length -= len(lines[window_start])

        # Compute average for window
        averages.append(float(count) / window_size)

        # Increment window indices
        window_end += 1
        window_start += 1

    return averages


def r_string_letter(file_string, first_string, second_string, window_size,
                    token_type):
    """
    Computes the rolling ratio of one letter to another over a certain window
    (size in letters).
    aka. Letter ratio in a window of letters.

    Args:
        file_string: the text from file
        first_string: the letter to count, for the ratio's numerator
        second_string: the letter to count, for the ratio's denominator
        window_size: the number of letters to have in the window

    Returns:
        List of ratios, each index representing the window number
    """
    window_start = 0
    window_end = window_start + window_size

    # Rolling count, to be divided for average
    ratios = []

    if token_type == 'string':
        literal_one = re.escape(first_string)
        first_search_term = re.compile(literal_one)
        second_search_term = re.compile(second_string)
    else:
        first_search_term = re.compile(first_string, re.UNICODE)
        second_search_term = re.compile(second_string, re.UNICODE)

    while window_end < len(file_string) + 1:

        current_window = file_string[window_start:window_end]
        hits1 = first_search_term.findall(current_window)
        hits2 = second_search_term.findall(current_window)

        count1 = len(hits1)
        count2 = len(hits2)

        if count1 + count2 != 0:
            ratios.append(float(count1) / float(count1 + count2))
        else:
            ratios.append(0)

        window_end += 1
        window_start += 1

    return ratios


def r_string_word_line(split_list, first_string, second_string, window_size,
                       token_type):  # works regex
    """
    Computes the rolling ratio of one letter to another over a certain window
    (size in words or lines).
    aka. Letter ratio in a window of words or lines.

    Args:
        split_list: the text already split by words or lines, as chosen
        first_string: the letter to count, for the ratio's numerator
        second_string: the letter to count, for the ratio's denominator
        window_size: the number of words or lines to have in the window

    Returns:
        List of ratios, each index representing the window number
    """
    window_start = 0
    window_end = window_start + window_size

    ratios = []

    if token_type == 'string':
        literal_one = re.escape(first_string)
        first_search_term = re.compile(literal_one)
        second_search_term = re.compile(second_string)
    else:
        first_search_term = re.compile(first_string, re.UNICODE)
        second_search_term = re.compile(second_string, re.UNICODE)

    while window_end < len(split_list) + 1:

        current_window = ' '.join(
            split_list[window_start: window_end])  # get current window
        # find matches for first term
        hits1 = first_search_term.findall(current_window)
        # find matches for second term
        hits2 = second_search_term.findall(current_window)

        count1 = len(hits1)
        count2 = len(hits2)

        if count1 == 0 and count2 == 0:  # calculate ratio
            ratios.append(0)
        else:
            ratios.append(float(count1) / float(count1 + count2))
        # move window and reset counts
        window_end += 1
        window_start += 1

    return ratios


def r_word_word(split_list, first_word, second_word, window_size):
    """
    Computes the rolling ratio of one word to another over a certain window
    (size in words).
    aka. Word ratio in a window of words.

    Args:
        split_list: the text already split by words or lines, as chosen
        first_word: the word to count, for the ratio's numerator
        second_word: the word to count, for the ratio's denominator
        window_size: the number of words to have in the window

    Returns:
        List of ratios, each index representing the window number
    """
    window_start = 0
    window_end = window_start + window_size

    # Rolling counts, to be divided for ratio
    first = 0
    second = 0

    words = []

    # Split the lines into words for comparison and counting
    for i in range(len(split_list)):
        words.append(split_list[i])

    # Count the initial window
    for i in range(window_start, window_end):
        if first_word == words[i]:
            first += 1
        if second_word == words[i]:
            second += 1

    # Create list with initial value
    if first == 0 and second == 0:
        ratios = [0]
    else:
        ratios = [float(first) / (first + second)]

    while window_end < len(words):

        # increase counter if a match moves into window
        if words[window_end] == first_word:
            first += 1

        # increase counter if a match moves into window
        if words[window_end] == second_word:
            second += 1

        # Decrease count if match moves out of window
        if words[window_start] == first_word:
            first -= 1

        # Decrease count if match moves out of window
        if words[window_start] == second_word:
            second -= 1

        if second == 0 and first == 0:  # calculate ratio
            ratios.append(0)
        else:
            ratios.append(float(first) / (first + second))

        # Increment window indices
        window_end += 1
        window_start += 1

    return ratios


def r_word_line(split_list, first_word, second_word, window_size):
    """
    Computes the rolling ratio of one word to another over a certain window
    (size in lines).
    aka. Word ratio in a window of lines.

    Args:
        split_list: the text already split by words or lines, as chosen
        first_word: the word to count, for the ratio's numerator
        second_word: the word to count, for the ratio's denominator
        window_size: the number of lines to have in the window

    Returns:
        List of ratios, each index representing the window number
    """
    window_start = 0
    window_end = window_start + window_size

    # Rolling counts, to be divided for ratio
    first = 0
    second = 0

    lines = []

    # Split the lines into words for comparison and counting
    for i in range(len(split_list)):
        lines.append(split_list[i].split())

        # Count the initial window
    for i in range(window_start, window_end):
        for word in lines[i]:
            if word == first_word:
                first += 1
            if word == second_word:
                second += 1

    # Create list with initial value
    if first == 0 and second == 0:
        ratios = [0]
    else:
        ratios = [float(first) / (first + second)]

    while window_end < len(lines):
        # Counter++ if new match moves into window
        for word in lines[window_end]:
            if word == first_word:
                first += 1
            if word == second_word:
                second += 1

        # Counter-- if new match moves out of window
        for word in lines[window_start]:
            if word == first_word:
                first -= 1
            if word == second_word:
                second -= 1

        if second == 0 and first == 0:  # Calculate ratio
            ratios.append(0)
        else:
            ratios.append(float(first) / (first + second))

        # Increment window indices
        window_end += 1
        window_start += 1

    return ratios


##########################################################################

def rw_analyze(
        file_string,
        count_type,
        token_type,
        window_type,
        key_word,
        second_key_word,
        window_size):
    """
    Creates a rolling window plot depending on the specifications chosen by
    the user.

    Args:

    Returns:

    """

    if window_size != "":
        window_size = int(window_size)
    else:
        window_size = 1000

    # for when finding strings in window need original value
    min_num_of_windows = 10

    # if windowType is a word or line, splits the list accordingly
    if window_type == 'word':
        split_list = file_string.split()
    elif window_type == 'line':
        if re.search('\r', file_string) is not None:
            split_list = file_string.split('\r')
        else:
            split_list = file_string.split('\n')

    if window_type == 'word' or window_type == 'line':
        split_list = [i for i in split_list if i != '']

        if window_size > len(split_list) - min_num_of_windows:
            window_size = len(split_list) - min_num_of_windows
            if window_size <= 0:
                window_size = 1
    else:
        if window_size > len(file_string) - min_num_of_windows:
            window_size = len(file_string) - min_num_of_windows
            if window_size <= 0:
                window_size = 1

    ##########################################################################
    # if keyWord has multiple values, separates into list

    if (re.search(', ', key_word) is not None or
            re.search(',', key_word) is not None):
        split_key_words = key_word.replace(", ", "###")
        split_key_words = split_key_words.replace(",", "###")
        split_key_words = split_key_words.split("###")
    else:
        split_key_words = [key_word]

    if (re.search(', ', second_key_word) is not None or
            re.search(',', key_word) is not None):
        split_key_words2 = second_key_word.replace(", ", "###")
        split_key_words2 = split_key_words2.replace(",", "###")
        split_key_words2 = split_key_words2.split('###')
    else:
        split_key_words2 = [second_key_word]

    ##########################################################################

    # sends you to the right function depending on user choices
    plot_list = []

    # Call the correct analysis function to get plot data
    if count_type == 'average':
        if token_type == 'string' or token_type == 'regex':
            if window_type == 'letter':
                for i in (range(len(split_key_words))):
                    plot_list.append(
                        a_string_letter(file_string,
                                        split_key_words[i],
                                        window_size,
                                        token_type))

            else:  # windowType == 'word' or windowType == 'line'
                for i in (range(len(split_key_words))):
                    plot_list.append(
                        a_string_word_line(split_list,
                                           split_key_words[i],
                                           window_size,
                                           token_type))

        else:  # tokenType == 'word'
            if window_type == 'word':
                for i in (range(len(split_key_words))):
                    plot_list.append(
                        a_word_word(split_list,
                                    split_key_words[i],
                                    window_size))

            else:  # windowType == 'line'
                for i in (range(len(split_key_words))):
                    plot_list.append(
                        a_word_line(split_list,
                                    split_key_words[i],
                                    window_size))

    elif count_type == 'ratio':
        if token_type == 'string' or token_type == 'regex':
            if window_type == 'letter':
                for i in (range(len(split_key_words))):
                    plot_list.append(
                        r_string_letter(file_string,
                                        split_key_words[i],
                                        split_key_words2[i],
                                        window_size,
                                        token_type))

            else:  # windowType == 'line' or 'word'
                for i in (range(len(split_key_words))):
                    plot_list.append(
                        r_string_word_line(split_list,
                                           split_key_words[i],
                                           split_key_words2[i],
                                           window_size,
                                           token_type))

        else:  # tokenType == 'word'
            if window_type == 'word':
                for i in (range(len(split_key_words))):
                    plot_list.append(
                        r_word_word(split_list,
                                    split_key_words[i],
                                    split_key_words2[i],
                                    window_size))

            else:  # windowType == 'line'
                for i in (range(len(split_key_words))):
                    plot_list.append(
                        r_word_line(split_list,
                                    split_key_words[i],
                                    split_key_words2[i],
                                    window_size))

    # Give correct labels according to input type
    if window_type == 'letter':
        count_unit_label = 'characters'
        x_axis_label = "First character in window"
    elif window_type == 'word':
        count_unit_label = 'words'
        x_axis_label = "First word in window"
    else:
        count_unit_label = 'lines'
        x_axis_label = "First line in window"

    if count_type == 'average':
        y_axis_label = 'Average'
        graph_title = "Average number of " + key_word + "'s in a window of " +\
                      str(window_size) + " " + count_unit_label + "."
    else:
        y_axis_label = 'Ratio'
        graph_title = "Ratio of " + key_word + "'s to (number of " + \
                      key_word + "'s + number of " + second_key_word + \
                      "'s) in a window of " + str(window_size) + " " + \
                      count_unit_label + "."
    return plot_list, graph_title, x_axis_label, y_axis_label
