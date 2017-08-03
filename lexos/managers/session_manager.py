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
                random.choice(
                    string.ascii_uppercase +
                    string.digits) for _ in range(30))

            print('Attempting new id of', session['id'], '...', end=' ')
            os.makedirs(session_folder())
            folder_created = True
            print('Good.')

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

    for uploadFile in request.files:
        file_name = request.files[uploadFile].filename
        if file_name != '':

            session['scrubbingoptions']['optuploadnames'][uploadFile] = \
                file_name


def cache_scrub_options():
    """Stores scrubbing options from request.form in session cookie object."""

    for box in const.SCRUBBOXES:
        session['scrubbingoptions'][box] = (box in request.form)

    for box in const.SCRUBINPUTS:
        session['scrubbingoptions'][box] = (
            request.form[box] if box in request.form else '')

    session['scrubbingoptions']['sw_option'] = request.form['sw_option']
    if 'tags' in request.form:
        session['scrubbingoptions']['keepDOEtags'] = \
            request.form['tags'] == 'keep'

    session['scrubbingoptions']['entityrules'] = request.form['entityrules']


def cache_cutting_options():
    """Stores cutting options from request.form in session cookie object."""

    session['cuttingoptions'] = {
        'cutType': request.form['cutType'],

        'cutValue': request.form['cutValue'],

        'cutOverlap': request.form['cutOverlap']
        if 'cutOverlap' in request.form else '0',

        'cutLastProp': request.form['cutLastProp']
        if 'cutLastProp' in request.form else '50'}
    if "cutByMS" in request.form:
        session['cuttingoptions']['cutType'] = "milestone"
        session['cuttingoptions']['cutValue'] = request.form['MScutWord']


def cache_csv_options():
    """Stores cutting options from request.form in session cookie object."""

    if request.json:
        session['csvoptions'] = {
            'csvorientation': request.json['csvorientation'],
            'csvdelimiter': request.json['csvdelimiter']}

        if 'onlygreyword' in request.json:
            session['csvoptions'].update(
                {'onlygreyword': request.json['onlygreyword']})
    else:
        session['csvoptions'] = {
            'csvorientation': request.form['csvorientation'],
            'csvdelimiter': request.form['csvdelimiter']}

        if 'onlygreyword' in request.form:
            session['csvoptions'].update(
                {'onlygreyword': request.form['onlygreyword']})


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


def cache_cloud_option():
    """Stores global cloud options from request.form in session cookie object.

    See constant.CLOUDLIST for more.
    """

    # list
    for list in const.CLOUDLIST:
        session['cloudoption'][list] = request.form.getlist(list)


def cache_multi_cloud_options():
    """Stores filename if uploading topic file to use for multicloud."""

    for request_input in const.MULTICLOUDINPUTS:

        session['multicloudoptions'][request_input] = \
            request.form[request_input] if input in request.form \
            else const.DEFAULT_MULTICLOUD_OPTIONS[request_input]

    for file in const.MULTICLOUDFILES:

        file_pointer = request.files[file] \
            if file in request.files \
            else const.DEFAULT_MULTICLOUD_OPTIONS[file]

        topic_string = str(file_pointer)
        topic_string = re.search(r"'(.*?)'", topic_string)
        filename = topic_string.group(1)
        if filename != '':
            session['multicloudoptions'][file] = filename


def cache_bubble_viz_option():
    """Stores Bubble Viz options from request.form in session cookie object."""

    for box in const.BUBBLEVIZBOX:
        session['bubblevisoption'][box] = (box in request.form)
    for request_input in const.BUBBLEVIZINPUT:
        session['bubblevisoption'][request_input] = (
            request.form[request_input] if input in request.form
            else const.DEFAULT_BUBBLEVIZ_OPTIONS[request_input])


def cache_statistic_option():
    """Stores global cloud options from request.form in session cookie object.

    See constant.CLOUDLIST for more.
    """

    # list
    for list in const.STATISTIC_LIST:
        session['statisticoption'][list] = request.form.getlist(list)


def cache_hierarchy_option():
    """Stores all Hierarchy Clustering options in the session cookie object.

    These options were from request.form.
    """

    if request.json:
        opts = request.json
    else:
        opts = request.form
    for box in const.HIERARCHICALBOX:
        session['hierarchyoption'][box] = (box in opts)
    for request_input in const.HIERARCHICALINPUT:
        session['hierarchyoption'][request_input] = (
            opts[request_input] if input in opts
            else const.DEFAULT_HIERARCHICAL_OPTIONS[request_input])
    session['degenerated'] = True


def cache_k_mean_option():
    """Stores Kmean options from request.form in the session cookie object."""

    for request_input in const.KMEANINPUT:
        session['kmeanoption'][request_input] = (
            request.form[request_input] if input in request.form
            else const.DEFAULT_KMEAN_OPTIONS[request_input])


def cache_sim_options():
    """Stores filename if uploading topic file to use for multicloud."""

    for box in const.SIMBOX:
        session['similarities'][box] = (box in request.form)
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
    """Stores all general settings options in the session cookie object.

    These options were from request.json.
    """

    # for setting in constants.GENERALSETTINGS:
    if request.json:
        session['generalsettings']["beta_onbox"] = request.json["beta_onbox"]
    else:
        session['generalsettings']["beta_onbox"] = const.GENERALSETTINGS
    session.modified = True
