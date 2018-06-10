SEG_NON_POSITIVE_MESSAGE = "The segment size must be a positive integer"
OVERLAP_LARGE_MESSAGE = "The segment size must be greater than " \
    "the overlap of words between chunks"
PROP_NEGATIVE_MESSAGE = "The proportional size of the last segment must be " \
    "zero or greater"
OVERLAP_NEGATIVE_MESSAGE = "The overlap between segments must be zero or " \
                           "greater"
NON_POSITIVE_SEGMENT_MESSAGE = "the segment size should be positive"
NEG_OVERLAP_LAST_PROP_MESSAGE = "the overlap or last segment proportion" \
                                "should not be negative"
LARGER_SEG_SIZE_MESSAGE = "the segment size should be larger " \
    "than the overlap size"
NON_NEGATIVE_INDEX_MESSAGE = "the index should be larger than or equal to zero"
MATRIX_DIMENSION_UNEQUAL_MESSAGE = "the dimension of the matrix " \
    "should be equal"
EMPTY_LIST_MESSAGE = "the list should not be empty"
WINDOW_SIZE_LARGE_MESSAGE = "The window size must be less than or equal to" \
                            " the length of the given document"
INVALID_CUTTING_TYPE_MESSAGE = "the cutting type should be letters, lines, " \
    "number, words or milestone"
EMPTY_MILESTONE_MESSAGE = "the milestone should not be empty"
EMPTY_NP_ARRAY_MESSAGE = "The input numpy array should not be empty, since" \
    "the input file should not be empty."
NOT_ONE_REPLACEMENT_COLON_MESSAGE = "Invalid number of colons: "
REPLACEMENT_RIGHT_OPERAND_MESSAGE = "Too many values on right side of " \
                                    "replacement string: "
REPLACEMENT_NO_LEFTHAND_MESSAGE = "Missing value on the left side of " \
                                  "replacement string: "
EMPTY_STRING_MESSAGE = "the string should not be empty"
WINDOW_NON_POSITIVE_MESSAGE = "The window size must be a positive integer"

# ============= General Erros ===============================
EMPTY_DTM_MESSAGE = "Empty DTM received, please upload files."


# ============= Base Model Errors ===========================
NO_DATA_SENT_ERROR_MESSAGE = 'Front end did not send data to backend'
INVALID_DATA_KEY_MESSAGE_FORMAT = \
    'no data with name {data_key} sended to backend'

# ============= Topword Model Error =========================
NOT_ENOUGH_CLASSES_MESSAGE = "Only one class given, cannot do Z-test by " \
                             "class, at least 2 classes needed."
