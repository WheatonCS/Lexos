"""This is a model to produce bootstrap consensus tree of the dtm."""

import numpy as np
import pandas as pd
from io import StringIO
from Bio import Phylo
from skbio import TreeNode
from typing import NamedTuple, Optional, List
from scipy.cluster.hierarchy import linkage
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

    def _get_newick_tree(self, sample_dtm: pd.DataFrame) -> str:
        # Create the StringIO newick tree holder.
        newick_tree = StringIO()

        # Get the linkage matrix for the sample doc term matrix.
        linkage_matrix = linkage(
            sample_dtm.data,
            metric=self._bct_option.dist_metric,
            method=self._bct_option.linkage_method
        )

        # Convert linkage matrix to a tree node
        tree = TreeNode.from_linkage_matrix(
            linkage_matrix=linkage_matrix,
            id_list=sample_dtm.index
        )

        # noinspection PyUnresolvedReferences
        # Write the tree to newick format to the stringIO holder.
        tree.write(newick_tree)

        # Get the string in side StringIO object.
        newick_tree_string = newick_tree.getvalue()

        A = Phylo.read(StringIO(newick_tree_string), format="newick")

        # Return it as a bio python object.
        return Phylo.read(
            StringIO(newick_tree_string),
            format="newick"
        )

    def _get_bootstrap_trees(self) -> List[str]:
        return [
            self._get_newick_tree(
                sample_dtm=self._doc_term_matrix.sample(
                    frac=0.8,
                    random_state=np.random.RandomState
                )
            )
            for _ in range(self._bct_option.iterations)
        ]

    def get_bootstrap_consensus_tree(self) -> str:
        A = self._get_bootstrap_trees()
        B = self._get_newick_tree()

        return "works"
