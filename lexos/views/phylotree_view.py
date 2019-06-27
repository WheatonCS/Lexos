import os


def get_phylotree(nwk_tree):
    """
        :param nwk_tree: A str containing a tree in Newick format
        :return: phylotree in html
    """
    current_dir = os.path.dirname(__file__)
    filepath = os.path.join(current_dir + '/../templates', 'phylotree.html')
    with open(filepath, 'r') as file:
        phylo_html = file.read()
    # Make content div visible
    phylo_html = phylo_html.replace(
        'style="display: none"',
        'style="display: inline"')
    nwk_tree = nwk_tree.replace("\n", "")
    if ";" in nwk_tree:
        nwk_tree = nwk_tree.replace(";", "")
    # insert graph in newick format
    return phylo_html.replace("let nwk_string = '()'",
                              "let nwk_string ='" +
                              nwk_tree[:-1] + "'")
