#!/usr/bin/python
# -*- coding: utf-8 -*-
import string, re, sys, unicodedata

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

		# 39 is apos, deal with that


		# this only works for ascii characters
		#table = string.maketrans("","")
		#text = text.translate(table, string.punctuation)
		
		# note: string.punctuation is ONLY the ascii punctuation;
		#remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

		# this is a one-op; can we cache this table somehow?
		# (we should test this on multiple languages ...)
		remove_punctuation_map = dict.fromkeys(i for i in xrange(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('P'))

		text = text.translate(remove_punctuation_map)

	if digits:
		text = re.sub("\d+", '', text)

	return text
