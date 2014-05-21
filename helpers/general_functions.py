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
    return {'cuttingType': 'Size', 'cuttingValue': '', 'overlap': '0', 'lastProp': '50'}

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