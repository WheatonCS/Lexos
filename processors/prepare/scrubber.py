# -*- coding: utf-8 -*-
import re
import sys
import unicodedata
import os
import pickle
import debug.log as debug
import helpers.constants as constants

from flask import request, session
import codecs


def handle_specialcharacters(text):
    """
    Replaces encoded characters (common_characters) with their corresponding unicode characters (common_unicode),
    based on options chosen by the user.

    Args:
        text: The text to be altered.

    Returns:
        The altered unicode string.
    """
    optionlist = request.form['entityrules']

    if optionlist in ('doe-sgml', 'early-english-html', 'MUFI-3', 'MUFI-4'):
        if optionlist == 'doe-sgml':
            common_characters = ['&ae;', '&d;', '&t;', '&e;', '&AE;', '&D;', '&T;', '&E;', '&oe;', '&amp;', '&egrave;',
                                 '&eacute;', '&auml;', '&ouml;', '&uuml;', '&amacron;', '&cmacron;', '&emacron;',
                                 '&imacron;', '&nmacron;', '&omacron;', '&pmacron;', '&qmacron;', '&rmacron;', '&lt;',
                                 '&gt;', '&lbar;', '&tbar;', '&bbar;']
            common_unicode = [u'æ', u'ð', u'þ', u'ę', u'Æ', u'Ð', u'Þ', u'Ę', u'œ', u'⁊', u'è', u'é', u'ä', u'ö',
                              u'ü',
                              u'ā', u'c̄', u'ē', u'ī', u'n̄', u'ō', u'p̄', u'q̄', u'r̄', u'<', u'>', u'ł', u'ꝥ',
                              u'ƀ']


        elif optionlist == 'early-english-html':
            common_characters = ['&ae;', '&d;', '&t;', '&e;', '&AE;', '&D;', '&T;', '&#541;', '&#540;', '&E;', '&amp;',
                                 '&lt;', '&gt;', '&#383;']
            common_unicode = [u'æ', u'ð', u'þ', u'\u0119', u'Æ', u'Ð', u'Þ', u'ȝ', u'Ȝ', u'Ę', u'&', u'<', u'>', u'ſ']

        elif optionlist == 'MUFI-3':
            cur_file_dir = os.path.dirname(os.path.abspath(__file__))   # assign current working path to variable

            # Go up two levels (2x break path name into two parts, where
            # cur_file_dir path is everything but the last component)
            cur_file_dir, discard = os.path.split(cur_file_dir)     # discard: tail of path to be removed
            cur_file_dir, discard = os.path.split(cur_file_dir)

            # Create full pathname to find MUFI_3_DICT.tsv in resources directory
            mufi3path = os.path.join(cur_file_dir, constants.RESOURCE_DIR, constants.MUFI_3_FILENAME)

            common_characters = []
            common_unicode = []
            Dict = {}
            with codecs.open(mufi3path, encoding='utf-8') as MUFI_3:

                for line in MUFI_3:
                    pieces = line.split('\t')   # divide columns of .tsv file into two separate arrays
                    key = pieces[0].rstrip()
                    value = pieces[1].rstrip()
                    Dict[key] = value

                # Assign values to the dictionary corresponding with values in pieces arrays
                for key, value in Dict.items():
                    common_characters.append(value)
                    common_unicode.append(key)


        elif optionlist == 'MUFI-4':

            cur_file_dir = os.path.dirname(os.path.abspath(__file__))  # assign current working path to variable

            # Go up two levels (2x break path name into two parts, where
            # cur_file_dir path is everything but the last component)
            cur_file_dir, discard = os.path.split(cur_file_dir)  # discard: tail of path to be removed
            cur_file_dir, discard = os.path.split(cur_file_dir)

            # Create full pathname to find MUFI_4_DICT.tsv in resources directory
            mufi4path = os.path.join(cur_file_dir, constants.RESOURCE_DIR, constants.MUFI_3_FILENAME)

            common_characters = []
            common_unicode = []
            Dict = {}
            with codecs.open(mufi4path, encoding='utf-8') as MUFI_4:

                for line in MUFI_4:
                    pieces = line.split('\t')   # divide columns of .tsv file into two separate arrays
                    key = pieces[0].rstrip()
                    value = pieces[1].rstrip()
                    Dict[key] = value

                # Assign values to the dictionary corresponding with values in pieces arrays
                for key, value in Dict.items():
                    common_characters.append(value)
                    common_unicode.append(key)

        # now we've set the common_characters and common_unicode based on the special chars used
        r = make_replacer(dict(zip(common_characters, common_unicode)))
        #print "Made it this far"
        # r is a function created by the below functions
        text = r(text)
    return text


