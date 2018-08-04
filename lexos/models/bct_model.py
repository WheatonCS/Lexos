"""This is a model to produce bootstrap consensus tree of the dtm."""

import os
import numpy as np
import pandas as pd
from Bio import Phylo
from io import StringIO
from skbio import TreeNode
from ete3 import TreeStyle, Tree
from Bio.Phylo.Consensus import *
from scipy.cluster.hierarchy import linkage
from typing import NamedTuple, Optional, List
from lexos.managers import session_manager
from lexos.models.base_model import BaseModel
from lexos.helpers.constants import RESULTS_FOLDER
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
                         sample_dtm: pd.DataFrame) -> str:
        """Get newick tree based on a subset of the DTM.

        :param labels: All file names from the DTM.
        :param sample_dtm: A 80% subset of the complete DTM.
        :return: A newick formatted tree representing the DTM subset.
        """
        # Create the StringIO newick tree holder.
        newick_tree = StringIO()

        # noinspection PyTypeChecker
        # Get the linkage matrix for the sample doc term matrix.
        linkage_matrix = linkage(
            sample_dtm.values,
            metric=self._bct_option.dist_metric,
            method=self._bct_option.linkage_method
        )

        # Convert linkage matrix to a tree node
        tree = TreeNode.from_linkage_matrix(
            linkage_matrix=linkage_matrix,
            id_list=labels
        )

        # noinspection PyUnresolvedReferences
        # Write the tree to newick format to the stringIO holder.
        tree.write(newick_tree)

        # Get the string in side StringIO object.
        newick_tree_string = newick_tree.getvalue()

        # Return it as a bio python object.
        return Phylo.read(
            StringIO(newick_tree_string),
            format="newick"
        )

    def _get_bootstrap_trees(self) -> List[str]:
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

    def _get_bootstrap_consensus_tree(self) -> Tree:
        """Get the consensus tree.

        :return: The consensus tree of the list of newick trees.
        """
        # Create the StringIO newick tree holder.
        consensus_tree_holder = StringIO()

        # Check users selection and return the correct consensus tree.
        if self._bct_option.consensus_method == "strict":
            Phylo.write(
                trees=strict_consensus(trees=self._get_bootstrap_trees()),
                file=consensus_tree_holder,
                format="newick"
            )
        elif self._bct_option.consensus_method == "majority":
            Phylo.write(
                trees=majority_consensus(trees=self._get_bootstrap_trees()),
                file=consensus_tree_holder,
                format="newick"
            )
            return majority_consensus(trees=self._get_bootstrap_trees())
        elif self._bct_option.consensus_method == "adam":
            Phylo.write(
                trees=adam_consensus(trees=self._get_bootstrap_trees()),
                file=consensus_tree_holder,
                format="newick"
            )
        else:
            raise ValueError("Invalid bootstrap consensus method.")

        return Tree(consensus_tree_holder.getvalue(), quoted_node_names=True)

    @staticmethod
    def _get_ete_tree_style() -> TreeStyle:
        """

        :return:
        """
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
        # Get the default saving directory of BCT result.
        result_folder_path = os.path.join(
            session_manager.session_folder(), RESULTS_FOLDER)

        # Attempt to make the directory, if the directory isn't already there.
        if not os.path.isdir(result_folder_path):
            os.makedirs(result_folder_path)

        # Get the complete saving path of BCT result.
        save_path = os.path.join(result_folder_path, "bct_result.png")

        # Get the ete formatted consensus tree.
        consensus_tree = self._get_bootstrap_consensus_tree()

        consensus_tree.render(
            tree_style=self._get_ete_tree_style(),
            file_name="result.png",
            units="px",
            h=700,
            w=700
        )

        return save_path
