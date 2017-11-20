from flask import session, render_template, Blueprint

from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager
from lexos.models.filemanager_model import FileManagerModel
from lexos.models.similarity_model import SimilarityModel
from lexos.views.base_view import detect_active_docs

# this is a flask blue print, it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
sim_blueprint = Blueprint('sim_query', __name__)


# Tells Flask to load this function when someone is at '/extension'
@sim_blueprint.route("/similarity", methods=["GET"])
def similarity():
    """Handles the similarity query page functionality.

    Returns ranked list of files and their cosine similarities to a comparison
    document.
    :return: a response object (often a render_template call) to flask and
    eventually to the browser.
    """
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    id_label_map = \
        FileManagerModel().load_file_manager().get_active_labels_with_id()

    # 'GET' request occurs when the page is first loaded
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
    if 'similarities' not in session:
        session['similarities'] = constants.DEFAULT_SIM_OPTIONS
    return render_template(
        'similarity.html',
        labels=id_label_map,
        similaritiesgenerated=False,
        numActiveDocs=num_active_docs)


@sim_blueprint.route("/similarityHTML", methods=['POST'])
def sim_html():
    session_manager.cache_analysis_option()
    session_manager.cache_sim_options()
    return SimilarityModel().generate_sims_html()
