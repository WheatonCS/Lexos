import os
import re
import sys
import time

from flask import Flask, request, jsonify
from jinja2 import evalcontextfilter
from markupsafe import Markup, escape

import lexos.helpers.constants
from lexos.views.base import render

from lexos.views.base import base_blueprint
from lexos.views.bubbleviz import bubbleviz_blueprint
from lexos.views.consensus_tree import consensus_tree_blueprint
from lexos.views.content_analysis import content_analysis_blueprint
from lexos.views.cut import cut_blueprint
from lexos.views.dendrogram import dendrogram_blueprint
from lexos.views.k_means import k_means_blueprint
from lexos.views.manage import manage_blueprint
from lexos.views.multicloud import multicloud_blueprint
from lexos.views.rolling_window import rolling_window_blueprint
from lexos.views.scrub import scrub_blueprint
from lexos.views.similarity_query import similarity_query_blueprint
from lexos.views.statistics import statistics_blueprint
from lexos.views.tokenize import tokenize_blueprint
from lexos.views.top_words import top_words_blueprint
from lexos.views.upload import upload_blueprint
from lexos.views.word_cloud import word_cloud_blueprint
from lexos.views.classifier import classifier_blueprint


def get_secret_key(file_name: str = "secret_key") -> bytes:
    """Creates an encryption key for a secure session.

    :param: file_name: A string representing the secret key.
    :return: the bytes of the secret key
    """

    file_full_name = os.path.join(app.static_folder, file_name)

    if os.path.isfile(file_full_name):
        return open(file_full_name, "rb").read()

    else:
        print("The secret key was not found. Creating a secret key.")

        # Create secrete key
        open(file_full_name, "wb").write(os.urandom(24))

        return open(file_full_name, "rb").read()


app = Flask(__name__, static_folder="frontend",
            template_folder="frontend/html")
app.config.from_pyfile("config.cfg")
app.config["MAX_CONTENT_LENGTH"] = lexos.helpers.constants.MAX_FILE_SIZE
app.config["SECRET_KEY"] = get_secret_key()

# Open the debugger when we are not on the server
app.debug = not lexos.helpers.constants.IS_SERVER
app.jinja_env.filters["type"] = type
app.jinja_env.filters["str"] = str
app.jinja_env.filters["tuple"] = tuple
app.jinja_env.filters["len"] = len
app.jinja_env.filters["unicode"] = str
app.jinja_env.filters["time"] = time.time()

# Register the blueprints
app.register_blueprint(base_blueprint)
app.register_blueprint(bubbleviz_blueprint)
app.register_blueprint(consensus_tree_blueprint)
app.register_blueprint(content_analysis_blueprint)
app.register_blueprint(cut_blueprint)
app.register_blueprint(dendrogram_blueprint)
app.register_blueprint(k_means_blueprint)
app.register_blueprint(manage_blueprint)
app.register_blueprint(multicloud_blueprint)
app.register_blueprint(rolling_window_blueprint)
app.register_blueprint(scrub_blueprint)
app.register_blueprint(similarity_query_blueprint)
app.register_blueprint(statistics_blueprint)
app.register_blueprint(tokenize_blueprint)
app.register_blueprint(top_words_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(word_cloud_blueprint)
app.register_blueprint(classifier_blueprint)


@app.template_filter()  # Register the template filter
@evalcontextfilter  # Add an attribute to the evaluation time context filter
def nl2br(eval_ctx, value):
    """
    Wraps a string value in HTML <p> tags and replaces internal new line
    esacapes with <br/>. Since the result is a markup tag, the Markup()
    function temporarily disables Jinja2's autoescaping in the evaluation time
    context when it is returned to the template.
    """

    _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
    result = '\n\n'.join('<p>%s</p>' % p.replace('\n', Markup('<br/>\n'))
                         for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


# Add error handlers
@app.errorhandler(404)
def page_not_found(_):
    """Custom 404 Page"""

    app.logger.error("\nPage not found: {url}".format(url=request.path))
    return render("404.html")


@app.errorhandler(Exception)
def unhandled_exception(error):
    """Handles internal server errors."""
    return jsonify({"error": str(error)})


def run():
    """Runs Lexos."""
    try:
        sys.exit(app.run())

    except KeyboardInterrupt:
        print("Exiting Lexos. Bye!")
