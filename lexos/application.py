import json
import os
import re
import sys
import time

from flask import Flask, request, render_template
from jinja2 import evalcontextfilter
from markupsafe import Markup, escape

import lexos.helpers.constants
from lexos.helpers.exceptions import LexosException
from lexos.interfaces.base_interface import base_view
from lexos.interfaces.bubble_viz_interface import viz_view
from lexos.interfaces.clustering_interface import cluster_view
from lexos.interfaces.cut_interface import cutter_view
from lexos.interfaces.manage_interface import manage_view
from lexos.interfaces.multi_cloud_interface import multi_cloud_view
from lexos.interfaces.rolling_window_interface import rwa_view
from lexos.interfaces.scrub_interface import scrubber_view
from lexos.interfaces.similarity_query_interface import sim_view
from lexos.interfaces.statistics_interface import stats_view
from lexos.interfaces.tokenizer_interface import tokenizer_view
from lexos.interfaces.top_words_interface import top_words_view
from lexos.interfaces.upload_interface import upload_view
from lexos.interfaces.word_cloud_interface import word_cloud_view


def get_secret_key(file_name: str = 'secret_key') -> bytes:
    """Creates an encryption key for a secure session.

    :param: file_name: A string representing the secret key.
    :return: the bytes of the secret key
    """
    file_full_name = os.path.join(app.static_folder, file_name)

    if os.path.isfile(file_full_name):
        return open(file_full_name, 'rb').read()

    else:
        print('secret key not found, creating secret key')

        # create secrete key
        open(file_full_name, 'wb').write(os.urandom(24))

        return open(file_full_name, 'rb').read()


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config['MAX_CONTENT_LENGTH'] = lexos.helpers.constants.MAX_FILE_SIZE
app.config['SECRET_KEY'] = get_secret_key()
# open debugger when we are not on the server
app.debug = not lexos.helpers.constants.IS_SERVER
app.jinja_env.filters['type'] = type
app.jinja_env.filters['str'] = str
app.jinja_env.filters['tuple'] = tuple
app.jinja_env.filters['len'] = len
app.jinja_env.filters['unicode'] = str
app.jinja_env.filters['time'] = time.time()

# register all the blue prints
# they helps us to manage groups of views
# see here for more detail:
# http://exploreflask.com/en/latest/blueprints.html
# http://flask.pocoo.org/docs/0.12/blueprints/
app.register_blueprint(base_view)
app.register_blueprint(upload_view)
app.register_blueprint(manage_view)
app.register_blueprint(viz_view)
app.register_blueprint(cluster_view)
app.register_blueprint(cutter_view)
app.register_blueprint(multi_cloud_view)
app.register_blueprint(rwa_view)
app.register_blueprint(scrubber_view)
app.register_blueprint(sim_view)
app.register_blueprint(stats_view)
app.register_blueprint(tokenizer_view)
app.register_blueprint(top_words_view)
app.register_blueprint(word_cloud_view)


# http://flask.pocoo.org/snippets/28/
# http://stackoverflow.com/questions/12523725/
# why-is-this-jinja-nl2br-filter-escaping-brs-but-not-ps
@app.template_filter()  # Register template filter
@evalcontextfilter  # Add attribute to the evaluation time context filter
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


# ==== add error handlers ====
@app.errorhandler(404)
def page_not_found(_):
    """Custom 404 Page"""
    app.logger.error('Page not found: %s', request.path)
    return render_template('404.html'), 404


@app.errorhandler(Exception)
def unhandled_exception(error):
    """handles internal server errors

    Send all the LexosException to the frontend.
    For all the other Exceptions,
    we will just render the internal server error (500) page.
    """
    # if we want to send this backend error to the front end
    if isinstance(error, LexosException):
        ret_data = {"lexosException": str(error)}
        return json.dumps(ret_data)

    # if flask raises this error
    else:
        render_template("500.html")


def run():
    """Run lexos."""
    try:
        sys.exit(app.run())
    except KeyboardInterrupt:
        print('Exiting lexos. Bye!')

