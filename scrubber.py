#!/usr/bin/python
# -*- coding: utf-8 -*-
import string, re, sys, unicodedata

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

	if punct:

		# 39 is apos, deal with that


		# this only works for ascii characters
		#table = string.maketrans("","")
		#text = text.translate(table, string.punctuation)
		
		# note: string.punctuation is ONLY the ascii punctuation; 
		#remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

		# this is a one-op; can we cache this table somehow?
		# (we should test this on multiple languages ...)
		remove_punctuation_map = dict.fromkeys(i for i in xrange(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('P'))
		print text
		text = text.translate(remove_punctuation_map)

	if digits:
		text = re.sub("\d+", '', text)

	return text
