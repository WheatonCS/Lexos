from flask import render_template, Blueprint

consensus_tree_blueprint = Blueprint("consensus-tree", __name__)


@consensus_tree_blueprint.route("/consensus-tree", methods=["GET"])
def consensus_tree() -> str:
    """Gets the consensus tree page.
    :return: The consensus tree page.
    """

    # Return the consensus tree page
    return render_template("consensus-tree.html")
