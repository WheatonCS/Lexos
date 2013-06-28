# -*- coding: utf-8 -*-
import string, re, sys, unicodedata, os, pickle
from flask import Flask, request, session

def defaulthandle_specialcharacters(text):
	"""
	Replaces common characters with their corresponding special unicode characters, depending
	on the options chosen by the user.

	Args:
		text: A unicode string representing the whole text that is being manipulated.

	Returns:
		A unicode string representing the whole text including special characters.
	"""
	# originals    = u"ç,œ,á,é,í,ó,ú,à,è,ì,ò,ù,ä,ë,ï,ö,ü,ÿ,â,ê,î,ô,û,å,e,i,ø".split(',')
	# replacements = u"c,oe,a,e,i,o,u,a,e,i,o,u,a,e,i,o,u,y,a,e,i,o,u,a,e,i,o".split(',')
	# replace = dict(zip(originals,replacements))
	# for k, v in replace.iteritems():
	# 	text = text.replace(k, v)
	optionList = request.form['entityrules']
	if optionList:
		if optionList == 'default':
			commoncharacters = ['&ae;', '&d;', '&t;', '&e;', '&AE;', '&D;', '&T;', '&#541;', '&#540;', '&E;', '&amp;', '&lt;', '&gt;']
			commonunicode =    [u'æ', u'ð', u'þ', u'ę', u'Æ', u'Ð', u'Þ', u'ȝ', u'Ȝ', u'Ę', u'&', u'<', u'>']
			
			r = make_replacer(dict(zip(commoncharacters, commonunicode)))
			text = r(text)

		elif optionList == 'doe-sgml':
			commoncharacters = ['&ae;', '&d;', '&t;', '&e;', '&AE;', '&D;', '&T;', '&E;', '&oe;', '&amp;', '&egrave;', '&eacute;', '&auml;', '&ouml;', '&uuml;', '&amacron;', '&cmacron;', '&emacron;', '&imacron;', '&nmacron;', '&omacron;', '&pmacron;', '&qmacron;', '&rmacron;', '&lt;', '&gt;', '&lbar;', '&tbar;', '&bbar;']
			commonunicode = [u'æ', u'ð', u'þ', u'ę', u'Æ', u'Ð', u'Þ', u'Ę', u'œ', u'⁊', u'è', u'é', u'ä', u'ö', u'ü', u'ā', u'c̄', u'ē', u'ī', u'n̄', u'ō', u'p̄', u'q̄', u'r̄', u'<', u'>', u'ł', u'ꝥ', u'ƀ']
			
			r = make_replacer(dict(zip(commoncharacters, commonunicode)))
			text = r(text)
			
		elif optionList == 'early-english-html':
			commoncharacters = ['&aelig;', '&eth;', '&thorn;', '&yogh;', '&AElig;', '&ETH;', '&THORN;', '&YOGH;', '&#383;']
			commonunicode = [u'æ', u'ð', u'þ', u'ȝ', u'Æ', u'Ð', u'Þ', u'Ȝ', u'ſ']
			
			r = make_replacer(dict(zip(commoncharacters, commonunicode)))
			text = r(text)
				
	return text

def make_replacer(replacements):
	"""
	Creates a function (to be called later) that alters a text according to the replacements dictionary.

	Args:
		replacements: A dictionary where the keys are the strings of common characters and the
					  values are the unicode characters that the common characters stand for.

	Returns:
		The replace function that actually does the replacing.
	"""
	locator = re.compile('|'.join(re.escape(k) for k in replacements))

	def _doreplace(mo):
		return replacements[mo.group()]

	def replace(s):
		return locator.sub(_doreplace, s)

	return replace

def replacement_handler(text, replacer_string, is_lemma):
	"""
	Handles replacement lines found in the optional uploaded files 
	(for lemmas, consolidations, and special characters).

	Args:
		text: A unicode string representing the whole text that is being manipulated.
		replacer_string: A string representing what to the user wants to replace and what 
						 the user wants to replace it with (from BOTH manual input and the 
						 uploaded file).
		is_lemma: A boolean indicating whether or not the replacement line is for a lemma.

	Returns:
		A string representing the text after the replacements have taken place. 
	"""
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

