"""This is a model to produce bootstrap consensus tree of the dtm."""

import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO, BytesIO
from Bio import Phylo
from Bio.Phylo.Consensus import majority_consensus
from scipy.cluster.hierarchy import linkage, to_tree, ClusterNode
from typing import NamedTuple, Optional, List
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import DocumentLabelMap
from lexos.receivers.consensus_tree_receiver import BCTOption, BCTReceiver
import lexos.managers.utility as utility


# Make plt to use a non-interactive backend to generate PNG instead of window.
plt.switch_backend("Agg")


class BCTTestOptions(NamedTuple):
    """A named tuple to hold test options."""

    doc_term_matrix: pd.DataFrame
    front_end_option: BCTOption
    document_label_map: DocumentLabelMap


class BCTModel(BaseModel):
    """The BCTModel inherits from the BaseModel."""

    def __init__(self, test_options: Optional[BCTTestOptions] = None):
        """Generate bootstrap consensus tree.

        :param test_options: The input used in testing to override the
                             dynamically loaded option.
        """
        super().__init__()
        if test_options is not None:
            self._test_dtm = test_options.doc_term_matrix
            self._test_front_end_option = test_options.front_end_option
            self._test_document_label_map = test_options.document_label_map
        else:
            self._test_dtm = None
            self._test_front_end_option = None
            self._test_document_label_map = None

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:
        """:return: the document term matrix."""
        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _document_label_map(self) -> DocumentLabelMap:
        """:return: a map takes an id to temp labels."""
        return self._test_document_label_map \
            if self._test_document_label_map is not None \
            else utility.get_active_document_label_map()

    @property
    def _bct_option(self) -> BCTOption:
        """:return: the front end option of bootstrap consensus tree."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else BCTReceiver().options_from_front_end()

    @staticmethod
    def linkage_to_newick(matrix: np.ndarray, labels: List[str]):
        """Convert a linkage matrix to a newick formatted tree.

        :param matrix: The linkage matrix.
        :param labels: Names of the tree node.
        :return: The newick representation of the linkage matrix.
        """
        # Convert the linkage matrix to a ClusterNode object.
        tree = to_tree(matrix, False)

        # Define the helper recursive function to build the newick tree.
        def _build_newick_tree(node: ClusterNode,
                               newick: str,
                               parent_dist: float,
                               leaf_names: List[str]) -> str:
            """Recursively build the newick tree.

            :param node: The tree node currently being converted to.
            :param newick: The current newick representation of the tree.
            :param parent_dist: The distance to parent node.
            :param leaf_names: Names of the tree node.
            :return:
            """
            # If node is leaf, enclose.
            if node.is_leaf():
                return f"{leaf_names[node.id]}" \
                    f":{(parent_dist - node.dist) / 2}{newick}"
            else:
                # Write the distance.
                newick = f"):{(parent_dist - node.dist) / 2}{newick}" \
                    if len(newick) > 0 else ");"
                # Recursive call to expand the tree.
                newick = _build_newick_tree(
                    newick=newick,
                    node=node.get_left(),
                    parent_dist=node.dist,
                    leaf_names=leaf_names)
                newick = _build_newick_tree(
                    newick=f",{newick}",
                    node=node.get_right(),
                    parent_dist=node.dist,
                    leaf_names=leaf_names)
                # Enclose the tree at the beginning.
                return f"({newick}"

        # Trigger the recursive function.
        return _build_newick_tree(
            node=tree, newick="", parent_dist=tree.dist, leaf_names=labels)

    def _get_newick_tree(self,
                         labels: List[str],
                         sample_dtm: pd.DataFrame) -> str:
        """Get newick tree based on a subset of the DTM.

        :param labels: All file names from the DTM.
        :param sample_dtm: A 80% subset of the complete DTM.
        :return: A newick formatted tree representing the DTM subset.
        """
        # noinspection PyTypeChecker
        # Get the linkage matrix for the sample doc term matrix.
        linkage_matrix = linkage(
            sample_dtm.values,
            metric=self._bct_option.dist_metric,
            method=self._bct_option.linkage_method
        )

        # Get the newick representation of the tree.
        newick = self.linkage_to_newick(matrix=linkage_matrix, labels=labels)

        # Convert linkage matrix to a tree node and return it.
        return Phylo.read(StringIO(newick), format="newick")

    def _get_bootstrap_trees(self) -> List[str]:
        """Do bootstrap on the DTM to get a list of newick trees.

        :return: A list of newick formatted tree where each tree was based on
                 a 80% subset of the complete DTM.
        """
        # Save the DTM to avoid multiple calls.
        doc_term_matrix = self._doc_term_matrix

        # Get file names, since tree nodes need labels.
        labels = [self._document_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # The bootstrap process to get all the trees.
        return [
            self._get_newick_tree(
                sample_dtm=doc_term_matrix.sample(
                    axis=1,
                    frac=0.8,
                    replace=self._bct_option.replace,
                    random_state=np.random.RandomState()
                ),
                labels=labels,
            )
            for _ in range(self._bct_option.iterations)
        ]

    def _get_bootstrap_consensus_tree(self) -> Phylo:
        """Get the consensus tree.

        :return: The consensus tree of the list of newick trees.
        """
        # Find the consensus of all the newick trees.
        return majority_consensus(
            trees=self._get_bootstrap_trees(),
            cutoff=self._bct_option.cutoff
        )

    def _get_bootstrap_consensus_tree_plot(self) -> plt:

        # Get the colors
        color = tuple(map(int, self._bct_option.text_color[4:-1].split(",")))
        normalized_color = tuple(x / 255 for x in color)

        # Draw the consensus tree as a MatPlotLib object.
        tree = self._get_bootstrap_consensus_tree()
        tree.root.color = color
        Phylo.draw(
            tree,
            do_show=False,
            branch_labels=lambda clade: "{0:.4f}\n".format(clade.branch_length)
            if clade.branch_length is not None else ""
        )

        # Set labels for the plot.
        plt.xlabel("Branch Length", color=normalized_color)
        plt.ylabel("Documents", color=normalized_color)

        # Hide the two unused border.
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)

        # Set the color of the used borders and labels.
        plt.gca().spines["bottom"].set_color(normalized_color)
        plt.gca().spines["left"].set_color(normalized_color)
        plt.gca().tick_params(colors=normalized_color)

        # Extend x-axis to the right to fit longer labels.
        x_left, x_right, y_low, y_high = plt.axis()
        plt.axis((x_left, x_right * 1.25, y_low, y_high))

        # Set graph size, title and tight layout.
        plt.gcf().set_size_inches(
            w=9.5,
            h=(len(self._document_label_map) * 0.3 + 1)
        )
        plt.title("Bootstrap Consensus Tree Result", color=normalized_color)
        plt.gcf().tight_layout()

        # Change line spacing
        for text in plt.gca().texts:
            text.set_linespacing(spacing=0.1)
            text.set_color(normalized_color)

        return plt

    def get_bootstrap_consensus_tree_plot_decoded(self) -> str:
        """Render the bootstrap consensus tree result and save it to images.

        :return: The rendered BCT result file name.
        """
        # Get the matplotlib plot for bootstrap consensus tree result.
        bct_plot = self._get_bootstrap_consensus_tree_plot()

        # Create a bytes IO image holder and save figure to it.
        image_holder = BytesIO()
        bct_plot.savefig(image_holder, transparent=True)
        image_holder.seek(0)

        # Decode image to utf-8 string.
        return base64.b64encode(b''.join(image_holder)).decode('utf-8')
