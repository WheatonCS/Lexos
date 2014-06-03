import os
import pickle
import re

import helpers.constants as constants


def makePreviewFrom(string):

    if len(string) <= constants.PREVIEW_SIZE:
        previewString = string
    else:
        newline = '\n'
        halfLength = constants.PREVIEW_SIZE // 2
        previewString = string[:halfLength] + u'\u2026 ' + newline + newline + u'\u2026' + string[-halfLength:] # New look

    return previewString


def generateD3Object(wordCounts, objectLabel, wordLabel, countLabel):
    JSONObject = {}

    JSONObject['name'] = str(objectLabel)

    JSONObject['children'] = []

    for word, count in wordCounts.items():
        JSONObject['children'].append({ wordLabel: word.encode('utf-8'), countLabel: count })

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