def make_replacer(replacements):
    """
    Creates a function (to be called later) that alters a text according to the replacements dictionary.

    Args:
        replacements: A dictionary where the keys are the strings of encoded ascii characters and the
                      values are the encoded unicode characters.

    Returns:
        The replace function that actually does the replacing.
    """
    #for k in replacements:
        #print k
   # l = (ru'|'.join(re.escape(k))
    #print l

    #print locator.decode("UTF-8")
    #small_replacements = replacements[0:10]

    locator = re.compile('|'.join(re.escape(k) for k in replacements), re.UNICODE)


    def _doreplace(mo):
        """
        Creates a function to return an object according to the replacements dictionary.

        Args:
            mo: A replacement character

        Returns:
            The object contains the replacement character
        """
        #print mo.group()
        # ------Delete this---------
        #if (isinstance(mo.group(), unicode)):
           # print "we've got uni"
        # ------Delete this---------

        return replacements[mo.group()]


    def replace(s):
        """
        Creates a function to return a replaced text according to the replacements dictionary.

        Args:
            s: A string contains the file contents

        Returns:
            The replaced text
        """
        #print "file contents: \n", s
        return locator.sub(_doreplace, s)
        #re.sub(locator, _doreplace, s)


    return replace


def replacement_handler(text, replacer_string, is_lemma):
    """
    Handles replacement lines found in the scrub-alteration-upload files.

    Args:
        text: A unicode string with the whole text to be altered.
        replacer_string: A formatted string input with newline-separated "replacement lines", where
            each line is formatted to replace the majority of the words with one word.
        is_lemma: A boolean indicating whether or not the replacement line is for a lemma.

    Returns:
        The replace function that actually does the replacing.
    """
    replacer_string = re.sub(' ', '', replacer_string)
    replacementlines = replacer_string.split('\n')
    for replacementline in replacementlines:
        replacementline = replacementline.strip()

        if replacementline.find(':') == -1:
            lastComma = replacementline.rfind(',')
            replacementline = replacementline[:lastComma] + ':' + replacementline[lastComma + 1:]

        elementList = replacementline.split(':')
        for i, element in enumerate(elementList):
            elementList[i] = element.split(',')

        if len(elementList[0]) == 1 and len(elementList[1]) == 1:
            replacer = elementList.pop()[0]
        elif len(elementList[0]) == 1:  # Targetresult word is first
            replacer = elementList.pop(0)[0]
        elif len(elementList[1]) == 1:  # Targetresult word is last
            replacer = elementList.pop()[0]
        else:
            return text

        elementList = elementList[0]

        if is_lemma:
            edge = r'\b'
        else:
            edge = ''

        for changeMe in elementList:
            theRegex = re.compile(edge + changeMe + edge, re.UNICODE)
            text = theRegex.sub(replacer, text)

    return text


def call_replacement_handler(text, replacer_string, is_lemma, manualinputname, cache_folder, cache_filenames,
                             cache_number):
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
    if replacer_string and not request.form[manualinputname] != '':  # filestrings[2] == special characters
        cache_filestring(replacer_string, cache_folder,
                         cache_filenames[cache_number])  # call cache_filestring to cache a file string
        replacementline_string = replacer_string
    elif not replacer_string and request.form[manualinputname] != '':
        replacementline_string = request.form[manualinputname]
    elif replacer_string and request.form[manualinputname] != '':
        replacementline_string = '\n'.join([replacer_string, request.form[manualinputname]])
    else:
        text = handle_specialcharacters(text)

    if replacementline_string != '':
        text = replacement_handler(text, replacementline_string, is_lemma=is_lemma)

    return text


