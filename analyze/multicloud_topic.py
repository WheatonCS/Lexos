import numpy as np

def topicJSONmaker(malletPath):

    # Configuration
    inpath = malletPath # Insert the path to the Mallet file here
    num_top_words = 100 # Top N number of words in each topic that will appear in output
    mallet_vocab = []
    word_topic_counts = []
    topics = []

    # Calculate the number of topics in the model
    n_topics = []
    with open(inpath) as data:
        for line in data:
            l = line.rstrip().split(' ') # Split the line on spaces
            id = l[0] # Get the word ID from the first item in the list
            word = l[1] # Get the word token from the second item in the list
            l[0:2] = [] # Delete the ID and word from the list
            topic_count_pairs = [pair.split(':') for pair in l] # New list topic-count pairs
            for topic, count in topic_count_pairs:
                n_topics.append(int(topic)) # New list with topics
    n_topics.sort() # Sort the topics
    num_topics = max(n_topics) + 1 # The number of topics in the model is the highest in the list

    # Re-shape the file data
    with open(inpath) as f:
        for line in f:
            l = line.rstrip().split(' ')
            id = l[0]
            word = l[1]
            l[0:2] = []
            topic_count_pairs = [pair.split(':') for pair in l]
            mallet_vocab.append(word)
            counts = np.zeros(num_topics)
            for topic, count in topic_count_pairs:
                counts[int(topic)] = int(count)
            word_topic_counts.append(counts)

    word_topic = np.array(word_topic_counts)
    word_topic.shape
    word_topic = word_topic / np.sum(word_topic, axis=0)
    mallet_vocab = np.array(mallet_vocab)

    # Generate a topics dictionary
    for t in range(num_topics):
        top_words_idx = np. argsort(word_topic[:,t])[::-1]
        top_words_idx = top_words_idx[:num_top_words]
        top_words = mallet_vocab[top_words_idx]
        top_words_shares = word_topic[top_words_idx, t]
        #print("Topic{}".format(t))
        topics.append({})
        for word, share in zip(top_words, top_words_shares):
            topics[t].update({word: np.round(share,3)}) # Create the topics dictionary
            #print("{} : {}".format(word, np.round(share,3)))

    # For Lexos, build the json string
    jsonStr = ""

    for i in xrange(len(topics)):
        jsonStr += '{"name": "Topic' + str(i) + '.txt", "children": ['
        children = ""
        for name, size in topics[i].iteritems():
            children += ', {"text": "%s", "size": %s}' % (name, size*1000)
            children = children.lstrip(', ')
        jsonStr += children
        jsonStr += ']}, '
    jsonStr = jsonStr[:-2]

    # Send the jsonStr variable to the template

    JSONObj = []

    for i in xrange(len(topics)):
        newChildrenlist = []

        for name, size in topics[i].iteritems():
            newChildrenlist.append({"text": name, "size": size*1000})

        JSONObj.append({"name": "Topic" + str(i) + ".txt", "children": newChildrenlist})

    return JSONObj