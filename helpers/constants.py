""" Constants """
UPLOAD_FOLDER = '/tmp/Lexos/'
FILECONTENTS_FOLDER = 'filecontents/'
RESULTS_FOLDER = 'analysis_results/'
WORKSPACE_DIR = 'workspace/'
WORKSPACE_UPLOAD_DIR = 'tmp/Lexos/workspace/'  # use to handle workspace upload
# this should be equal to UPLOAD_FOLDER + WORKSPACE_DIR

MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024  # 1 GB
MAX_FILE_SIZE_INT = 1
MAX_FILE_SIZE_UNITS = "G"

PREVIEW_SIZE = 500  # note: number of characters in a preview screen (e.g., on Select page)
MIN_ENCODING_DETECT = 500  # minimum number of characters used to detect a file's encoding scheme upon upload
CHARACTERS_PER_LINE_IN_LEGEND = 100

FILEMANAGER_FILENAME = 'filemanager.p'
SESSION_FILENAME = 'session.p'

DENDROGRAM_FILENAME = 'dendrogram.pdf'
FILE_INFORMATION_FIGNAME = 'statistic.svg'
CORPUS_INFORMATION_FIGNAME = 'corpus_statistic.svg'
WORKSPACE_FILENAME = 'workspace.lexos'

KMEANS_GRAPH_FILENAME = 'kmeans.svg'

'''the request form keys'''
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
RWBOXES = (
    'rollinghasmilestone',)  # if there is no comma in the end, python recognize this var as a string instead of a tuple
RWINPUTS = ('filetorollinganalyze', 'counttype', 'windowtype', 'inputtype', 'rollingsearchword', 'rollingsearchwordopt',
            'rollingwindowsize', 'rollingmilestonetype')

# for word cloud and multicloud and bubbleviz
CLOUDLIST = (
    'segmentlist',)  # if there is no comma in the end, python recognize this var as a string instead of a tuple

# for word cloud
# for multicloud
MULTICLOUDINPUTS = ('analysistype',)
MULTICLOUDFILES = ('optuploadname',)

# for BubbleViz
BUBBLEVIZBOX = ('vizmaxwords',)
BUBBLEVIZINPUT = ('minlength', 'graphsize', 'maxwords')

# for hierarchical Clustering
HIERARCHICALBOX = ('augmented', 'dendroLegends')
HIERARCHICALINPUT = ('metric', 'linkage', 'title', 'orientation', 'pruning', 'criterion', 'threshold')

# for kmeans Clustering
KMEANINPUT = ('nclusters', 'max_iter', 'init', 'n_init', 'tolerance', 'KMeans_metric')
# for similarity query
SIMINPUT = ('uploadname',)
SIMBOX = ('simsuniquetokens',)

'''the request form default value'''
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
                                 'windowtype': 'letter', 'inputtype': 'string', 'rollingsearchword': '',
                                 'rollingsearchwordopt': '',
                                 'rollingwindowsize': '', 'rollingmilestonetype': ''}

DEFAULT_ANALIZE_OPTIONS = {'tokenSize': '1', 'tokenType': 'word', 'normalizeType': 'freq', 'norm': 'l0',
                           'mfwcheckbox': False, 'mfwnumber': '1', 'cullcheckbox': False, 'cullnumber': '1',
                           'greyword': False}

DEFAULT_CLOUD_OPTIONS = {'segmentlist': []}

DEFAULT_MULTICLOUD_OPTIONS = {'optuploadname': '', 'analysistype': 'userfiles'}

DEFAULT_BUBBLEVIZ_OPTIONS = {'vizmaxwords': False, 'minlength': '0', 'graphsize': '800', 'maxwords': '1'}

DEFAULT_HIERARCHICAL_OPTIONS = {'metric': 'euclidean', 'linkage': 'average', 'title': '', 'orientation': 'top',
                                'pruning': '', 'augmented': True, 'criterion': 'inconsistent', 'threshold': '',
                                'dendroLegends': False}

DEFAULT_KMEAN_OPTIONS = {'nclusters': '', 'max_iter': '', 'init': 'k-means++', 'n_init': '', 'tolerance': '',
                         'KMeans_metric': ''}

DEFAULT_SIM_OPTIONS = {'uploadname': '', 'simsuniquetokens': True}
