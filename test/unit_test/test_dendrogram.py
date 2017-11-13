import numpy as np
import pandas as pd

from lexos.models.dendro_model import DendroOption, DendrogramModel, \
    DendroTestOptions


class TestsBasic:
    test_options = DendroTestOptions(
        doc_term_matrix=pd.DataFrame(
            [
                [0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 5.0, 4.0],
                [0.0, 0.0, 9.0, 9.0, 0.0, 0.0, 0.0, 4.0],
                [5.0, 10.0, 0.0, 0.0, 10.0, 5.0, 0.0, 0.0]
            ],
            index=[2, 4, 10],
            columns=['1', '2', '3', '4', '5', '6', '7', '8']
        ),

        front_end_option=DendroOption(
            orientation='left',
            linkage_method='average',
            dist_metric='euclidean'
        ),

        id_temp_label_map={
            2: "this is a test",
            4: "Cheng is handsome",
            10: "I look so good!"
        }

    )

    model = DendrogramModel(test_options=test_options)

    # noinspection PyProtectedMember
    def test_get_dendro_graph(self):
        basic_fig = self.model._get_dendrogram_fig()
        np.testing.assert_equal(
            basic_fig['layout']['yaxis']['ticktext'],
            np.array(['I look so good!', 'this is a test', 'Cheng is handsome'])
        )
        np.testing.assert_allclose(
            basic_fig['data'][0]['x'], [0., 5., 5., 0.]
        )
        np.testing.assert_allclose(
            basic_fig['data'][0]['y'], [-15., -15., -25., -25.]
        )
        np.testing.assert_allclose(
            basic_fig['data'][1]['x'], [0., 20.98597876, 20.98597876, 5.]
        )
        np.testing.assert_allclose(
            basic_fig['data'][1]['y'], [-5., -5., -20., -20.]
        )