def handle_tags(text, keeptags, tags, filetype, previewing=False):
    """
    Handles tags that are found in the text. Useless tags (header tags) are deleted and
    depending on the specifications chosen by the user, words between meaningful tags (corr, foreign)
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

    if filetype == 'doe':  # dictionary of old english, option to keep/discard tags (corr/foreign).
        # <s(.*?)>: Lazily match any number of characters between <s and >
        text = re.sub("<s(.*?)>", '<s>', text)
        s_tags = re.search('<s>', text)
        if s_tags is not None:
            # <s>(.+?)</s>: Lazily matches one or more characters between <s> and </s>
            cleaned_text = re.findall(u'<s>(.+?)</s>', text)
            if previewing:
                text = u'</s><s>'.join(cleaned_text)
                text = '<s>' + text + '</s>'
            else:
                text = u''.join(cleaned_text)

        if keeptags:
            # <[^<]+?>; Lazily matches a single character, except <, one or more times between < and >
            text = re.sub(u'<[^<]+?>', '', text)
        else:
            # does not work for some nested loops (i.e. <corr><corr>TEXT</corr></corr> )
            pattern = re.compile(ur"""
                <        # matches the character < literally
                (.+?)    # first capturing group lazily matches any character (except
                         # newline) one or more times
                >        # matches the character > literally
                (.+?)    # first capturing group lazily matches any character (except
                         # newline) one or more times
                <        # matches the character < literally
                \/       # matches the character / literally
                \1       # matches the same text as most recently matched by the first
                         # capturing group
                >        # matches the character > literally
            """, re.VERBOSE)
            text = re.sub(pattern, u'', text)

    #elif tags:
    else:

        # Any XML or HTML file goes through here
        # For regex documentation, see https://github.com/WheatonCS/Lexos/issues/295
        pattern ="""
            <           # Match opening of tag
            (?:         # First Alternative:
            [A-Za-z_:]  # Match alphabetic characters literally
            [\w:.-]*    # Greedily match a single word character between zero
                        # and unlimited times, literally

            (?=\s)      # Positive Lookahead - Assert that any white space
                        # character can be matched
            (?!         # Negative Lookahead - Assert that it is impossible to
                        # match the regex below
            (?:         # First alternative:
            [^>" \']    # Match a single character literally that is not >
            |           # Or second alternative
            "[^"]*"     # Greedily match a single character literally that is
                        # not " between zero and unlimited times
            |           # Or third alternative
            \'[^\']*\'  # Greedily match a single character literally that is
                        # not \ between zero and unlimited times
            )*?         # Execute the negative look ahead lazily between zero
                        # and unlimited times
            (?<=\s)\s*=)# Positive Lookbehind - Assert that any white space
                        # or = can be matched greedily between zero and
                        # unlimited times, preceded by <
            (?!\s*/?>)  # Negative Lookahead - Assert that it is impossible to
                        # match greedily white space between zero and
                        # unlimited times or / between zero and one time
                        # followed by >
            \s          # Greedily match any white space character between one
                        # and unlimited times
            (?:         # First alternative:
            ".*?"       # Lazily match " followed by between zero and
              \/          # unlimited characters, followed by "
            |           # Or second alternative
            \'.*?\'     # Lazily match ' followed by between zero and
                        # unlimited characters, followed by ''
            |           # Or third alternative
            [^>]*?)     # Lazily match any single character not > between
                        # zero and unlimited times
            +|          # Begin Second Alternative:
            /?          # Greedily match / literally between zero and one
                        # time...
            [A-Za-z_:]  # ...followed by one or more alphabetic characters...
            [\w:.-]*    # ...and one or more word characters, colons, dots or
                        # hyphens...
            \s*         # ...and any white space between zero and unlimited
                        # times
            /?)         # Greedily match / between zero and one times
            >           # Match closing of tag
            """
        text = re.sub(u'[\t ]+', " ", text, re.UNICODE)  # Remove extra white space
        text = re.sub("(<\?.*?>)", "", text)  # Remove xml declarations
        text = re.sub("(<\!--.*?-->)", "", text)  # Remove comments
        text = re.sub("(<\!DOCTYPE.*?>)", "", text)  # Remove DOCTYPE declarations
        if 'xmlhandlingoptions' in session:     #Should always be true
            for tag in session['xmlhandlingoptions']:
                action = session['xmlhandlingoptions'][tag]["action"]
                if action == "remove-tag":
                    pattern = re.compile(u'<(?:'+tag+'(?=\s)(?!(?:[^>"\']|"[^"]*"|\'[^\']*\')*?(?<=\s)\s*=)(?!\s*/?>)\s+(?:".*?"|\'.*?\'|[^>]*?)+|/?'+tag+'\s*/?)>',re.MULTILINE|re.DOTALL)
                    m = re.findall(pattern, text)
                    m = list(set(m))  # unique values take less time
                    for st in m:
                        #st may have regex characters, re.escape(st) will backslash all characters in st
                        text = re.sub(re.escape(st), " ", text,re.UNICODE)

                    text = re.sub(u'[\t ]+', " ", text, re.UNICODE)  # Remove extra white space

                elif action == "replace-element":
                    attribute = session['xmlhandlingoptions'][tag]["attribute"]
                    pattern = re.compile("<\s*"+tag+".*?>.+?<\/\s*"+tag+".*?>", re.MULTILINE | re.DOTALL)
                    text = re.sub(pattern, attribute, text)


                elif action == "remove-element":
                    text = re.sub("<\s*"+tag+".*?>.+?<\/?\s*"+tag+".*?>", "", text)

                else:
                    pass #Leave Tag Alone

    return text


def remove_punctuation(text, apos, hyphen, amper, tags, previewing):

    """
    Removes punctuation from the text files.

    Args:
        text: A unicode string representing the whole text that is being manipulated.
        apos: A boolean indicating whether or not apostrophes are kept in the text.
        hyphen: A boolean indicating whether or not hyphens are kept in the text.
        amper: A boolean indicating whether or not ampersands are kept in the text.
        tags: A boolean indicating whether or not the text contains tags.
        previewing: A boolean indicating whether or not the user is previewing.

    Returns:
        A unicode string representing the text that has been stripped of punctuation, and
        manipulated depending on the options chosen by the user.
    """

    # follow this sequence:
    # 1. make (or load) a remove_punctuation_map
    # 2. if "keep apostrophes" box is checked
    # 3  remove all apostrophes (single quotes) except: possessives (joe's), contractions (i'll), plural possessive (students')
    # 4. delete the rest of the punctuations

    punctuation_filename = os.path.join(constants.UPLOAD_FOLDER, "cache/punctuationmap.p")  # Localhost path (relative)


    # Map of punctuation to be removed
    if os.path.exists(punctuation_filename):
        remove_punctuation_map = pickle.load(open(punctuation_filename, 'rb'))
    else:
        # Creates map of punctuation to be removed if it doesn't already exist
        remove_punctuation_map = dict.fromkeys(i for i in xrange(sys.maxunicode) if
                                               unicodedata.category(unichr(i)).startswith('P') or unicodedata.category(
                                                   unichr(i)).startswith('S'))

        try:
            cache_path = os.path.dirname(punctuation_filename)
            os.makedirs(cache_path)
        except:
            pass
        pickle.dump(remove_punctuation_map, open(punctuation_filename, 'wb'))  # Cache

    # If Keep Word-Internal Apostrophes (UTF-8: 39) ticked
    #       (Remove must also be ticked in order for this option to appear)
    if apos:
        pattern = re.compile(ur"""
            (?<=[\w])'+(?=[^\w])     #If apos preceded by any word character and followed by non-word character
            |
            (?<=[^\w])'+(?=[\w])     #If apos preceded by non-word character and followed by any word character
            |
            (?<=[^\w])'+(?=[^\w])    #If apos surrounded by non-word characters
        """, re.VERBOSE | re.UNICODE)

        # replace all external or floating apos with empty strings
        text = unicode(re.sub(pattern, r"", text))

        # apos is removed from the remove_punctuation_map
        del remove_punctuation_map[39]  # apostrophe is removed from map

    if 'xmlhandlingoptions' in session:
        # if (keeping tags) remove '<' and '>' from the punctuation map.
        del remove_punctuation_map[60]
        del remove_punctuation_map[62]

    if previewing:
        del remove_punctuation_map[8230]

    # If keep hyphens (UTF-16: 45) ticked
    if hyphen:
        # All UTF-8 values (hex) for different hyphens: for translating
        # All unicode dashes have 'Pd'

        # as of -5/26/2015, we removed the math (minus) symbols from this list
        # as of 5/31/2016, all the dashes were added to this list
        hyphen_values = [u'\u058A', u'\u05BE', u'\u2010', u'\u2011', u'\u2012', u'\u2013', u'\u2014', u'\u2015',
                         u'\uFE58', u'\uFE63', u'\uFF0D', u'\u1400', u'\u1806', u'\u2E17', u'\u2E1A', u'\u2E3A',
                         u'\u2E3B',
                         u'\u2E40', u'\u301C', u'\u3030', u'\u30A0', u'\uFE31', u'\uFE32']

        # All UTF-8 values (decimal) for different hyphens: for translating
        # hyphen_values       = [8208, 8211, 8212, 8213, 8315, 8331, 65123, 65293, 56128, 56365]

        chosen_hyphen_value = u'\u002D'  # 002D corresponds to the hyphen-minus symbol

        # convert all those types of hyphens into the ascii hyphen (decimal 45, hex 2D)
        for value in hyphen_values:
            text = text.replace(value, chosen_hyphen_value)
        # now that all those hypens are the ascii hyphen (hex 002D), remove hyphens from the map
        del remove_punctuation_map[45]  # now no hyphens will be deleted from the text

    if amper:   # If keeping ampersands

        amper_values = [u"\uFF06", u"\u214B", u"\U0001F674", u"\uFE60", u"\u0026", u"\U0001F675", u"\u06FD",
                        u"\U000E0026"]

        chosen_amper_value = u"\u0026"

        for value in amper_values:      # Change all ampersands to one type of ampersand
            text = text.replace(value, chosen_amper_value)

        del remove_punctuation_map[38]      # Remove chosen ampersand from remove_punctuation_map

    # now remove all punctuation symbols still in the map
    text = text.translate(remove_punctuation_map)

    return text


def remove_digits(text, previewing):
    """
    Removes digits from the text.

    Args:
		text: A unicode string representing the whole text that is being manipulated.
    Returns:
		A unicode string representing the text that has been stripped of all digits.
    """
    #Why is previewing being passed?
    digit_filename = os.path.join(constants.UPLOAD_FOLDER, "cache/digitmap.p")  # Localhost path (relative)

    if os.path.exists(digit_filename):  # if digit map has already been generated
        remove_digit_map = pickle.load(open(digit_filename, 'rb'))  # open the digit map for further use
    else:
        remove_digit_map = dict.fromkeys(
            i for i in xrange(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('N'))
        # else generate the digit map with all unicode characters that start with the category 'N'
        # see http://www.fileformat.info/info/unicode/category/index.htm for reference of categories
    try:
        cache_path = os.path.dirname(digit_filename)  # try making a directory for cacheing if it doesn't exist
        os.makedirs(cache_path)  # make a directory with cache_path as input
    except:
        pass
    pickle.dump(remove_digit_map, open(digit_filename, 'wb'))  # cache the digit map

    text = text.translate(remove_digit_map)  # remove all unicode digits from text

    return text


def get_punctuation_string():

    punctuation_filename = os.path.join(constants.UPLOAD_FOLDER, "cache/punctuationmap.p")  # Localhost path (relative)

    # Map of punctuation to be removed
    if os.path.exists(punctuation_filename):
        remove_punctuation_map = pickle.load(open(punctuation_filename, 'rb'))
    else:

        remove_punctuation_map = dict.fromkeys(i for i in xrange(sys.maxunicode) if
                                               unicodedata.category(unichr(i)).startswith('P') or unicodedata.category(
                                                   unichr(i)).startswith('S'))
    try:
        cache_path = os.path.dirname(punctuation_filename)
        os.makedirs(cache_path)
    except:
        pass
    pickle.dump(remove_punctuation_map, open(punctuation_filename, 'wb'))  # Cache

    punctuation = "["
    for key in remove_punctuation_map:
        punctuation += unichr(key)
    punctuation += " ]"
    return punctuation


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
    remove_list = []
    for line in splitlines:
        line = line.strip()
        # Using re for multiple delimiter splitting
        line = re.split('[,. ]', line)
        remove_list.extend(line)

    remove_list = [word for word in remove_list if word != '']

    # Create pattern
    remove_string = "|".join(remove_list)
    # Compile pattern with bordering \b markers to demark only full words
    pattern = re.compile(ur'\b(' + remove_string + ur')\b', re.UNICODE)
    #debug.show(pattern)
    #print "text:", text
    # Replace stopwords
    text = pattern.sub('', text)

    # Fill in extra spaces with 1 space
    text = re.sub(' +', ' ', text)
    #print "remove_list:", remove_list
    #print "remove_string: ", remove_string
    #print "text:", text
    return text


def keep_words(text, non_removal_string):
    """
    Removes words that are not in non_removal_string from the text.
    Args:
        text: A unicode string representing the whole text that is being manipulated.
        non_removal_string: A unicode string representing the list of keep word.
    Returns:
        A unicode string representing the text that has been stripped of everything but
        the words chosen by the user.
    """
    punctuation = get_punctuation_string()
    splitlines = non_removal_string.split("\n")
    keep_list = []
    for line in splitlines:
        line = line.strip()
        # Using re for multiple delimiter splitting
        line = re.split('[., ]', line)  # maybe change '[., ]' for punctuation
        keep_list.extend(line)

    splitlines = text.split("\n")
    keep_list = [word for word in keep_list if word != '']

    text_list = []  # list containing all words in text
    for line in splitlines:
        line = line.strip()
        # Using re for multiple delimiter splitting
        line = re.split(punctuation, line)
        text_list.extend(line)
    text_list = [word for word in text_list if word != '']

    remove_list = [word for word in text_list if word not in keep_list]

    # Create pattern
    remove_string = "|".join(remove_list)
    # Compile pattern with bordering \b markers to demark only full words
    pattern = re.compile(ur'\b(' + remove_string + ur')\b', re.UNICODE)

    #debug.show(pattern)
    #print "test_list:", text_list
    #print "keep_list", keep_list
    #print "remove_list", remove_list
    #print "remove_string:", remove_string

    # Replace stopwords
    text = re.sub(pattern, '', text)

    # Fill in extra spaces with 1 space
    text = re.sub(' +', ' ', text)
    #print "text: ", text
    return text

def remove_whiteSpace(text, spaces, tabs, newLines, previewing):
    """
    Removes white spaces from the text.

    Args:
        text: A unicode string representing the whole text that is being manipulated.
        spaces: A boolean indicating whether or not spaces should be removed.
        tabs: A boolean indicating whether or not tabs should be removed.
        newLines: A boolean indicating whether or not new lines should be removed.

    Returns:
        A unicode string representing the text that has been stripped of all types of selected white spaces.
    """

    # removes spaces
    if spaces:
        text = re.sub(ur' ', '', text)
    # removes tags
    if tabs:
        text = re.sub(ur'\t', '', text)
    # removes new lines
    if newLines:
        text = re.sub(ur'\n', '', text)

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
"""
def minimal_scrubber(text, tags, keeptags, filetype):

    Calls handle_tags() during a preview reload (previewing == True).

    Args:
        text: A unicode string representing the whole text that is being manipulated.
        tags:  A boolean indicating whether or not the text contains tags.
        keeptags: A boolean indicating whether or not tags are kept in the texts.
        filetype: A string representing the type of the file being manipulated.

    Returns:
        Returns handle_tags(), returning the text where tags have been manipulated depending on
        the options chosen by the user.

    print "error in scrubber.py"
    return handle_tags(text, keeptags, tags, filetype, previewing=True)
