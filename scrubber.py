#!/usr/bin/python
# -*- coding: utf-8 -*-
import string, re, sys, unicodedata, os, pickle
from flask import Flask, request, session

def handle_specialcharacters(text, got_files, specialchars):
	if got_files and specialchars:
		text = format_special(text, opt_uploads[uploads[2]].read())
	else:
		optionList = request.form['entityrules']
		if optionList:
			if optionList == 'default':
				commoncharacters = ['&ae;', '&d;', '&t;', '&e;', '&AE;', '&D;', '&T;', '&#541;', '&#540;']
				# commoncharacters = [unicodedata.normalize('NFKD', i) for i in commoncharacters]
				commonunicode = [u'æ', u'ð', u'þ', u'ę', u'Æ', u'Ð', u'Þ', u'ȝ', u'Ȝ']
				
				r = make_replacer(dict(zip(commoncharacters, commonunicode)))
				text = r(text)

			elif optionList == 'doe-sgml':
				commoncharacters = ['&ae;', '&d;', '&t;', '&e;', '&AE;', '&D;', '&T;']
				# commoncharacters = [unicodedata.normalize('NFKD', i) for i in commoncharacters]
				commonunicode = [u'æ', u'ð', u'þ', u'ę', u'Æ', u'Ð', u'Þ']
				
				r = make_replacer(dict(zip(commoncharacters, commonunicode)))
				text = r(text)
				
			elif optionList == 'early-english-html':
				commoncharacters = ['&aelig;', '&eth;', '&thorn;', '&#541;', '&AElig;', '&ETH;', '&THORN;', '&#540;', '&#383;']
				# commoncharacters = [unicodedata.normalize('NFKD', i) for i in commoncharacters]
				commonunicode = [u'æ', u'ð', u'þ', u'ȝ', u'Æ', u'Ð', u'Þ', u'Ȝ', u'ſ']
				
				r = make_replacer(dict(zip(commoncharacters, commonunicode)))
				text = r(text)
				
	return text

def make_replacer(replacements):
	locator = re.compile('|'.join(re.escape(k) for k in replacements))

	def _doreplace(mo):
		return replacements[mo.group()]

	def replace(s):
		return locator.sub(_doreplace, s)

	return replace

def format_special(text,special_file):
	special_lines = special_file.split("\n")
	for special_line in special_lines:
		special_line = special_line.strip()
		specialList = special_line.split(', ')
		special = specialList.pop(0)

		for i, changeMe in enumerate(specialList):
			character = re.compile(changeMe)
			text = character.sub(special,text)
	return text

def handle_tags(text, keeptags, hastags, file_type):
	if hastags: #sgml or txt file, has tags that can be kept/discarded
		if file_type == "sgml":
			text =  re.sub("<s(.+?)>",'<s>', text)
			cleaned_text = re.findall(u'<s>(.+?)</s>',text)
			text = u''.join(cleaned_text)
			
			if keeptags:
				text = re.sub(u'<[^<]+?>', '', text)
			else:
				# does not work for same nested loops (i.e. <corr><corr>TEXT</corr></corr> )
				text = re.sub(ur'<(.+?)>(.+?)<\/\1>', u'', text)	

		if file_type == "txt":
			if keeptags:
				text = re.sub(u'<[^<]+?>', '', text)
			else:
				#does not work for same nested loops (i.e. <corr><corr>TEXT</corr></corr> )
				text = re.sub(ur'<(.+?)>(.+?)<\/\1>', u'', text)

	else: # no option to delete tags
		# html or xml file-- nuking all tags, keeping the rest of the text
		if file_type == "xml" or file_type == "html":
			matched = re.search(u'<[^<]+?>', text)
			while (matched):
				text = re.sub(u'<[^<]+?>', '', text)
				matched = re.search(u'<[^<]+?>', text)
		else: # file without tags
			pass

	return text

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

	return text



def scrubber(text, file_type, lower, punct, apos, hyphen, digits, hastags, keeptags, opt_uploads, cache_options):
	# originals    = u"ç,œ,á,é,í,ó,ú,à,è,ì,ò,ù,ä,ë,ï,ö,ü,ÿ,â,ê,î,ô,û,å,e,i,ø".split(',')
	# replacements = u"c,oe,a,e,i,o,u,a,e,i,o,u,a,e,i,o,u,y,a,e,i,o,u,a,e,i,o".split(',')
	# replace = dict(zip(originals,replacements))
	# for k, v in replace.iteritems():
	# 	text = text.replace(k, v)

	# print "\nboom1:", cache_options

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

	text = handle_specialcharacters(text, got_files, specialchars)

	text = handle_tags(text, keeptags, hastags, file_type)

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