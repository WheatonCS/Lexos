import os
import pickle
from shutil import rmtree

from flask import session, request

import helpers.constants as constants

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
    while not folderCreated: # Continue to try to make
        try:
            session['id'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
            print 'Attempting new id of', session['id'], '...',
            os.makedirs(session_folder())
            folderCreated = True
            print 'Good.'

        except: # This except block will be hit if and only if the os.makedirs line throws an exception
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
    from models.ModelClasses import FileManager
    
    managerFilePath = os.path.join(session_folder(), constants.FILEMANAGER_FILENAME)
    pickle.dump(fileManager, open(managerFilePath, 'wb'))

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
    session.modified = True # Necessary to tell Flask that the mutable object (dict) has changed


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
    for box in constants.TEXTAREAS:
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

def cacheCSVOptions():
    """
    Stores all cutting options from request.form in the session cookie object.

    Args:
        None

    Returns:
        None
    """

    session['csvoptions'] = {'normalizeType': request.form['normalizeType'],
                             'csvorientation': request.form['csvorientation'],
                             'csvdelimiter': request.form['csvdelimiter']}

def cacheMCOptions():
    """
    stores filename if uploading topic file to use for multicloud

    Args: 
        None

    Returns:
        None
    """

    session['multicloudoptions']['optuploadname'] = (request.form['optuploadname'] if 'optuploadname' in request.form else '')


def cacheSimOptions():
    """
    stores filename if uploading topic file to use for multicloud

    Args: 
        None

    Returns:
        None
    """

    session['similarities']['uploadname'] = (request.form['uploadname'] if 'uploadname' in request.form else '')
