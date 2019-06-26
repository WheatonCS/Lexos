import os
import pickle
import random
import re
import string
from shutil import rmtree

from flask import session, request

from lexos.helpers import constants as const


def session_folder() -> str:
    """Generates and returns the file path for the session folder.

    :return: the file path for the session folder.
    """

    return os.path.join(const.UPLOAD_FOLDER, session['id'])


def reset():
    """Resets current session, deleting old folder and creating a new one."""

    try:
        print('\nWiping session (' + session['id'] + ') and old files...')
        rmtree(os.path.join(const.UPLOAD_FOLDER, session['id']))
    except FileNotFoundError:
        print('Note: Failed to delete old session files:', end=' ')
        if 'id' in session:
            print('Couldn\'t delete ' + session['id'] + '\'s folder.')
        else:
            print('Previous id not found.')
    session.clear()


def init():
    """Initializes new session & creates new session folder & file manager.

    New session initialized using a random id.
    """

    folder_created = False
    while not folder_created:  # Continue to try to make
        try:
            session['id'] = ''.join(
                random.choice(string.ascii_uppercase + string.digits)
                for _ in range(30)
            )

            print('Attempting new id of', session['id'], '...', end=' ')
            os.makedirs(session_folder())
            folder_created = True

        # This except block will be hit if and only if
        # the os.makedirs line throws an exception
        except FileExistsError:
            print('Already in use.')

    # init FileManager
    from lexos.managers.file_manager import FileManager
    from lexos.managers import utility
    # initialize the file manager
    empty_file_manager = FileManager()

    utility.save_file_manager(empty_file_manager)

    print('Initialized new session, session folder, and empty file manager '
          'with id.')


def fix():
    """This function fixes the problem of outdated session."""

    try:
        if not os.path.isfile(
            os.path.join(
                const.UPLOAD_FOLDER,
                session['id'],
                const.FILEMANAGER_FILENAME)):
            # 1. no file manager
            # 2. no session folder
            print("No file manager or session folder. Re-initialising.")
            init()  # reinitialize the session and create a file manager
    except KeyError:
        # no 'id' in session
        print("No 'id' in session. Re-initialising.")
        init()


def save(path: str):
    """Pickle session into a specific path.

    :param path: the path you want to put session.p into.
    """

    path = os.path.join(path, const.SESSION_FILENAME)
    session_copy = deep_copy_session()
    pickle.dump(session_copy, open(path, 'wb'))


def load():
    """Merges the session of the session you uploaded with the current session.

    All the settings contained in the session you upload will replace the
    settings in current session.
    """

    path = os.path.join(session_folder(), const.SESSION_FILENAME)
    new_session = pickle.load(open(path, 'rb'))
    for key in new_session:
        # only keep the session id because that determines the session folder
        if key != 'id':
            session[key] = new_session[key]
    os.remove(path)  # delete the session file


def deep_copy_session() -> dict:
    """Creates a deep copy of the current session.
    :return: the copy of the session.
    """

    result = {}
    for key in list(session.keys()):
        result[key] = session[key]
    return result


def cache_alteration_files():
    """Stores all alteration files in the session cookie object.

    All alteration files (uploaded on the scrub page) are from request.form.
    """

    for upload_file in request.files:
        file_name = request.files[upload_file].filename
        if file_name != '':
            session['scrubbingoptions']['file_uploads'][upload_file] = \
                file_name


def cache_scrub_options():
    """Stores scrubbing options from request.form in session cookie object."""

    for box in const.SCRUBBOXES:
        session['scrubbingoptions'][box] = (box in request.form)

    for box in const.SCRUBINPUTS:
        session['scrubbingoptions'][box] = (
            request.form[box] if box in request.form else '')

    session['scrubbingoptions']['stop_words_'] = \
        request.form['stop_words_method']
    if 'tags' in request.form:
        session['scrubbingoptions']['keepDOEtags'] = \
            request.form['tags'] == 'keep'

    session['scrubbingoptions']['special_characters_preset'] = \
        request.form['special_characters_preset']


def cache_cutting_options():
    """Stores cutting options from request.form in session cookie object."""

    session['cuttingoptions'] = {
        'cut_mode': request.form['cut_mode'],

        'segment_size': request.form['segment_size'],

        'overlap': request.form['overlap']
        if 'overlap' in request.form else '0',

        'merge_threshold': request.form['merge_threshold']
        if 'merge_threshold' in request.form else '50'}
    if "cutByMS" in request.form:
        session['cuttingoptions']['cut_mode'] = "Milestones"
        session['cuttingoptions']['segment_size'] = request.form['MScutWord']


def cache_analysis_option():
    """Stores base_analyze options from request.form in sess cookie object."""

    if request.json:
        # check boxes
        for box in const.ANALYZEBOXES:
            session['analyoption'][box] = (box in request.json)
        # non check boxes
        for request_input in const.ANALYZEINPUTS:
            session['analyoption'][request_input] = (
                request.json[request_input] if input in request.json
                else const.DEFAULT_ANALYZE_OPTIONS[request_input])
    else:
        # check boxes
        for box in const.ANALYZEBOXES:
            session['analyoption'][box] = (box in request.form)
        # non check boxes
        for request_input in const.ANALYZEINPUTS:
            session['analyoption'][request_input] = (
                request.form[request_input] if input in request.form
                else const.DEFAULT_ANALYZE_OPTIONS[request_input])


def cache_rw_analysis_option():
    """Stores rolling window options frm request.form in sess cookie object."""

    # check boxes
    for box in const.RWBOXES:
        session['rwoption'][box] = (box in request.form)
    # non check boxes
    for request_input in const.RWINPUTS:
        session['rwoption'][request_input] = (
            request.form[request_input] if input in request.form
            else const.DEFAULT_ROLLINGWINDOW_OPTIONS[request_input])


def cache_hierarchy_option():
    """Stores all Hierarchy Clustering options in the session cookie object.

    These options were from request.form.
    """

    if request.json:
        opts = request.json
    else:
        opts = request.form
    for request_input in const.HIERARCHICALINPUT:
        session['hierarchyoption'][request_input] = (
            opts[request_input] if input in opts
            else const.DEFAULT_HIERARCHICAL_OPTIONS[request_input])


def cache_bct_option():
    """Stores BCT options from request.form in the session cookie object."""
    for request_input in const.BCTINPUT:
        session['bctoption'][request_input] = (
            request.form[request_input] if input in request.form
            else const.DEFAULT_BCT_OPTIONS[request_input]
        )


def cache_k_mean_option():
    """Stores Kmean options from request.form in the session cookie object."""

    for request_input in const.KMEANINPUT:
        session['kmeanoption'][request_input] = (
            request.form[request_input] if input in request.form
            else const.DEFAULT_KMEAN_OPTIONS[request_input])


def cache_sim_options():
    """Stores filename if uploading topic file to use for similarity query."""

    for request_input in const.SIMINPUT:
        session['similarities'][request_input] = (
            request.form[request_input] if input in request.form
            else const.DEFAULT_SIM_OPTIONS[request_input])


def cache_top_word_options():
    """Stores filename if uploading topic file to use for top word."""

    for request_input in const.TOPWORDINPUT:
        session['topwordoption'][request_input] = (
            request.form[request_input] if input in request.form
            else const.DEFAULT_TOPWORD_OPTIONS[request_input])


def cache_general_settings():
    """Stores the general settings.
    """

    session["generalsettings"]["theme"] = request.json["theme"]
    session.modified = True
