from flask import session, Blueprint
from lexos.helpers import constants as constants
from lexos.views.base import render

"""flask jsonify
from lexos.managers import session_manager
from lexos.models.classifier_model import ClassifierModel
"""

classifier_blueprint = Blueprint("classifier", __name__)


@classifier_blueprint.route("/classifier", methods=["GET"])
def classifier():
    """ Gets the classifier page.
    :return: The classifier page.
    """
    session["analyoption"] = constants.DEFAULT_ANALYZE_OPTIONS

    # Send the page.
    return render("classifier.html")

@classifier_blueprint.route("/classifier/prediction-statistics",
                            methods=["POST"])
def predictions() -> str:
    """Get the statistics of the prediction trials.
    :return: The statistics of the prediction trials.
    """

    session_manager.cache_analysis_option()
    return jsonify(StatsModel().get_document_statistics())