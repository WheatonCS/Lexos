""" Constants """
UPLOAD_FOLDER = '/tmp/Lexos/'
FILECONTENTS_FOLDER = 'filecontents/'
RESULTS_FOLDER = 'analysis_results/'

PREVIEW_SIZE = 500  # note: number of characters

FILEMANAGER_FILENAME = 'filemanager.p'
DENDROGRAM_FILENAME = 'dendrogram.pdf'

SCRUBBOXES = ('punctuationbox', 'aposbox', 'hyphensbox', 'digitsbox', 'lowercasebox', 'tagbox')
TEXTAREAS = ('manualstopwords', 'manualspecialchars', 'manualconsolidations', 'manuallemmas')
OPTUPLOADNAMES = ('swfileselect[]', 'lemfileselect[]', 'consfileselect[]', 'scfileselect[]')
CUTINPUTAREAS = ('cut_type', 'lastprop', 'overlap', 'cutting_value', 'cutsetnaming')
ANALYZEBOXES = ('mfwcheckbox', 'cullcheckbox', 'greyword', 'inWordsOnly')
ANALYZENUMS = ('tokenSize', 'tokenType', 'normalizeType', 'norm', 'mfwnumber', 'cullnumber')

CHARACTERS_PER_LINE_IN_LEGEND = 100

# Default options for use in session and accessing request.form
DEFAULT_SCRUB_OPTIONS = {
    'punctuationbox': True, 'aposbox': False, 'hyphensbox': False, 'digitsbox': True, 'lowercasebox': True,
    'tagbox': True,
    'manualstopwords': '', 'manualspecialchars': '', 'manualconsolidations': '', 'manuallemmas': '',
    'entityrules': 'default', 'optuploadnames': {
    'swfileselect[]': '', 'lemfileselect[]': '', 'consfileselect[]': '', 'scfileselect[]': '',
}
}
DEFAULT_CUT_OPTIONS = {
    'cutType': 'words', 'cutValue': '', 'cutOverlap': '0', 'cutLastProp': '50'
}
DEFAULT_CSV_OPTIONS = {
    'csvdata': 'count', 'csvorientation': 'filecolumn', 'csvdelimiter': 'comma'
}

DEFAULT_ANALIZE_OPTIONS = {'tokenSize': '1', 'tokenType': 'word', 'normalizeType': 'freq', 'norm': 'l1',
                           'mfwcheckbox': False, 'mfwnumber': '1', 'cullcheckbox': False, 'cullnumber': '1',
                           'greyword': False}

DEFAULT_MC_OPTIONS = {
    'optuploadname': ''
}

DEFAULT_SIM_OPTIONS = {
    'uploadname': ''
}

# DEFAULT_DENDRO_OPTIONS = {
#   'orientation': 'top', 'title': '', 'pruning': 0, 'linkage': 'average', 'metric': 'euclidean', 'matrixData': 'freq'
# }
