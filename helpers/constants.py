""" Constants """

'''configurations'''
IS_SERVER = False
DUMPING = True

'''file dir'''
UPLOAD_FOLDER = '/tmp/Lexos/'
FILECONTENTS_FOLDER = 'filecontents/'
RESULTS_FOLDER = 'analysis_results/'
WORKSPACE_DIR = 'workspace/'
WORKSPACE_UPLOAD_DIR = 'tmp/Lexos/workspace/'  # use to handle workspace upload
# this should be equal to UPLOAD_FOLDER + WORKSPACE_DIR

'''file name'''
FILEMANAGER_FILENAME = 'filemanager.p'
SESSION_FILENAME = 'session.p'
DENDROGRAM_FILENAME = 'dendrogram.pdf'
DENDROGRAM_SVG_FILENAME = 'dendrogram.svg'
FILE_INFORMATION_FIGNAME = 'statistic.svg'
CORPUS_INFORMATION_FIGNAME = 'corpus_statistic.svg'
WORKSPACE_FILENAME = 'workspace.lexos'
KMEANS_GRAPH_FILENAME = 'kmeans.svg'
MALLET_INPUT_FILE_NAME = 'topicfile'
MALLET_OUTPUT_FILE_NAME = 'topicfile_for_json'
TOPWORD_CSV_FILE_NAME = 'topwordResult.csv'
DEBUG_LOG_FILE_NAME = 'debug.log'

'''constant numbers'''
MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024  # 1 GB
MAX_FILE_SIZE_INT = 1
MAX_FILE_SIZE_UNITS = "G"
PREVIEW_SIZE = 500  # note: number of characters in a preview screen (e.g., on Select page)
MIN_ENCODING_DETECT = 5000  # minimum number of characters used to detect a file's encoding scheme upon upload
MIN_NEWLINE_DETECT = 1000
CHARACTERS_PER_LINE_IN_LEGEND = 100
ROUND_DIGIT = 4

'''secret key <not functional for now>'''
FILEMANAGER_KEY = ''  # the key you use to encrypt your file manager
SESSION_KEY = ''  # the key you use to encrypt your session
FILE_CONTENT_KEY = ''  # the key you use to encrypt you file content

'''system type'''
'''(this can be printed well by system, therefore do not convert these object to json)'''
''' see debug.log for more '''
SYS_TYPE = {"<type 'int'>", "<type 'str'>", "<type 'list'>", "<type 'tuple'>", "<type 'float'>", "<type 'long'>",
            "<type 'NoneType'>"}

'''session caching option'''
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
    'rollinghasmilestone', 'hideDots',
    'BWoutput')  # if there is no comma in the end, python recognize this var as a string instead of a tuple
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
HIERARCHICALINPUT = ('metric', 'linkage', 'title', 'orientation', 'pruning', 'criterion')

# for kmeans Clustering
KMEANINPUT = ('nclusters', 'max_iter', 'init', 'n_init', 'tolerance', 'KMeans_metric', 'viz')
# for similarity query
SIMINPUT = ('uploadname',)
SIMBOX = ('simsuniquetokens',)

# for topword
TOPWORDINPUT = (
    'testMethodType', 'testInput', 'groupOptionType', 'outlierMethodType', "outlierTypeStd", "outlierTypeIQR",
    'lowerboundPC', 'upperboundPC', 'lowerboundRC', 'upperboundRC', 'useFreq')

# for statistic
STATISTIC_LIST = (
    'segmentlist',)  # if there is no comma in the end, python recognize this var as a string instead of a tuple

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

DEFAULT_ROLLINGWINDOW_OPTIONS = {'rollinghasmilestone': False, 'hideDots': False, 'BWoutput': False,
                                 'filetorollinganalyze': '', 'counttype': 'average',
                                 'windowtype': 'letter', 'inputtype': 'string', 'rollingsearchword': '',
                                 'rollingsearchwordopt': '',
                                 'rollingwindowsize': '', 'rollingmilestonetype': ''}

DEFAULT_ANALIZE_OPTIONS = {'tokenSize': '1', 'tokenType': 'word', 'normalizeType': 'freq', 'norm': 'l0',
                           'mfwcheckbox': False, 'mfwnumber': '1', 'cullcheckbox': False, 'cullnumber': '1',
                           'greyword': False}

DEFAULT_CLOUD_OPTIONS = {'segmentlist': []}

DEFAULT_MULTICLOUD_OPTIONS = {'optuploadname': '', 'analysistype': 'userfiles'}

DEFAULT_BUBBLEVIZ_OPTIONS = {'vizmaxwords': False, 'minlength': '0', 'graphsize': '800', 'maxwords': '100'}

DEFAULT_HIERARCHICAL_OPTIONS = {'metric': 'euclidean', 'linkage': 'average', 'title': '', 'orientation': 'top',
                                'pruning': '', 'augmented': True, 'criterion': 'maxclust', 'threshold': '',
                                'dendroLegends': False}

DEFAULT_KMEAN_OPTIONS = {'nclusters': '', 'max_iter': '', 'init': 'k-means++', 'n_init': '', 'tolerance': '',
                         'KMeans_metric': '', 'viz': 'Voronoi'}

DEFAULT_SIM_OPTIONS = {'uploadname': '', 'simsuniquetokens': True}

DEFAULT_TOPWORD_OPTIONS = {'testMethodType': 'pz', 'testInput': 'useclass', 'groupOptionType': 'all',
                           'outlierMethodType': 'stdErr', "outlierTypeStd": 'top', "outlierTypeIQR": 'top',
                           'lowerboundPC': '0', 'upperboundPC': '1', 'lowerboundRC': '0', 'upperboundRC': '0',
                           'useFreq': 'PC'}

DEFAULT_STATISTICS_OPTIONS = {}  # never used, go to lexos.py `statistic()` function to see why

'''do not cache options'''
SESSION_DO_NOT_CACHE = {}
WORKSPACE_DO_NOT_CACHE = {}