def call_replacement_handler(text, replacer_string, is_lemma, manualinputname, cache_folder, cache_filenames, cache_number):
	"""
	Performs pre-processing before calling replacement_handler().

	Args:
		text: A unicode string representing the whole text that is being manipulated.
		replacer_string: A string representing what to the user wants to replace and what 
						 the user wants to replace it with (from ONLY the uploaded file).
		is_lemma: A boolean indicating whether or not the replacement line is for a lemma.
		manualinputname: A string representing the manual input field in scrub.html.
		cache_folder: A string representing the path to the cache folder.
		cache_filenames: A list of the cached filenames.
		cache_number: An integer representing the position (index) of a file in cache_filenames

	Returns:
		A string representing the text after the replacements have taken place.
	"""
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
		text = replacement_handler(text, replacementline_string, is_lemma=is_lemma)

	return text

def handle_tags(text, keeptags, tags, filetype, previewing=False):
	"""
	Handles tags that are found in the text. Useless tags (header tags) are deleted and 
	depending on the specifications chosen by the user, words between meaninful tags (corr, foreign)
	are either kept or deleted.

	Args:
		text: A unicode string representing the whole text that is being manipulated.
		keeptags: A boolean indicating whether or not tags are kept in the texts.
		tags:  A boolean indicating whether or not the text contains tags.
		filetype: A string representing the type of the file being manipulated.
		previewing: A boolean indicating whether or not the user is previewing.

	Returns:
		A unicode string representing the text where tags have been manipulated depending on
		the options chosen by the user.
	"""
	if filetype == 'doe': #dictionary of old english, option to keep/discard tags (corr/foreign).
		text =  re.sub("<s(.*?)>",'<s>', text)
		s_tags = re.search('<s>',text)
		if s_tags != None:
			cleaned_text = re.findall(u'<s>(.+?)</s>',text)
			if previewing:
				text = u'</s><s>'.join(cleaned_text)
				text = '<s>' + text + '</s>'
			else:
				text = u''.join(cleaned_text)
			
		if keeptags:
			text = re.sub(u'<[^<]+?>', '', text)
		else:
			# does not work for same nested loops (i.e. <corr><corr>TEXT</corr></corr> )
			text = re.sub(ur'<(.+?)>(.+?)<\/\1>', u'', text)

	elif tags: #tagbox is checked to remove tags
		matched = re.search(u'<[^<]+?>', text)
		while (matched):
			text = re.sub(u'<[^<]+?>', '', text)
			matched = re.search(u'<[^<]+?>', text)

	else: # keeping tags
		pass

	return text

def remove_punctuation(text, apos, hyphen):
	"""
	Removes punctuation from the text files.

	Args:
		text: A unicode string representing the whole text that is being manipulated.
		apos: A boolean indicating whether or not apostrophes are kept in the text.
		hyphen: A boolean indicating whether or not hyphens are kept in the text.

	Returns:
		A unicode string representing the text that has been stripped of punctuation, and
		manipulated depending on the options chosen by the user.
	"""
	# Translating all hyphens to one type

	# All UTF-16 values for different hyphens: for translating
	hyphen_values       = [8208,8211,8212,8213,8315,8331,65123,65293,56128,56365]
	chosen_hyphen_value = 45 # 45 corresponds to the hyphen-minus symbol

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
	"""
	Removes stopwords from the text.

	Args:
		text: A unicode string representing the whole text that is being manipulated.
		removal_string: A unicode string representing the list of stopwords.
	Returns:
		A unicode string representing the text that has been stripped of the stopwords chosen
		by the user.
	"""
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
	"""
	Caches a file string into the cache folder.

	Args:
		file_string: A string that is being cached in the cache folder.
		cache_folder: A string representing the path of the cache folder.
		filename: A string representing the name of the file that is being loaded.

	Returns:
		None
	"""
	try:
		os.makedirs(cache_folder)
	except:
		pass
	pickle.dump(file_string, open(cache_folder + filename, 'wb'))

