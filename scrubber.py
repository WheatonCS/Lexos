# -*- coding: utf-8 -*-
import string, re, sys, unicodedata, os, pickle
from flask import Flask, request, session

def defaulthandle_specialcharacters(text):
	# originals    = u"ç,œ,á,é,í,ó,ú,à,è,ì,ò,ù,ä,ë,ï,ö,ü,ÿ,â,ê,î,ô,û,å,e,i,ø".split(',')
	# replacements = u"c,oe,a,e,i,o,u,a,e,i,o,u,a,e,i,o,u,y,a,e,i,o,u,a,e,i,o".split(',')
	# replace = dict(zip(originals,replacements))
	# for k, v in replace.iteritems():
	# 	text = text.replace(k, v)
	optionList = request.form['entityrules']
	if optionList:
		if optionList == 'default':
			commoncharacters = ['&ae;', '&d;', '&t;', '&e;', '&AE;', '&D;', '&T;', '&#541;', '&#540;']
			commonunicode = [u'æ', u'ð', u'þ', u'ę', u'Æ', u'Ð', u'Þ', u'ȝ', u'Ȝ']
			
			r = make_replacer(dict(zip(commoncharacters, commonunicode)))
			text = r(text)

		elif optionList == 'doe-sgml':
			commoncharacters = ['&ae;', '&d;', '&t;', '&e;', '&AE;', '&D;', '&T;']
			commonunicode = [u'æ', u'ð', u'þ', u'ę', u'Æ', u'Ð', u'Þ']
			
			r = make_replacer(dict(zip(commoncharacters, commonunicode)))
			text = r(text)
			
		elif optionList == 'early-english-html':
			commoncharacters = ['&aelig;', '&eth;', '&thorn;', '&yogh;', '&AElig;', '&ETH;', '&THORN;', '&YOGH;', '&#383;']
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

def replacementline_handler(text, replacer_string, is_lemma):
	replacer_string = re.sub(' ', '', replacer_string)
	replacementlines = replacer_string.split('\n')
	for replacementline in replacementlines:
		replacementline = replacementline.strip()

		if replacementline.find(':') == -1:
			lastComma = replacementline.rfind(',')
			replacementline = replacementline[:lastComma] + ':' + replacementline[lastComma+1:]

		elementList = replacementline.split(':')
		for i, element in enumerate(elementList):
			elementList[i] = element.split(',')

		if len(elementList[0]) == 1 and len(elementList[1]) == 1:
			replacer = elementList.pop()[0]
		elif len(elementList[0]) == 1: # Targetresult word is first
			replacer = elementList.pop(0)[0]
		elif len(elementList[1]) == 1: # Targetresult word is last
			replacer = elementList.pop()[0]
		else:
			print "Error in replacementline_handler formatting..." 
			print "Too many elements on either side of colon."
			return text

		elementList = elementList[0]

		if is_lemma:
			edge = r'\b'
		else:
			edge = ''

		for changeMe in elementList:
			theRegex = re.compile(edge + changeMe + edge)
			text = theRegex.sub(replacer, text)

	return text

def call_rlhandler(text, replacer_string, is_lemma, manualinputname, cache_folder, cache_filenames, cache_number):
	replacementline_string = ''
	if replacer_string and not request.form[manualinputname] != '': # filestrings[2] == special characters
		cache_filestring(replacer_string, cache_folder, cache_filenames[cache_number])
		replacementline_string = replacer_string
	elif not replacer_string and request.form[manualinputname] != '':
		replacementline_string = request.form[manualinputname]
	elif replacer_string and request.form[manualinputname] != '':
		replacementline_string = '\n'.join([replacer_string, request.form[manualinputname]])
	else:
		text = defaulthandle_specialcharacters(text)

	if replacementline_string != '':
		text = replacementline_handler(text, replacementline_string, is_lemma=is_lemma)

	return text

