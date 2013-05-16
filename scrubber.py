#!/usr/bin/python
# -*- coding: utf-8 -*-
import string, re, sys, unicodedata

def remove_stopwords(text, SW_file):
	# Grab stopwords into a list from the file
	for line in SW_file:
		line = line.strip()
		# Using re for multiple delimiter splitting
		line = re.split(', ', line)

	# Create pattern
	remove = "|".join(line)
	# Compile pattern with bordering \b markers to demark only full words
	pattern = re.compile(r'\b(' + remove + r')\b')

	# Replace stopwords
	text = pattern.sub('', text)
	# Fill in extra spaces with 1 space
	text = re.sub(' +', ' ', text)

	return text

def convertedLemmatize(text, lemmaFileName):
	with open(lemmaFileName,"r") as data:
		for line in data:
			line = line.strip()
			lemmaList = line.split(', ')
		lemma = lemmaList[0]
		i = 1
		while (i < len(lemmaList) ):
			changeMe = lemmaList[i]
			print "convert", changeMe, "to", lemma
			i = i+1
			# time for some regex magic
			theRegex = re.compile(r'\b' + changeMe + r'\b')
			text = theRegex.sub(lemma, text)
			print "new text is:", text

		print "final text:", text
	return text


def make_replacer(replacements):
	locator = re.compile('|'.join(re.escape(k) for k in replacements))

	def _doreplace(mo):
		return replacements[mo.group()]

	def replace(s):
		return locator.sub(_doreplace, s)

	return replace

def scrubber(text, lower, punct, apos, hyphen, digits):
	# originals    = u"ç,œ,á,é,í,ó,ú,à,è,ì,ò,ù,ä,ë,ï,ö,ü,ÿ,â,ê,î,ô,û,å,e,i,ø".split(',')
	# replacements = u"c,oe,a,e,i,o,u,a,e,i,o,u,a,e,i,o,u,y,a,e,i,o,u,a,e,i,o".split(',')
	# replace = dict(zip(originals,replacements))
	# for k, v in replace.iteritems():
	# 	text = text.replace(k, v)

	# handling nested tags?
	text = re.sub('<[^<]+>', "", text)

	if lower:
		text = text.lower()

	commoncharacters = ["&ae;", "&d;", "&t;", "&e;", "&AE;", "&D;", "&T;"]
	commonunicode = [u"æ", u"ð", u"þ", u"e", u"Æ", u"Ð", u"Þ"]

	r = make_replacer(dict(zip(commoncharacters, commonunicode)))
	text = r(text)

	

	if punct:

		# 39 is apos, 45 is hyphen
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

		# Map of punctuation to be removed
		remove_punctuation_map = dict.fromkeys(i for i in xrange(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('P') or unicodedata.category(unichr(i)).startswith('S'))

		# If keep apostrophes ticked
		if apos:
			del remove_punctuation_map[39]

		# If keep hyphens ticked
		if hyphen:
			del remove_punctuation_map[45]

		text = text.translate(remove_punctuation_map)

	if digits:
		text = re.sub("\d+", '', text)

	return text
