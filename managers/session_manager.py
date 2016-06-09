import os
import pickle
from shutil import rmtree
import re
import random
import string

from flask import session, request

import helpers.constants as constants


def session_folder():
    """
    Generates and returns the file path for the session folder.

    Args:
        None

    Returns:
        The file path for the session folder.
    """
    return os.path.join(constants.UPLOAD_FOLDER, session['id'])


def reset():
    """
    Resets the current session, deleting the old folder and creating a new one.

    Args:
        None

    Returns:
        None
    """
    try:
        print '\nWiping session (' + session['id'] + ') and old files...'
        rmtree(os.path.join(constants.UPLOAD_FOLDER, session['id']))
    except:
        print 'Note: Failed to delete old session files:',
        if 'id' in session:
            print 'Couldn\'t delete ' + session['id'] + '\'s folder.'
        else:
            print 'Previous id not found.'
    session.clear()


def init():
    """
    Initializes the new session using a random id and creates a new session folder and file manager.

    Args:
        None

    Returns:
        None
    """

    folderCreated = False
    while not folderCreated:  # Continue to try to make
        try:
            session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
            print 'Attempting new id of', session['id'], '...',
            os.makedirs(session_folder())
            folderCreated = True
            print 'Good.'

        except:  # This except block will be hit if and only if the os.makedirs line throws an exception
            print 'Already in use.'

    # init FileManager
    from managers.file_manager import FileManager
    from managers import utility
     # initialize the file manager
    emptyFileManager = FileManager()

    utility.saveFileManager(emptyFileManager)

    print 'Initialized new session, session folder, and empty file manager with id.'


def fix():
    """
    this function fix the problem of outdated session

    """
    try:
        if not os.path.isfile(os.path.join(constants.UPLOAD_FOLDER, session['id'], constants.FILEMANAGER_FILENAME)):
            # 1. no file manager
            # 2. no session folder
            init()  # reinitialize the session and create a file manager
    except KeyError:
        # no 'id' in session
        init()


def save(path):
    """
    Pickle session into a specific path
    
    Args:
        path: the path you want to put session.p into

    Returns:
        None
    """
    path = os.path.join(path, constants.SESSION_FILENAME)
    sessionCopy = deepCopySession()
    pickle.dump(sessionCopy, open(path, 'wb'))



def load():
    """
    Merges the session of the session you uploaded with the current session
    (all the settings contained in the session you upload will replace the settings in current session)
    
    Args:
        None

    Returns:
        None
    """
    path = os.path.join(session_folder(), constants.SESSION_FILENAME)
    newsession = pickle.load(open(path, 'rb'))
    for key in newsession:
        if key != 'id':  # only keep the session id because that determines the session folder
            session[key] = newsession[key]
    os.remove(path)  # delete the session file


def deepCopySession():
    """
    Creates a deep copy of the current session

    Args:
        None

    Returns:
        the copy of the session
    """
    result = {}
    for key in session.keys():
        result[key] = session[key]
    return result


def cacheAlterationFiles():
    """
    Stores all alteration files (uploaded on the scrub page) from request.form in the session cookie object.

    Args:
        None

    Returns:
        None
    """
    for uploadFile in request.files:
        fileName = request.files[uploadFile].filename
        if fileName != '':
            session['scrubbingoptions']['optuploadnames'][uploadFile] = fileName
            # the following line don't seem to do anything
            # session.modified = True  # Necessary to tell Flask that the mutable object (dict) has changed


def cacheScrubOptions():
    """
    Stores all scrubbing options from request.form in the session cookie object.

    Args:
        None

    Returns:
        None
    """
    for box in constants.SCRUBBOXES:
        session['scrubbingoptions'][box] = (box in request.form)
    for box in constants.SCRUBINPUTS:
        session['scrubbingoptions'][box] = (request.form[box] if box in request.form else '')
    if 'tags' in request.form:
        session['scrubbingoptions']['keepDOEtags'] = request.form['tags'] == 'keep'
    session['scrubbingoptions']['entityrules'] = request.form['entityrules']

def cacheXMLHandlingOptions(data):
    """
    Stores all the XML Handling options from request.form in the session cookie object.

    Args:
        data: a json string

    Return:
        None
    """
    import json

    xmlDict = json.loads(json.dumps(data))

    RE_delKeyMatch = re.compile(ur'(myselect|attributeValue)', re.IGNORECASE | re.UNICODE)

    # deleting all the unnecessary entries for this purpose in xmlDict
    for key in xmlDict.keys():
        match = re.search(RE_delKeyMatch, key)
        if (not match):
        #if  key doesn't start with myselect or attributeValue':
            del xmlDict[key]
        else:
            print key, "---", xmlDict[key]

    name = 'myselect'
    attribute = 'attributeValue'
    length = len(xmlDict.keys()) #gets the length of xmlDict
    length = length/2 #divides length in half since data contains twice the amount wanted

    xmlhandlingdict = {}

    for i in range(0,length):
        nameval = name + str(i) #add the number to the name
        attrib_tag = xmlDict[nameval].split(",") #split the value from data at name by the comma so we have the attribute and tag seperated
        attributeval = attribute + str(i) #add the number to the attribute
        attributevalue = xmlDict[attributeval]

        #add all the values to the dictionary
        xmlhandlingdict2 = {}
        xmlhandlingdict2['action'] = attrib_tag[0]
        xmlhandlingdict2['tag'] = attrib_tag[1]
        xmlhandlingdict2['attribute'] = attributevalue

        xmlhandlingdict[nameval] = xmlhandlingdict2 #associate the nameval with the dictionary that was just made
        print nameval, "---", xmlhandlingdict[nameval]

    session['xmlhandlingoptions'] = xmlhandlingdict


