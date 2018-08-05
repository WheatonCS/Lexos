"""This is a model to produce bootstrap consensus tree of the dtm."""

import datetime
import numpy as np
import pandas as pd
from io import StringIO
from skbio import TreeNode
from skbio.tree import majority_rule
from ete3 import TreeStyle, Tree
from scipy.cluster.hierarchy import linkage
from typing import NamedTuple, Optional, List
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel, IdTempLabelMap
from lexos.receivers.bct_receiver import BCTOption, BCTReceiver


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
                    random_state=np.random.RandomState()
                ),
                labels=labels,
            )
            for _ in range(self._bct_option.iterations)
        ]

    def _get_bootstrap_consensus_tree(self):
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

        # Return consensus tree as a ETE tree object.
        return Tree(
            newick_tree.getvalue(),
            quoted_node_names=True
        )

    @staticmethod
    def _get_ete_tree_style() -> TreeStyle:
        """

        :return:
        """
        # Set up a ete tree style object.
        tree_style = TreeStyle()
        tree_style.mode = "c"
        tree_style.scale = None
        tree_style.arc_span = 360
        tree_style.arc_start = 0
        tree_style.show_scale = False
        tree_style.show_leaf_name = True
        tree_style.show_branch_length = True
        tree_style.branch_vertical_margin = 10
        return tree_style

    def get_bootstrap_consensus_result(self) -> str:
        """Draw the bootstrap consensus tree result.

        :return:
        """
        # TODO: this method is hack.. Seeking for better solution.
        # Get the current time to help distinguish pictures.
        current_time = datetime.datetime.now().isoformat()
        result_file_name = f"bct_result{current_time}.png"

        # Get the ete formatted consensus tree.
        consensus_tree = self._get_bootstrap_consensus_tree()

        consensus_tree.render(
            tree_style=self._get_ete_tree_style(),
            file_name=f"lexos/static/images/{result_file_name}",
            units="px",
            dpi=300,
            h=1000,
            w=1000
        )

        return result_file_name
