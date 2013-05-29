#!/usr/bin/python
# -*- coding: utf-8 -*-
import string, re, sys, unicodedata, os, pickle

def make_replacer(replacements):
	locator = re.compile('|'.join(re.escape(k) for k in replacements))

	def _doreplace(mo):
		return replacements[mo.group()]

	def replace(s):
		return locator.sub(_doreplace, s)

	return replace

def remove_punctuation(text, apos, hyphen):
		# this is a one-op; can we cache this table somehow?
		# (we should test this on multiple languages ...)

		# Translating all hyphens to one type

		# All UTF-16 values for different hyphens: for translating
		hyphen_values       = [8208,8211,8212,8213,8315,8331,65123,65293,56128,56365]
		chosen_hyphen_value = 45 # 45 correspondds to the hyphen-minus symbol

		# Create a dict of from_value:to_value out of the list and int
		trans_table = dict((value, chosen_hyphen_value) for value in hyphen_values)
		# Translate the text, converting all odd hyphens to one type
		text = text.translate(trans_table)

		punctuation_filename = "cache/punctuationmap.p"
		# Map of punctuation to be removed
		if os.path.exists(punctuation_filename):
			# print "Loading cached punctuation map"
			remove_punctuation_map = pickle.load(open(punctuation_filename, 'rb'))
		else:
			# print "No punctuation translate table cached - creating new"
			remove_punctuation_map = dict.fromkeys(i for i in xrange(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('P') or unicodedata.category(unichr(i)).startswith('S'))
			pickle.dump(remove_punctuation_map, open(punctuation_filename, 'wb'))

		# If keep apostrophes (UTF-16: 39) ticked
		if apos:
			del remove_punctuation_map[39]

		# If keep hyphens (UTF-16: 45) ticked
		if hyphen:
			del remove_punctuation_map[45]

		return text.translate(remove_punctuation_map)



def remove_stopwords(text, sw_file):
	sw_file = sw_file.split("\n")
	line_list = []
	for line in sw_file:
		line = line.strip()
		# Using re for multiple delimiter splitting
		line = re.split(', ', line)
		line_list.extend(line)

	# Create pattern
	remove = "|".join(line_list)
	# Compile pattern with bordering \b markers to demark only full words
	pattern = re.compile(r'\b(' + remove + r')\b')

	# Replace stopwords
	text = pattern.sub('', text)
	# Fill in extra spaces with 1 space
	text = re.sub(' +', ' ', text)

	return text

def lemmatize(text, lemma_file):
	lemma_lines = lemma_file.split("\n")

	for lemma_line in lemma_lines:
		lemma_line = lemma_line.strip()
		lemmaList = lemma_line.split(', ')
		lemma = lemmaList.pop(0)

		for i, changeMe in enumerate(lemmaList):
			theRegex = re.compile(r'\b' + changeMe + r'\b')
			text = theRegex.sub(lemma, text)

	print "Final text after lemmatize:", text
	return text

def consolidate(text, consolidation_file):
	consolidation_lines = consolidation_file.split("\n")

	for consolidation_line in consolidation_lines:
		consolidation_line = consolidation_line.strip()
		consolidationList = consolidation_line.split(', ')
		consolidation = consolidationList.pop(0)

		for i, changeMe in enumerate(consolidationList):
			theRegex = re.compile(changeMe)
			text = theRegex.sub(consolidation, text)

	print "Final text after consolidations:", text
	return text



def scrubber(text, lower, punct, apos, hyphen, digits, hastags, tags, opt_uploads):
	# originals    = u"ç,œ,á,é,í,ó,ú,à,è,ì,ò,ù,ä,ë,ï,ö,ü,ÿ,â,ê,î,ô,û,å,e,i,ø".split(',')
	# replacements = u"c,oe,a,e,i,o,u,a,e,i,o,u,a,e,i,o,u,y,a,e,i,o,u,a,e,i,o".split(',')
	# replace = dict(zip(originals,replacements))
	# for k, v in replace.iteritems():
	# 	text = text.replace(k, v)

	"""
	uploads order:
	0 - consolidations
	1 - lemmas
	2 - specialchars
	3 - stopwords
	"""
	uploads = sorted(opt_uploads.keys())
	files_uploaded = []
	for upload_type in uploads:
		if opt_uploads[upload_type].filename != '':
			files_uploaded.append(True)
		else:
			files_uploaded.append(False)

	if files_uploaded:
		consolidations = files_uploaded[0]
		lemmas = files_uploaded[1]
		specialchars = files_uploaded[2]
		stopwords = files_uploaded[3]
		got_files = True
	else:
		got_files = False


	"""
	Scrubbing order:
	1. lower
	2. special characters
	3. tags
	4. punctuation
	5. digits
	6. lemmatize
	7. consolidations
	8. stopwords
	"""

	if lower:
		text = text.lower()

	if got_files and specialchars:
		pass # TODO
	else: # Should be elif for "Default" choice
		commoncharacters = ["&ae;", "&d;", "&t;", "&e;", "&AE;", "&D;", "&T;"]
		commonunicode = [u"æ", u"ð", u"þ", u"e", u"Æ", u"Ð", u"Þ"]

		r = make_replacer(dict(zip(commoncharacters, commonunicode)))
		text = r(text)

	# handling nested tags?
	if hastags:
		if tags == "keep":
			text = re.sub('<[^<]+?>', "", text)
		else:
			#doesn't handle nested tags yet
			text = re.sub('>[^<]+</', "", text)
			text = re.sub('<[^<]+>', "", text)

	if punct:
		text = remove_punctuation(text, apos, hyphen)

	if digits:
		text = re.sub("\d+", '', text)

	if got_files and lemmas: # uploads[1] is lemma_file
		text = lemmatize( text, opt_uploads[uploads[1]].read() )

	if got_files and consolidations:
		text = consolidate( text, opt_uploads[uploads[0]].read() )

	if got_files and stopwords:
		text = remove_stopwords( text, opt_uploads[uploads[3]].read() )


	
	return text