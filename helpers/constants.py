""" Constants """
UPLOAD_FOLDER = '/tmp/Lexos/'
FILECONTENTS_FOLDER = 'filecontents/'
RESULTS_FOLDER = 'analysis_results/'

PREVIEW_SIZE = 500  # note: number of characters
CHARACTERS_PER_LINE_IN_LEGEND = 100

FILEMANAGER_FILENAME = 'filemanager.p'
DENDROGRAM_FILENAME = 'dendrogram.pdf'

# for scrub
SCRUBBOXES = ('punctuationbox', 'aposbox', 'hyphensbox', 'digitsbox', 'lowercasebox', 'tagbox')
SCRUBINPUTS = ('manualstopwords', 'manualspecialchars', 'manualconsolidations', 'manuallemmas')
OPTUPLOADNAMES = ('swfileselect[]', 'lemfileselect[]', 'consfileselect[]', 'scfileselect[]')
# for cut
CUTINPUTAREAS = ('cut_type', 'lastprop', 'overlap', 'cutting_value', 'cutsetnaming')
# for base analyze
ANALYZEBOXES = ('mfwcheckbox', 'cullcheckbox', 'greyword', 'inWordsOnly')
ANALYZEINPUTS = ('tokenSize', 'tokenType', 'normalizeType', 'norm', 'mfwnumber', 'cullnumber')
# for rowing window
RWBOXES = ('rollinghasmilestone',)  # if there is no comma in the end, python recognize this var as a string instead of a tuple
RWINPUTS = ('filetorollinganalyze', 'counttype', 'windowtype', 'inputtype', 'rollingsearchword', 'rollingsearchwordopt',
           'rollingwindowsize', 'rollingmilestonetype')
# for word cloud and multicloud and bubbleviz
CLOUDLIST = ('segmentlist', ) # if there is no comma in the end, python recognize this var as a string instead of a tuple
# for word cloud
# for multicloud
MCINPUTS = ('analysistype', 'optuploadname')


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

DEFAULT_ROLLINGWINDOW_OPTIONS = {'rollinghasmilestone': False, 'filetorollinganalyze': '', 'counttype': 'average',
                                 'windowtype': 'letter', 'inputtype': 'string', 'rollingsearchword': '', 'rollingsearchwordopt': '',
                                 'rollingwindowsize': '', 'rollingmilestonetype': ''}

DEFAULT_ANALIZE_OPTIONS = {'tokenSize': '1', 'tokenType': 'word', 'normalizeType': 'freq', 'norm': 'l1',
                           'mfwcheckbox': False, 'mfwnumber': '1', 'cullcheckbox': False, 'cullnumber': '1',
                           'greyword': False}
DEFAULT_CLOUD_OPTIONS = {'segmentlist': []}

DEFAULT_MC_OPTIONS = {
    'optuploadname': ''
}

DEFAULT_SIM_OPTIONS = {
    'uploadname': ''
}

# DEFAULT_DENDRO_OPTIONS = {
#   'orientation': 'top', 'title': '', 'pruning': 0, 'linkage': 'average', 'metric': 'euclidean', 'matrixData': 'freq'
# }