def cacheCuttingOptions():
    """
    Stores all cutting options from request.form in the session cookie object.

    Args:
        None

    Returns:
        None
    """
    session['cuttingoptions'] = {'cutType': request.form['cutType'],
                                 'cutValue': request.form['cutValue'],
                                 'cutOverlap': request.form['cutOverlap'] if 'cutOverlap' in request.form else '0',
                                 'cutLastProp': request.form['cutLastProp'] if 'cutLastProp' in request.form else '50'}
    if "cutByMS" in request.form:
        session['cuttingoptions']['cutType'] = "milestone"
        session['cuttingoptions']['cutValue'] = request.form['MScutWord']


def cacheCSVOptions():
    """
    Stores all cutting options from request.form in the session cookie object.

    Args:
        None

    Returns:
        None
    """
    session['csvoptions'] = {'csvorientation': request.form['csvorientation'],
                             'csvdelimiter': request.form['csvdelimiter']}

    if 'onlygreyword' in request.form:
        session['csvoptions'].update({'onlygreyword': request.form['onlygreyword']})


def cacheAnalysisOption():
    """
    Stores all base_analyze options from request.form in the session cookie object.

    Args:
        None

    Returns:
        None
    """
    # check boxes
    for box in constants.ANALYZEBOXES:
        session['analyoption'][box] = (box in request.form)
    # non check boxes
    for input in constants.ANALYZEINPUTS:
        session['analyoption'][input] = (
            request.form[input] if input in request.form else constants.DEFAULT_ANALYZE_OPTIONS[input])


def cacheRWAnalysisOption():
    """
    Stores all rolling window options from request.form in the session cookie object.

    Args:
        None

    Returns:
        None
    """
    # check boxes
    for box in constants.RWBOXES:
        session['rwoption'][box] = (box in request.form)
    # non check boxes
    for input in constants.RWINPUTS:
        session['rwoption'][input] = (
            request.form[input] if input in request.form else constants.DEFAULT_ROLLINGWINDOW_OPTIONS[input])


def cacheCloudOption():
    """
    Stores all the globle cloud options from request.form in the session cookie object. see constant.CLOUDLIST for more

    Args:
        None

    Returns:
        None
    """
    # list
    for list in constants.CLOUDLIST:
        session['cloudoption'][list] = request.form.getlist(list)


def cacheMultiCloudOptions():
    """
    stores filename if uploading topic file to use for multicloud

    Args: 
        None

    Returns:
        None
    """

    for input in constants.MULTICLOUDINPUTS:
        session['multicloudoptions'][input] = (
            request.form[input] if input in request.form else constants.DEFAULT_MULTICLOUD_OPTIONS[input])
    for file in constants.MULTICLOUDFILES:
        filePointer = (request.files[file] if file in request.files else constants.DEFAULT_MULTICLOUD_OPTIONS[file])
        topicstring = str(filePointer)
        topicstring = re.search(r"'(.*?)'", topicstring)
        filename = topicstring.group(1)
        if filename != '':
            session['multicloudoptions'][file] = filename


def cacheBubbleVizOption():
    """
    Stores all Bubble Viz options from request.form in the session cookie object.

    Args:
        None

    Returns:
        None
    """
    for box in constants.BUBBLEVIZBOX:
        session['bubblevisoption'][box] = (box in request.form)
    for input in constants.BUBBLEVIZINPUT:
        session['bubblevisoption'][input] = (
            request.form[input] if input in request.form else constants.DEFAULT_BUBBLEVIZ_OPTIONS[input])


def cacheStatisticOption():
    """
    Stores all the globle cloud options from request.form in the session cookie object. see constant.CLOUDLIST for more

    Args:
        None

    Returns:
        None
    """
    # list
    for list in constants.STATISTIC_LIST:
        session['statisticoption'][list] = request.form.getlist(list)


def cacheHierarchyOption():
    """
    Stores all Hierarchy Clustering options from request.form in the session cookie object.

    Args:
        None

    Returns:
        None
    """
    for box in constants.HIERARCHICALBOX:
        session['hierarchyoption'][box] = (box in request.form)
    for input in constants.HIERARCHICALINPUT:
        session['hierarchyoption'][input] = (
            request.form[input] if input in request.form else constants.DEFAULT_HIERARCHICAL_OPTIONS[input])


def cacheKmeanOption():
    """
    Stores all Kmean options from request.form in the session cookie object.

    Args:
        None

    Returns:
        None
    """
    for input in constants.KMEANINPUT:
        session['kmeanoption'][input] = (
            request.form[input] if input in request.form else constants.DEFAULT_KMEAN_OPTIONS[input])


def cacheSimOptions():
    """
    stores filename if uploading topic file to use for multicloud

    Args: 
        None

    Returns:
        None
    """

    for box in constants.SIMBOX:
        session['similarities'][box] = (box in request.form)
    for input in constants.SIMINPUT:
        session['similarities'][input] = (
            request.form[input] if input in request.form else constants.DEFAULT_SIM_OPTIONS[input])

def cacheTopwordOptions():
    """
    stores filename if uploading topic file to use for top word

    Args:
        None

    Returns:
        None
    """

    for input in constants.TOPWORDINPUT:
        session['topwordoption'][input] = (
            request.form[input] if input in request.form else constants.DEFAULT_TOPWORD_OPTIONS[input])