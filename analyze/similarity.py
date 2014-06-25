from gensim import corpora, models, similarities

def similarityMaker(texts, compDoc, tempLabels):

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

	docsList = []

	for pair in sims:
		docsList.append(str(tempLabels[pair[0]]) + ",   " + str(pair[1]))

	return docsList
