import os
import pickle
import re

import helpers.constants as constants


def makePreviewFrom(string):
    """
    Creates a formatted preview string from a file contents string.

    Args:
        string: A string from which to create the formatted preview.

    Returns:
        The formatted preview string.
    """
    if len(string) <= constants.PREVIEW_SIZE:
        previewString = string
    else:
        newline = '\n'
        halfLength = constants.PREVIEW_SIZE // 2
        previewString = string[:halfLength] + u'\u2026 ' + newline + newline + u'\u2026' + string[-halfLength:] # New look

    return previewString


def generateD3Object(wordCounts, objectLabel, wordLabel, countLabel):
    """
    Generates a properly formatted JSON object for d3 use.

    Args:
        objectLabel: The label to identify this object.
        wordLabel: A label to identify all "words".
        countLabel: A label to identify all counts.

    Returns:
        The formatted JSON object.
    """
    JSONObject = {}

    JSONObject['name'] = str(objectLabel)

    JSONObject['children'] = []

    for word, count in wordCounts.items():
        JSONObject['children'].append({ wordLabel: word.encode('utf-8'), countLabel: count })

    return JSONObject

def intkey(s):
    """
    Returns the key to sort by.

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
    Sorts lists in human order (10 comes after 2, even when both are strings)

    Args:
        A list

    Returns:
        A sorted list
    """
    return sorted(l, key=intkey)