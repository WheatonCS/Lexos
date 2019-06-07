import os


def get_phylotree(nwk_tree):
    current_dir = os.path.dirname(__file__)
    filepath = os.path.join(current_dir + '/../templates', 'phylotree.html')
    with open(filepath, 'r') as file:
        phylo_html = file.read()
    # Make content div visible
    phylo_html = phylo_html.replace(
        '<div id="content" style="display: none">',
        '<div id="content" style="display: inline">')
    nwk_tree = nwk_tree.replace("\n", "")
    if ";" in nwk_tree:
        nwk_tree = nwk_tree.replace(";", "")
    # insert graph in newick format
    return phylo_html.replace("let test_string = '()'",
                              "let test_string ='" +
                              nwk_tree[:-1] + "'")
