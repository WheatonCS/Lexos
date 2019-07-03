import json
import pandas as pd
from flask import Blueprint, request
from lexos.managers import utility
from lexos.views.base import render

bubbleviz_blueprint = Blueprint("bubbleviz", __name__)


@bubbleviz_blueprint.route("/bubbleviz", methods=["GET"])
def viz():
    """ Gets the bubbleviz page.
    :return: The bubbleviz page.
    """

    return render("bubbleviz.html")


@bubbleviz_blueprint.route("/bubbleviz/get-word-counts", methods=["POST"])
def get_word_counts() -> str:
    """ Gets the top 100 word counts across all active files.
    :return: The top 100 word counts across all active files.
    """

    file_manager = utility.load_file_manager()

    # Get the contents of the active documents
    contents = ""
    for file in file_manager.files.values():
        if file.active:
            contents += file.load_contents()

    # If there are no active documents or contents, return an empty array
    if not contents:
        return "[]"

    # Get a sorted dataframe of word counts
    dtm, words = utility.simple_vectorizer([contents], "word", 1)
    dataframe = pd.DataFrame({"word": words, "count": dtm[0]})
    dataframe = dataframe.sort_values(by="count", ascending=False)

    # Create a list of the top 100 words and their normalized counts
    response = []
    maximum_top_words = int(request.get_json()["maximum_top_words"])
    maximum_count = dataframe.iloc[0]["count"]
    dataframe = dataframe[:maximum_top_words]

    for i in range(len(dataframe)):
        response.append({"word": dataframe.iloc[i]["word"],
                         "count": str(dataframe.iloc[i]["count"]),
                         "value": dataframe.iloc[i]["count"]/maximum_count})

    return json.dumps(response)