def handle_tags(text, keeptags, hastags, filetype, reloading=False):
	if hastags: #sgml or txt file, has tags that can be kept/discarded
		if filetype == "sgml":
			text =  re.sub("<s(.*?)>",'<s>', text)
			cleaned_text = re.findall(u'<s>(.+?)</s>',text)
			if reloading:
				text = '<s>' + u'</s><s>'.join(cleaned_text) + '</s>'
			else:
				text = u''.join(cleaned_text)
			
				if keeptags:
					text = re.sub(u'<[^<]+?>', '', text)
				else:
					# does not work for same nested loops (i.e. <corr><corr>TEXT</corr></corr> )
					text = re.sub(ur'<(.+?)>(.+?)<\/\1>', u'', text)

		if filetype == "txt":
			if keeptags:
				text = re.sub(u'<[^<]+?>', '', text)
			else:
				#does not work for same nested loops (i.e. <corr><corr>TEXT</corr></corr> )
				text = re.sub(ur'<(.+?)>(.+?)<\/\1>', u'', text)

	else: # no option to delete tags
		# html or xml file-- nuking all tags, keeping the rest of the text
		if filetype == "xml" or filetype == "html":
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

	# follow this sequence:
	# 1. make a remove_punctuation_map 
	# 2. see if "keep apostrophes" box is checked
	# 3.1 if so, keep all apostrophes
	# 3.2 if not, only replace cat's with cat井s, and delete all other cases (chris', 'this, 'single quotes')
	# 4. delete the according punctuations
	# 5. replace 井 with an apostrophe '

	punctuation_filename = "cache/punctuationmap.p"
	# Map of punctuation to be removed
	if os.path.exists(punctuation_filename):
		remove_punctuation_map = pickle.load(open(punctuation_filename, 'rb'))
	else:
		remove_punctuation_map = dict.fromkeys(i for i in xrange(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('P') or unicodedata.category(unichr(i)).startswith('S'))
		pickle.dump(remove_punctuation_map, open(punctuation_filename, 'wb'))

	# If keep apostrophes (UTF-16: 39) ticked
	if apos:
		# if keep apostrophes is checked, then we remove apos from the remove_punctuation_map (so keep all kinds of apos)
		del remove_punctuation_map[39]

		
	else:
		#When remove punctuation is checked, we remove all the apos but leave out the possessive/within-words(e.g.: I've) apos;

		# 1. make a substitution of "cat's" to "cat井s" (井 is a chinese character and it looks like #)
		text = re.sub(r"([A-Za-z])'([A-Za-z])",ur"\1井\2",text)
		# 2. but leave out all the other apostrophes, so don't delete apos from remove_punctuation_map

	# If keep hyphens (UTF-16: 45) ticked
	if hyphen:
		del remove_punctuation_map[45]

	# remove the according punctuations
	text = text.translate(remove_punctuation_map)

	# add back the apostrophe ' where it was substituted to a 井
	text = text.replace(u"井",'\'')

	return text



def remove_stopwords(text, removal_string):
	splitlines = removal_string.split("\n")
	word_list = []
	for line in splitlines:
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

def cache_filestring(file_string, cache_folder, filename):
	try:
		os.makedirs(cache_folder)
	except:
		pass
	pickle.dump(file_string, open(cache_folder + filename, 'wb'))

def load_cachedfilestring(cache_folder, filename):
	try:
		file_string = pickle.load(open(cache_folder + filename, 'rb'))
		return file_string
	except:
		return ""

def minimal_scrubber(text, hastags, keeptags, filetype):
	return handle_tags(text, keeptags, hastags, filetype, reloading=True)


def scrubber(text, filetype, lower, punct, apos, hyphen, digits, hastags, keeptags, opt_uploads, cache_options, cache_folder):

	cache_filenames = sorted(['stopwords.p', 'lemmas.p', 'consolidations.p', 'specialchars.p'])
	filestrings = {}

	for i, key in enumerate(sorted(opt_uploads)):
		if opt_uploads[key].filename != '':
			filestrings[i] = opt_uploads[key].read()
		else:
			filestrings[i] = ""
			if key.strip('[]') in cache_options:
				filestrings[i] = load_cachedfilestring(cache_folder, cache_filenames[i])
			else:
				session['scrubbingoptions']['optuploadnames'][key] = ''

	cons_filestring = filestrings[0]
	lem_filestring = filestrings[1]
	sc_filestring = filestrings[2]
	sw_filestring = filestrings[3]

	"""
	Scrubbing order:
	1. lower
	2. special characters
	3. tags
	4. punctuation
	5. digits
	6. consolidations
	7. lemmatize
	8. stopwords
	"""

	if lower:
		text = text.lower()

	text = call_rlhandler(text, 
				   sc_filestring, 
			  	   is_lemma=False, 
			  	   manualinputname='manualspecialchars', 
				   cache_folder=cache_folder,
			  	   cache_filenames=cache_filenames, 
			  	   cache_number=2)

	text = handle_tags(text, keeptags, hastags, filetype)

	if punct:
		text = remove_punctuation(text, apos, hyphen)

	if digits:
		text = re.sub("\d+", '', text)

	text = call_rlhandler(text, 
				   cons_filestring, 
				   is_lemma=False, 
				   manualinputname='manualconsolidations', 
				   cache_folder=cache_folder,
				   cache_filenames=cache_filenames, 
				   cache_number=0)

	text = call_rlhandler(text, 
				   lem_filestring, 
				   is_lemma=True, 
				   manualinputname='manuallemmas',
				   cache_folder=cache_folder,
				   cache_filenames=cache_filenames, 
				   cache_number=1)

	if sw_filestring: # filestrings[3] == stopwords
		cache_filestring(sw_filestring, cache_folder, cache_filenames[3])
		removal_string = '\n'.join([sw_filestring, request.form['manualstopwords']])
	else:
		removal_string = request.form['manualstopwords']
	text = remove_stopwords(text, removal_string)
	

	return text