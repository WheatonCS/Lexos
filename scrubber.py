#!/usr/bin/python
# -*- coding: utf-8 -*-
import string, re, sys, unicodedata, os, pickle
from flask import Flask, request, session

def defaulthandle_specialcharacters(text):
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

def replacementline_handler(text, upload_file, manualinputfield, is_lemma):
	mergedreplacements = upload_file + '\n' + request.form[manualinputfield]
	replacementlines = mergedreplacements.split("\n")
	print replacementlines
	for replacementline in replacementlines:
		replacementline = replacementline.strip()
		replacementlist = replacementline.split(',')
		replacementlist = [word.strip() for word in replacementlist]
		changeTo = replacementlist.pop(0)

		if is_lemma:
			edge = r'\b'
		else:
			edge = ''

		for changeMe in replacementlist:
			theRegex = re.compile(edge + changeMe + edge)
			text = theRegex.sub(changeTo, text)

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
		remove_punctuation_map = pickle.load(open(punctuation_filename, 'rb'))
	else:
		remove_punctuation_map = dict.fromkeys(i for i in xrange(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('P') or unicodedata.category(unichr(i)).startswith('S'))
		pickle.dump(remove_punctuation_map, open(punctuation_filename, 'wb'))

	# If keep apostrophes (UTF-16: 39) ticked
	if apos:
		del remove_punctuation_map[39]

	# If keep hyphens (UTF-16: 45) ticked
	if hyphen:
		del remove_punctuation_map[45]

	return text.translate(remove_punctuation_map)



def remove_stopwords(text, sw_file, manualinputfield):
	extendedinput = sw_file + " " + request.form[manualinputfield]
	extendedinput = extendedinput.split("\n")
	word_list = []
	for line in extendedinput:
		line = line.strip()
		# Using re for multiple delimiter splitting
		line = re.split('[, ]', line)
		word_list.extend(line)

	word_list = [word for word in word_list if word != '']

	# Create pattern
	remove = "|".join(word_list)
	# Compile pattern with bordering \b markers to demark only full words
	pattern = re.compile(r'\b(' + remove + r')\b')

	# Replace stopwords
	text = pattern.sub('', text)
	# Fill in extra spaces with 1 space
	text = re.sub(' +', ' ', text)

	return text

def cache_file(file_string, cache_folder, filename):
	try:
		os.makedirs(cache_folder)
	except:
		pass
	pickle.dump(file_string, open(cache_folder + filename, 'wb'))

def load_cachedfile(cache_folder, filename):
	try:
		file_string = pickle.load(open(cache_folder + filename, 'rb'))
		return file_string
	except:
		return ""

def scrubber(text, file_type, lower, punct, apos, hyphen, digits, hastags, keeptags, opt_uploads, cache_options, cache_folder):
	# originals    = u"ç,œ,á,é,í,ó,ú,à,è,ì,ò,ù,ä,ë,ï,ö,ü,ÿ,â,ê,î,ô,û,å,e,i,ø".split(',')
	# replacements = u"c,oe,a,e,i,o,u,a,e,i,o,u,a,e,i,o,u,y,a,e,i,o,u,a,e,i,o".split(',')
	# replace = dict(zip(originals,replacements))
	# for k, v in replace.iteritems():
	# 	text = text.replace(k, v)
	cache_filenames = sorted(['stopwords.p', 'lemmas.p', 'consolidations.p', 'specialchars.p'])
	files = {}

	for i, key in enumerate(sorted(opt_uploads)):
		if opt_uploads[key].filename != '':
			files[i] = opt_uploads[key].read()
		else:
			files[i] = ""
			if key.strip('[]') in cache_options:
				files[i] = load_cachedfile(cache_folder, cache_filenames[i])
			else:
				session['opt_uploads'][key] = ''
			if not files[i]:
				files[i] = False

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


	if files[2]: # files[2] == special characters
		sc_file = files[2]
		cache_file(sc_file, cache_folder, cache_filenames[2])
	else:
		sc_file = ""
		text = defaulthandle_specialcharacters(text)
	text = replacementline_handler(text, sc_file, 'manualspecialchars', is_lemma=False)


	text = handle_tags(text, keeptags, hastags, file_type)


	if punct:
		text = remove_punctuation(text, apos, hyphen)


	if digits:
		text = re.sub("\d+", '', text)


	if files[1]: # files[1] == lemmas
		lem_file = files[1]
		cache_file(lem_file, cache_folder, cache_filenames[1])
	else:
		lem_file = ""
	text = replacementline_handler(text, lem_file, 'manuallemmas', is_lemma=True)


	if files[0]: # files[0] == consolidations
		cons_file = files[0]
		cache_file(cons_file, cache_folder, cache_filenames[0])
	else:
		cons_file = ""
	text = replacementline_handler(text, cons_file, 'manualconsolidations', is_lemma=False)


	if files[3]: # files[3] == stopwords
		sw_file = files[3]
		cache_file(sw_file, cache_folder, cache_filenames[3])
	else:
		sw_file = ""
	text = remove_stopwords(text, sw_file, 'manualstopwords')
	
	return text