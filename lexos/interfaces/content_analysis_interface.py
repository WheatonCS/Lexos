import json
from natsort import natsorted

from flask import send_file, request, session, render_template, Blueprint

from lexos.helpers import constants as constants
from lexos.managers import session_manager as session_manager, utility
from lexos.interfaces.base_interface import detect_active_docs
from lexos.models.content_analysis_model import ContentAnalysisModel
# this is a flask blue print
# it helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
content_analysis_view = Blueprint('content_analysis', __name__)


# Tells Flask to load this function when someone is at '/contentanalysis'
@content_analysis_view.route("/contentanalysis", methods=["GET", "POST"])
def content_analysis():
    analysis = ContentAnalysisModel()
    # Detect the number of active documents.
    num_active_docs = detect_active_docs()

    file_manager = utility.load_file_manager()
    labels = file_manager.get_active_labels()
    files = file_manager.get_active_files()

    for file in files:
        analysis.add_corpus(file)

    if request.method == 'GET':
        # 'GET' request occurs when the page is first loaded

        return render_template('contentanalysis.html')
    else:
        for upload_file in request.files.getlist('lemfileselect[]'):
            analysis.add_dictionary(upload_file.filename, upload_file.read())
        analysis.count_words()
        analysis.generate_scores(analysis.dictionaries_labels,
                                 ['x', 'x', 'x', 'x'], ['1', '1', '1', '1'],
                                 ['+', '+', '+', '+'])
        analysis.display()
        results = [analysis.to_html()]
        data = {"data": results}
        data = json.dumps(data)
        return data


