import os
import pickle
import re

import helpers.constants as constants

def defaultScrubSettings():
    settingsDict = {'punctuationbox': True, 'aposbox': False, 'hyphensbox': False, 'digitsbox': True, 'lowercasebox': True, 'tagbox': True}

    for box in constants.TEXTAREAS:
        settingsDict[box] = ''

    settingsDict['optuploadnames'] = {}
    for name in constants.OPTUPLOADNAMES:
        settingsDict['optuploadnames'][name] = ''

    settingsDict['entityrules'] = 'default'

    return settingsDict

def defaultCutSettings():
    return {'cut_type': 'size', 'cutting_value': '', 'overlap': '0', 'lastprop': '50'}

def defaultCSVSettings():
    return {'csvdata': 'count', 'csvorientation': 'filecolumn', 'csvdelimiter': 'comma'}

def defaultDendroSettings():
    return {'orientation':'top','title':'','pruning':0,'linkage':'average','metric':'euclidean'}


def makePreviewFrom(string):
    splitString = string.split()

    if len(splitString) <= constants.PREVIEW_SIZE:
        previewString = ' '.join(splitString)
    else:
        newline = u'\n'
        halfLength = constants.PREVIEW_SIZE // 2
        previewString = ' '.join(splitString[:halfLength]) + u'\u2026 ' + newline + newline + u'\u2026' + ' '.join(splitString[-halfLength:]) # New look

    return previewString


def generateD3Object(wordCounts, objectLabel, wordLabel, countLabel):
    JSONObject = {}

    JSONObject['name'] = str(objectLabel)

    JSONObject['children'] = []

    for word, count in wordCounts.items():
        JSONObject['children'].append({ wordLabel: str(word), countLabel: count })

    return JSONObject

def intkey(s):
    """
    Returns the key to sort by

    Args:
        A key

    Returns:
        A key converted into an int if applicable
    """
    if type(s) == tuple:
        s = s[0]
    return tuple(int(part) if re.match(r'[0-9]+$', part) else part
        for part in re.split(r'([0-9]+)', s))

def natsort(l):
    """
    Sorts lists in human order (10 comes after 2, even with both are strings)

    Args:
        A list

    Returns:
        A sorted list
    """
    return sorted(l, key=intkey)