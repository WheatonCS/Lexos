import pandas as pd
from io import StringIO
from Bio import Phylo
from scipy.cluster.hierarchy import linkage

from lexos.receivers.consensus_tree_receiver import BCTOption
from lexos.models.consensus_tree_model import BCTTestOptions, BCTModel


# noinspection PyProtectedMember
class TestBCTModel:
    test_options = BCTTestOptions(
        doc_term_matrix=pd.DataFrame(
            index=[0, 1],
            columns=["A", "B", "C", "D", "E", "F", "G", "H", "I"],
            # Set data to be the same in order to fix result to test.
            data=[
                [10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 10, 10, 10, 10]
            ]
        ),
        document_label_map={0: "F1.txt", 1: "F2.txt"},
        front_end_option=BCTOption(
            linkage_method="average",
            dist_metric="euclidean",
            iterations=20,
            cutoff=0.5,
            replace=False,
            text_color="rgb(0, 0, 0)"
        )
    )

    # Get the model and set up tree holder.
    BCT_model = BCTModel(test_options=test_options)
    consensus_tree_holder = StringIO()
    consensus_tree = BCT_model._get_bootstrap_consensus_tree()
    Phylo.write(consensus_tree, consensus_tree_holder, format="newick")
    consensus_tree_plot = BCT_model._get_bootstrap_consensus_tree_plot()
    consensus_tree_plot_axis = consensus_tree_plot.gca()

    def test_linkage_to_matrix(self):
        # noinspection PyTypeChecker
        linkage_matrix = linkage(
            self.test_options.doc_term_matrix.values,
            metric=self.test_options.front_end_option.dist_metric,
            method=self.test_options.front_end_option.linkage_method
        )
        assert self.BCT_model.linkage_to_newick(
            matrix=linkage_matrix,
            labels=["F1.txt", "F2.txt"]
        ) == "(F2.txt:0.0,F1.txt:0.0);"

    def test_consensus_tree(self):
        assert self.consensus_tree_holder.getvalue() in [
            "(F2.txt:0.00000,F1.txt:0.00000):0.00000;\n",
            "(F1.txt:0.00000,F2.txt:0.00000):0.00000;\n"
        ]

    def test_consensus_tree_plot_content(self):
        assert self.consensus_tree_plot_axis.texts[0].get_text() in [
            " F1.txt", " F2.txt"
        ]

    def test_consensus_tree_plot_title(self):
        assert self.consensus_tree_plot_axis.title.get_text() == \
            "Bootstrap Consensus Tree Result"

    def test_consensus_tree_plot_size(self):
        assert self.consensus_tree_plot_axis.figure.bbox.x1 == 950.0
