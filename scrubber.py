#!/usr/bin/python
# -*- coding: utf-8 -*-
import string, re

def scrubber(text, lower, punct):
	originals = u"ç,œ,á,é,í,ó,ú,à,è,ì,ò,ù,ä,ë,ï,ö,ü,ÿ,â,ê,î,ô,û,å,e,i,ø".split(',')
	replacements = u"c,oe,a,e,i,o,u,a,e,i,o,u,a,e,i,o,u,y,a,e,i,o,u,a,e,i,o".split(',')
	replace = dict(zip(originals,replacements))
	for k, v in replace.iteritems():
		text = text.replace(k, v)
	text = re.sub('<[^<]+>', "", text)
	if lower:
		text = text.lower()
	if punct:
		text = text.translate(string.maketrans("",""), string.punctuation)
	return text