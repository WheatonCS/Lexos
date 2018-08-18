import pandas as pd
from io import StringIO
from Bio import Phylo
from lexos.receivers.bct_receiver import BCTOption
from lexos.models.bct_model import BCTTestOptions, BCTModel


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
        id_temp_label_map={0: "F1.txt", 1: "F2.txt"},
        front_end_option=BCTOption(
            linkage_method="average",
            dist_metric="euclidean",
            iterations=20,
            cutoff=0.5
        )
    )

    # Get the model and set up tree holder.
    BCT_model = BCTModel(test_options=test_options)
    consensus_tree_holder = StringIO()
    consensus_tree = BCT_model._get_bootstrap_consensus_tree()
    Phylo.write(consensus_tree, consensus_tree_holder, format="newick")

    def test_consensus_tree(self):
        assert self.consensus_tree_holder.getvalue() in [
            "(F2.txt:0.00000,F1.txt:0.00000):0.00000;\n",
            "(F1.txt:0.00000,F2.txt:0.00000):0.00000;\n"
        ]