def load_cachedfilestring(cache_folder, filename):
	"""
	Loads the file string that has been previously cached in the cache folder.

	Args:
		cache_folder: A string representing the path of the cache folder.
		filename: A string representing the name of the file that is being loaded.

	Returns:
		The file string that loaded from the cache folder 
		(returns an empty string if there is no string to load).
	"""
	try:
		file_string = pickle.load(open(cache_folder + filename, 'rb'))
		return file_string
	except:
		return ""

def minimal_scrubber(text, tags, keeptags, filetype):
	"""
	Calls handle_tags() during a preview reload (previewing == True).

	Args:
		text: A unicode string representing the whole text that is being manipulated.
		tags:  A boolean indicating whether or not the text contains tags.
		keeptags: A boolean indicating whether or not tags are kept in the texts.
		filetype: A string representing the type of the file being manipulated.

	Returns:
		Returns handle_tags(), returning the text where tags have been manipulated depending on
		the options chosen by the user. 
	"""
	return handle_tags(text, keeptags, tags, filetype, previewing=True)


def scrubber(text, filetype, lower, punct, apos, hyphen, digits, tags, keeptags, opt_uploads, cache_options, cache_folder):
	"""
	Completely scrubs the text according to the specifications chosen by the user. It calls call_rlhandler, 
	handle_tags(), remove_punctuation(), and remove_stopwords() to manipulate the text.

	*Called in call_scrubber() in the helpful functions section in lexos.py.

	Args:
		text: A unicode string representing the whole text that is being manipulated.
		filetype: A string representing the type of the file being manipulated.
		lower: A boolean indicating whether or not the text is converted to lowercase.
		punct: A boolean indicating whether or not punctuation is removed from the text.
		apos: A boolean indicating whether or not apostrophes are kept in the text.
		hyphen: A boolean indicating whether or not hyphens are kept in the text.
		digits: A boolean indicating whether or not digits are removed from the text.
		tags: A boolean indicating whether or not the text contains tags.
		keeptags: A boolean indicating whether or not tags are kept in the texts.
		opt_uploads: A dictionary containing the optional files that have been uploaded for additional scrubbing.
		cache_options: A list of the additional options that have been chosen by the user.
		cache_folder: A string representing the path of the cache folder.

	Returns:
		A string representing the completely scrubbed text after all of its manipulation.
	"""
	cache_filenames = sorted(['stopwords.p', 'lemmas.p', 'consolidations.p', 'specialchars.p'])
	filestrings = {}

	for i, key in enumerate(sorted(opt_uploads)):
		if opt_uploads[key].filename != '':
			filestrings[i] = opt_uploads[key].read().decode('utf-8')
			opt_uploads[key].seek(0)
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
		cons_filestring = cons_filestring.lower()
		lem_filestring = lem_filestring.lower()
		sc_filestring = sc_filestring.lower()
		sw_filestring = sw_filestring.lower()

	text = call_replacement_handler(text=text, 
						  replacer_string=sc_filestring, 
						  is_lemma=False, 
						  manualinputname='manualspecialchars', 
						  cache_folder=cache_folder,
						  cache_filenames=cache_filenames, 
						  cache_number=2)

	text = handle_tags(text, keeptags, tags, filetype)

	if punct:
		text = remove_punctuation(text, apos, hyphen)

	if digits:
		text = re.sub("\d+", '', text)

	text = call_replacement_handler(text=text, 
						  replacer_string=cons_filestring, 
						  is_lemma=False, 
						  manualinputname='manualconsolidations', 
						  cache_folder=cache_folder,
						  cache_filenames=cache_filenames, 
						  cache_number=0)

	text = call_replacement_handler(text=text, 
						  replacer_string=lem_filestring, 
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