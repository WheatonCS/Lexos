from typing import List

import numpy as np


def topic_json_maker(mallet_path: str) -> List[dict]:
    # Configuration
    in_path = mallet_path  # Insert the path to the Mallet file here
    # Top N number of words in each topic that will appear in output
    num_top_words = 100
    mallet_vocab = []
    word_topic_counts = []
    topics = []

    # Calculate the number of topics in the model
    n_topics = []
    with open(in_path, encoding='utf-8') as data:
        for line in data:
            try:
                l = line.rstrip().split(' ')  # Split the line on spaces
                l[0:2] = []  # Delete the ID and word from the list
                # New list topic-count pairs
                topic_count_pairs = [pair.split(':') for pair in l]
                for topic, count in topic_count_pairs:
                    n_topics.append(int(topic))  # New list with topics
            except ValueError:
                raise ValueError(
                    'Your source data cannot be parsed into a regular number '
                    'of columns. Please ensure that there are no spaces in '
                    'your file names or file paths. It may be easiest to open'
                    ' the output_state file in a spreadsheet using a space as '
                    'the delimiter to ensure that there are a regular number '
                    'of columns. Please fix any misaligned data and upload '
                    'the data again.')

    n_topics.sort()  # Sort the topics
    # The number of topics in the model is the highest in the list
    num_topics = max(n_topics) + 1

    # Re-shape the file data
    with open(in_path, encoding='utf-8') as f:
        for line in f:
            l = line.rstrip().split(' ')
            word = l[1]
            l[0:2] = []
            topic_count_pairs = [pair.split(':') for pair in l]
            mallet_vocab.append(word)
            counts = np.zeros(num_topics)
            for topic, count in topic_count_pairs:
                counts[int(topic)] = int(count)
            word_topic_counts.append(counts)

    word_topic = np.array(word_topic_counts)
    word_topic = word_topic / np.sum(word_topic, axis=0)
    mallet_vocab = np.array(mallet_vocab)

    # Generate a topics dictionary
    for t in range(num_topics):
        top_words_idx = np.argsort(word_topic[:, t])[::-1]
        top_words_idx = top_words_idx[:num_top_words]
        top_words = mallet_vocab[top_words_idx]
        top_words_shares = word_topic[top_words_idx, t]
        topics.append({})
        for word, share in zip(top_words, top_words_shares):
            # Create the topics dictionary
            topics[t].update({word: np.round(share, 3)})

    # Begin Topics to Document Files Conversion

    # If the convert topics check box is checked create topic files
    from flask import request
    checked = request.form.getlist('convertTopics')
    if len(checked) != 0:

        # Generate a full topics dictionary for topic files
        topics_full = []
        for t in range(num_topics):
            top_words_idx = np.argsort(word_topic[:, t])[::-1]
            top_words = mallet_vocab[top_words_idx]
            top_words_shares = word_topic[top_words_idx, t]
            topics_full.append({})
            for word, share in zip(top_words, top_words_shares):
                # Create the full topics dictionary
                topics_full[t].update({word: np.round(share, 3)})

        import lexos.managers.utility
        file_manager = lexos.managers.utility.load_file_manager()
        for i in range(len(topics_full)):
            fn = "Topic" + str(i) + ".txt"
            text = ""
            for name, size in topics_full[i].items():
                count = int(size * 1000)
                term = ""
                for c in range(count):
                    term += name + " "
                text += term + " "
            # Save the topic file to the file manager
            file_manager.add_upload_file(text, fn)
            lexos.managers.utility.save_file_manager(file_manager)

    # End Topics to Document Files Conversion

    # For Lexos, build the json string
    json_str = ""

    for i in range(len(topics)):
        json_str += '{"name": "Topic' + str(i) + '.txt", "children": ['
        children = ""
        for name, size in topics[i].items():
            children += ', {"text": "%s", "size": %s}' % (name, size * 1000)
            children = children.lstrip(', ')
        json_str += children
        json_str += ']}, '

    # Send the json_str variable to the template
    json_obj = []

    for i in range(len(topics)):
        new_children_list = []

        for name, size in topics[i].items():
            new_children_list.append({"text": name, "size": size * 1000})

        json_obj.append({"name": "Topic" + str(i) + ".txt",
                        "children": new_children_list})

    return json_obj
