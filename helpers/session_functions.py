import os
import pickle
from shutil import rmtree
import zipfile

from flask import session, request
import re

import helpers.constants as constants
from helpers.general_functions import zipdir

import models.ModelClasses


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
    import random, string
    from models.ModelClasses import FileManager

    folderCreated = False
    while not folderCreated:  # Continue to try to make
        try:
            session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
            print 'Attempting new id of', session['id'], '...',
            os.makedirs(session_folder())
            folderCreated = True
            print 'Good.'

        except:  # This except block will be hit if and only if the os.makedirs line throws an exception
            print 'Already in use.'

    emptyFileManager = FileManager()
    saveFileManager(emptyFileManager)

    print 'Initialized new session, session folder, and empty file manager with id.'


def loadFileManager():
    """
    Loads the file manager for the specific session from the hard drive.

    Args:
        None

    Returns:
        The file manager object for the session.
    """
    from models.ModelClasses import FileManager

    managerFilePath = os.path.join(session_folder(), constants.FILEMANAGER_FILENAME)
    fileManager = pickle.load(open(managerFilePath, 'rb'))

    return fileManager


def saveFileManager(fileManager):
    """
    Saves the file manager to the hard drive.

    Args:
        fileManager: File manager object to be saved.

    Returns:
        None
    """

    managerFilePath = os.path.join(session_folder(), constants.FILEMANAGER_FILENAME)
    pickle.dump(fileManager, open(managerFilePath, 'wb'))


def saveSession(session):
    WorkSpacePath = os.path.join(session_folder(), constants.WORKSPACE_DIR, constants.SESSION_FILENAME)
    pickle.dump(session, open(WorkSpacePath, 'wb'))


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

    session['csvoptions'] = {'csvcontent': request.form['csvcontent'],
                             'csvorientation': request.form['csvorientation'],
                             'csvdelimiter': request.form['csvdelimiter']}


def cacheAnalysisOption():
    # check boxes
    for box in constants.ANALYZEBOXES:
        session['analyoption'][box] = (box in request.form)
    # non check boxes
    for input in constants.ANALYZEINPUTS:
        session['analyoption'][input] = (
            request.form[input] if input in request.form else constants.DEFAULT_ANALIZE_OPTIONS[input])


def cacheRWAnalysisOption():
    # check boxes
    for box in constants.RWBOXES:
        session['rwoption'][box] = (box in request.form)
    # non check boxes
    print 'request', request.form['filetorollinganalyze']
    for input in constants.RWINPUTS:
        session['rwoption'][input] = (
            request.form[input] if input in request.form else constants.DEFAULT_ROLLINGWINDOW_OPTIONS[input])


def cacheCloudOption():
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


def cachBubbleVizOption():
    for box in constants.BUBBLEVIZBOX:
        session['bubblevisoption'][box] = (box in request.form)
    for input in constants.BUBBLEVIZINPUT:
        session['bubblevisoption'][input] = (
            request.form[input] if input in request.form else constants.DEFAULT_BUBBLEVIZ_OPTIONS[input])


def cachHierarchyOption():
    for box in constants.HIERARCHICALBOX:
        session['hierarchyoption'][box] = (box in request.form)
    for input in constants.HIERARCHICALINPUT:
        session['hierarchyoption'][input] = (
            request.form[input] if input in request.form else constants.DEFAULT_HIERARCHICAL_OPTIONS[input])


def cachKmeanOption():
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

    session['similarities']['uploadname'] = (request.form['uploadname'] if 'uploadname' in request.form else '')
