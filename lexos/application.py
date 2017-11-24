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
from lexos.views.base_view import base_blueprint
from lexos.views.bubble_view import viz_blueprint
from lexos.views.cut_view import cutter_blueprint
from lexos.views.dendrogram_view import dendrogram_blueprint
from lexos.views.k_means_view import k_means_blueprint
from lexos.views.manage_view import manage_blueprint
from lexos.views.multi_cloud_view import multi_cloud_blueprint
from lexos.views.rolling_window_view import rwa_blueprint
from lexos.views.scrub_view import scrubber_blueprint
from lexos.views.similarity_query_view import sim_blueprint
from lexos.views.statistics_view import stats_blueprint
from lexos.views.tokenizer_view import tokenizer_blueprint
from lexos.views.top_words_view import top_words_blueprint
from lexos.views.upload_view import upload_blueprint
from lexos.views.word_cloud_view import word_cloud_blueprint


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
app.register_blueprint(base_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(manage_blueprint)
app.register_blueprint(viz_blueprint)
app.register_blueprint(k_means_blueprint)
app.register_blueprint(dendrogram_blueprint)
app.register_blueprint(cutter_blueprint)
app.register_blueprint(multi_cloud_blueprint)
app.register_blueprint(rwa_blueprint)
app.register_blueprint(scrubber_blueprint)
app.register_blueprint(sim_blueprint)
app.register_blueprint(stats_blueprint)
app.register_blueprint(tokenizer_blueprint)
app.register_blueprint(top_words_blueprint)
app.register_blueprint(word_cloud_blueprint)


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
    app.logger.error('\nPage not found: {url}'.format(url=request.path))
    return render_template('404.html')


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
        raise error


def run():
    """Run lexos."""
    try:
        sys.exit(app.run())
    except KeyboardInterrupt:
        print('Exiting lexos. Bye!')
