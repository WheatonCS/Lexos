from gensim import corpora, models, similarities

def similarityMaker(texts, compDoc, tempLabels, useUniqueTokens):

	#if useUniqueTokens is true, modify texts before creating dictionary
	if useUniqueTokens:
		all_tokens = sum(texts, [])
		tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
		texts = [[word for word in text if word not in tokens_once] for text in texts]

	#sets up dictionary, corpus, and lsi model
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

	#creates lsi vector for comparison document
	vec_bow = dictionary.doc2bow(compDoc)
	vec_lsi = lsi[vec_bow]

	# transform corpus to LSI space and index it
	index = similarities.MatrixSimilarity(lsi[corpus]) 
	sims = index[vec_lsi] #perform a similarity query against the corpus
	sims = sorted(enumerate(sims), key=lambda item: -item[1])

	docsListscore = []
	docsListname = []

	for pair in sims:
		docsListname.append(str(tempLabels[pair[0]]))
		docsListscore.append(str(pair[1]))

	return docsListscore, docsListname