"""

def scrub(text, filetype, gutenberg, lower, punct, apos, hyphen, amper, digits, tags, keeptags, whiteSpace, spaces, tabs, newLines, opt_uploads, cache_options,
          cache_folder, previewing=False):
    """
    Completely scrubs the text according to the specifications chosen by the user. It calls call_rlhandler,
    handle_tags(), remove_punctuation(), and remove_stopwords() to manipulate the text.

    *Called in call_scrubber() in the helpful functions section in lexos.py.

    Args:
        text: A unicode string representing the whole text that is being manipulated.
        filetype: A string representing the type of the file being manipulated.
        gutenberg: A boolean indicating whether the text is a Project Gutenberg file.
        lower: A boolean indicating whether or not the text is converted to lowercase.
        punct: A boolean indicating whether or not punctuation is removed from the text.
        apos: A boolean indicating whether or not apostrophes are kept in the text.
        hyphen: A boolean indicating whether or not hyphens are kept in the text.
        amper: A boolean indicating whether of not ampersands are kept in the text
        digits: A boolean indicating whether or not digits are removed from the text.
        tags: A boolean indicating whether or not the text contains tags.
        keeptags: A boolean indicating whether or not tags are kept in the texts.   #seems to always be false
        whiteSpace: A boolean indicating whether or not white spaces should be removed.
        spaces: A boolean indicating whether or not spaces should be removed.
        tabs: A boolean indicating whether or not tabs should be removed.
        newLines: A boolean indicating whether or not new lines should be removed.
        opt_uploads: A dictionary containing the optional files that have been uploaded for additional scrubbing.
        cache_options: A list of the additional options that have been chosen by the user.
        cache_folder: A string representing the path of the cache folder.
        previewing: A boolean indicating whether or not the user is previewing.

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
    sw_kw_filestring = filestrings[3]

    """
    Scrubbing order:
    0. Gutenberg
    1. lower
    2. special characters
    3. tags
    4. punctuation (hyphens, apostrophes, ampersands)
    5. digits
    6. white space
    7. consolidations
    8. lemmatize
    9. stop words/keep words
    """


    # -- 0. Gutenberg --------------------------------------------------------------
    if gutenberg:
        # find end of front boiler plate
        RE_startGutenberg = re.compile(ur"\*\*\* Start.*?\*\*\*", re.IGNORECASE | re.UNICODE)
        match = re.search(RE_startGutenberg, text)
        if match:
            endBoilerFront = match.end()
            text = text[endBoilerFront:] # text saved without front boiler plate

        # now let's find the start of the ending boiler plate
        RE_endGutenberg = re.compile(ur"End of.*?Project Gutenberg", re.IGNORECASE | re.UNICODE)
        match = re.search(RE_endGutenberg, text)
        if match:
            startBoilerEnd = match.start()
            text = text[:startBoilerEnd] #text saved without end boiler plate


    # -- 1. lower ------------------------------------------------------------------
    if lower:
        text = text.lower()
        cons_filestring = cons_filestring.lower()
        lem_filestring = lem_filestring.lower()
        sc_filestring = sc_filestring.lower()
        sw_kw_filestring = sw_kw_filestring.lower()

    # -- 2. special characters -----------------------------------------------------
    text = call_replacement_handler(text=text,
                                    replacer_string=sc_filestring,
                                    is_lemma=False,
                                    manualinputname='manualspecialchars',
                                    cache_folder=cache_folder,
                                    cache_filenames=cache_filenames,
                                    cache_number=2)

    # -- 3. tags -------------------------------------------------------------------
    if tags:
        text = handle_tags(text, keeptags, tags, filetype)

    # -- 4. punctuation (hyphens, apostrophes, ampersands) -------------------------
    if punct:
        text = remove_punctuation(text, apos, hyphen, amper, tags, previewing)

    # -- 5. digits -----------------------------------------------------------------
    if digits:
        text = remove_digits(text, previewing)

    # -- 6. white space ------------------------------------------------------------
    if whiteSpace:
        text = remove_whiteSpace(text, spaces, tabs, newLines, previewing)

    # -- 7. consolidations ---------------------------------------------------------
    text = call_replacement_handler(text=text,
                                    replacer_string=cons_filestring,
                                    is_lemma=False,
                                    manualinputname='manualconsolidations',
                                    cache_folder=cache_folder,
                                    cache_filenames=cache_filenames,
                                    cache_number=0)

    # -- 8. lemmatize ----------------------------------------------------------------
    text = call_replacement_handler(text=text,
                                    replacer_string=lem_filestring,
                                    is_lemma=True,
                                    manualinputname='manuallemmas',
                                    cache_folder=cache_folder,
                                    cache_filenames=cache_filenames,
                                    cache_number=1)

    # -- 9. stop words/keep words --------------------------------------------------
    if request.form['sw_option'] == "stop":
        if sw_kw_filestring:  # filestrings[3] == stop words
            cache_filestring(sw_kw_filestring, cache_folder, cache_filenames[3])
            removal_string = '\n'.join([sw_kw_filestring, request.form['manualstopwords']])
            if lower:   # stop words made non-case-sensitive if 'make lowercase' checked
                removal_string = removal_string.lower()
            text = remove_stopwords(text, removal_string)
        elif request.form['manualstopwords']:
            removal_string = request.form['manualstopwords']
            if lower:   # stop words made non-case-sensitive if 'make lowercase' checked
                removal_string = removal_string.lower()
            text = remove_stopwords(text, removal_string)
    elif request.form['sw_option'] == "keep":
        if sw_kw_filestring:  # filestrings[3] == keep stopwords
            cache_filestring(sw_kw_filestring, cache_folder, cache_filenames[3])
            keep_string = '\n'.join([sw_kw_filestring, request.form['manualstopwords']])
            if lower:   # keep words made non-case-sensitive if 'make lowercase' checked
                keep_string = keep_string.lower()
            text = keep_words(text, keep_string)
        elif request.form['manualstopwords']:
            keep_string = request.form['manualstopwords']
            if lower:   # keep words made non-case-sensitive if 'make lowercase' checked
                keep_string = keep_string.lower()
            text = keep_words(text, keep_string)
    return text
