from flask import session, Blueprint
#flask jsonify
#from lexos.managers import session_manager
from lexos.helpers import constants as constants
#from lexos.models.classifier_model import ClassifierModel
from lexos.views.base import render

classify_blueprint = Blueprint("classify", __name__)


@classify_blueprint.route("/classify", methods=["GET"])
def classifier():
    """ Gets the classifier page.
    :return: The classifier page.
    """
    session["analyoption"] = constants.DEFAULT_ANALYZE_OPTIONS

    # Send the page.
    return render("classify.html")
