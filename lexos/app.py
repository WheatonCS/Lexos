import re
import time

import os

import sys
from flask import Flask
from jinja2 import evalcontextfilter
from markupsafe import Markup, escape
import lexos.helpers.constants
from lexos.interfaces.base_interface import base_view
from lexos.interfaces.upload_interface import upload_view
from lexos.interfaces.manage_interface import manage_view
from lexos.interfaces.bubble_viz_interface import viz_view
from lexos.interfaces.clustering_interface import cluster_view
from lexos.interfaces.cut_interface import cutter_view
from lexos.interfaces.multi_cloud_interface import multi_cloud_view
from lexos.interfaces.rolling_window_interface import rwa_view
from lexos.interfaces.scrub_interface import scrubber_view
from lexos.interfaces.similarity_query_interface import sim_view
from lexos.interfaces.statistics_interface import stats_view
from lexos.interfaces.tokenizer_interface import tokenizer_view
from lexos.interfaces.top_words_interface import top_words_view
from lexos.interfaces.word_cloud_interface import word_cloud_view


def install_secret_key(file_name='secret_key'):
    """
    Creates an encryption key for a secure session.
    Args:
        file_name: A string representing the secret key.
    Returns:
        None
    """
    file_name = os.path.join(app.static_folder, file_name)
    try:
        app.config['SECRET_KEY'] = open(file_name, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        if not os.path.isdir(os.path.dirname(file_name)):
            print('mkdir -p', os.path.dirname(file_name))
        print('head -c 24 /dev/urandom >', file_name)
        sys.exit(1)


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config['MAX_CONTENT_LENGTH'] = lexos.helpers.constants.MAX_FILE_SIZE
# open debugger when we are not on the server
app.debug = not lexos.helpers.constants.IS_SERVER
app.jinja_env.filters['type'] = type
app.jinja_env.filters['str'] = str
app.jinja_env.filters['tuple'] = tuple
app.jinja_env.filters['len'] = len
app.jinja_env.filters['unicode'] = str
app.jinja_env.filters['time'] = time.time()
install_secret_key()  # create the secret key

# register all the blue prints
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


def int_key(s):
    """
    Returns the key to sort by.

    Args:
        A key

    Returns:
        A key converted into an int if applicable
    """
    if isinstance(s, tuple):
        s = s[0]
    return tuple(int(part) if re.match(r'[0-9]+$', part) else part
                 for part in re.split(r'([0-9]+)', s))


@app.template_filter('natsort')
def natsort(l):
    """
    Sorts lists in human order (10 comes after 2, even when both are strings)

    Args:
        A list

    Returns:
        A sorted list
    """
    return sorted(l, key=int_key)


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


if __name__ == '__main__':
    app.run()
