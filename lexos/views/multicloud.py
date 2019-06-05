import json

import pandas as pd
from flask import session, render_template, Blueprint

from lexos.helpers import constants as constants
from lexos.managers import utility, session_manager as session_manager

multicloud_blueprint = Blueprint("multicloud", __name__)


@multicloud_blueprint.route("/multicloud", methods=["GET"])
def multicloud() -> str:
    """Gets the multicloud page.
    :return: The multicloud page.
    """

    # Sets the cloud and multicloud options to their defaults if they do not
    # exist
    if "cloudoption" not in session:
        session["cloudoption"] = constants.DEFAULT_CLOUD_OPTIONS
    if "multicloudoptions" not in session:
        session["multicloudoptions"] = constants.DEFAULT_MULTICLOUD_OPTIONS

    return render_template("multicloud.html")


@multicloud_blueprint.route("/multicloud/get-word-counts", methods=["GET"])
def get_word_counts() -> str:
    """ Gets the top 100 word counts for each active file.

    :return: The top 100 word counts for each active file.
    """

    file_manager = utility.load_file_manager()
    session_manager.cache_cloud_option()

    # Get the contents of the active documents
    response = []
    for file in file_manager.files.values():
        if file.active:
            response.append({"name": file.label,
                             "words": get_word_counts_single_file(
                                 file.load_contents())})

    return json.dumps(response)


def get_word_counts_single_file(contents) -> list:
    """ Gets the top 100 word counts for the given contents.

    :param contents: The words to count.
    :return: The top 100 word counts.
    """

    # Get a sorted dataframe of word counts
    dtm, words = utility.simple_vectorizer([contents], "word", 1)
    dataframe = pd.DataFrame({"word": words, "count": dtm[0]})
    dataframe = dataframe.sort_values(by="count", ascending=False)

    # Create a list of the top 100 words and their normalized counts
    top_words = []
    maximum = dataframe.iloc[0]["count"]
    dataframe = dataframe[:100]
    for i in range(len(dataframe)):
        top_words.append([dataframe.iloc[i]["word"],
                          dataframe.iloc[i]["count"]/maximum])

    return top_words
