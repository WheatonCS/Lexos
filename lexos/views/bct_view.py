from flask import session, render_template, Blueprint
from lexos.helpers import constants
from lexos.views.base_view import detect_active_docs
from lexos.models.filemanager_model import FileManagerModel

# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
bct_analysis_blueprint = Blueprint('bct_analysis', __name__)


@bct_analysis_blueprint.route("/bct_analysis", methods=['GET'])
def bct_analysis():
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()
    # Get labels with their ids.
    id_label_map = \
        FileManagerModel().load_file_manager().get_active_labels_with_id()

    # Fill in default options.
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALYZE_OPTIONS
    if 'hierarchyoption' not in session:
        session['bctoption'] = constants.DEFAULT_BCT_OPTIONS

    # Render the HTML template.
    return render_template(
        'bct_analysis.html',
        itm="bct-analysis",
        labels=id_label_map,
        numActiveDocs=num_active_docs
    )


@bct_analysis_blueprint.route("/bct_analysis", methods=['POST'])
def get_bct_result():
