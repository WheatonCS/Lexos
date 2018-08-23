"""This is a model to produce bootstrap consensus tree of the dtm."""

import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Bio import Phylo
from io import StringIO, BytesIO
from skbio import TreeNode
from skbio.tree import majority_rule
from scipy.cluster.hierarchy import linkage
from typing import NamedTuple, Optional, List
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel, IdTempLabelMap
from lexos.receivers.bct_receiver import BCTOption, BCTReceiver

# Make plt to use a non-interactive backend to generate PNG instead of window.
plt.switch_backend("Agg")


class BCTTestOptions(NamedTuple):
    """A typed tuple to hold test options."""

    doc_term_matrix: pd.DataFrame
    front_end_option: BCTOption
    id_temp_label_map: IdTempLabelMap


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
            self._test_id_temp_label_map = test_options.id_temp_label_map
        else:
            self._test_dtm = None
            self._test_front_end_option = None
            self._test_id_temp_label_map = None

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:
        """:return: the document term matrix."""
        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _id_temp_label_map(self) -> IdTempLabelMap:
        """:return: a map takes an id to temp labels."""
        return self._test_id_temp_label_map \
            if self._test_id_temp_label_map is not None \
            else MatrixModel().get_id_temp_label_map()

    @property
    def _bct_option(self) -> BCTOption:
        """:return: the front end option of bootstrap consensus tree."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else BCTReceiver().options_from_front_end()

    def _get_newick_tree(self,
                         labels: List[str],
                         sample_dtm: pd.DataFrame) -> TreeNode:
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

        # Convert linkage matrix to a tree node and return it.
        return TreeNode.from_linkage_matrix(
            linkage_matrix=linkage_matrix,
            id_list=labels
        )

    def _get_bootstrap_trees(self) -> List[TreeNode]:
        """Do bootstrap on the DTM to get a list of newick trees.

        :return: A list of newick formatted tree where each tree was based on
                 a 80% subset of the complete DTM.
        """
        # Get file names, since tree nodes need labels.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # The bootstrap process to get all the trees.
        return [
            self._get_newick_tree(
                sample_dtm=self._doc_term_matrix.sample(
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
        # Create the StringIO newick tree holder.
        newick_tree = StringIO()

        # Find the consensus tree among all trees.
        consensus_tree = majority_rule(
            trees=self._get_bootstrap_trees(),
            cutoff=self._bct_option.cutoff
        )

        # Grab the tree from the returned list and convert it to newick format.
        consensus_tree[0].write(newick_tree)
        consensus_tree_str = newick_tree.getvalue()

        # Return consensus tree as a ETE tree object.
        return Phylo.read(
            StringIO(consensus_tree_str),
            format="newick"
        )

    def _get_bootstrap_consensus_tree_plot(self) -> plt:
        # Draw the consensus tree as a matplotlib object.
        Phylo.draw(
            self._get_bootstrap_consensus_tree(),
            do_show=False,
            show_confidence=True,
            branch_labels=lambda clade: "{0:.4f}\n".format(clade.branch_length)
            if clade.branch_length is not None else ""
        )

        # Set labels for the plot.
        plt.xlabel("Branch Length")
        plt.ylabel("Texts")

        # Hide the two unused border.
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)

        # Extend x-axis to the right to fit longer labels.
        x_left, x_right, y_low, y_high = plt.axis()
        plt.axis((x_left, x_right * 1.25, y_low, y_high))

        # Set graph size, title and tight layout.
        plt.gcf().set_size_inches(
            w=9.5,
            h=(len(self._id_temp_label_map) * 0.5)
        )
        plt.title("Bootstrap Consensus Tree Result")
        plt.gcf().tight_layout()

        # Change line spacing
        for text in plt.gca().texts:
            text.set_linespacing(spacing=0.1)

        return plt

    def get_bootstrap_consensus_tree_plot_decoded(self) -> str:
        """Render the bootstrap consensus tree result and save it to images.

        :return: The rendered BCT result file name.
        """
        # Get the matplotlib plot for bootstrap consensus tree result.
        bct_plot = self._get_bootstrap_consensus_tree_plot()

        # Create a bytes IO image holder and save figure to it.
        image_holder = BytesIO()
        bct_plot.savefig(image_holder)
        image_holder.seek(0)

        # Decode image to utf-8 string.
        return base64.b64encode(b''.join(image_holder)).decode('utf-8')
