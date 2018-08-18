import pandas as pd
from lexos.models.bct_model import BCTTestOptions, BCTModel
from lexos.receivers.bct_receiver import BCTOption


class TestBCTModel:
    test_options = BCTTestOptions(
        doc_term_matrix=pd.DataFrame(
            index=[0, 1, 2],
            columns=["A", "B", "C", "D", "E", "F", "G", "H", "I"],
            # Set data to be the same in order to fix result to test.
            data=[
                [10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 10, 10, 10, 10],
                [10, 10, 10, 10, 10, 10, 10, 10, 10]
            ]
        ),
        id_temp_label_map={0: "F1.txt", 1: "F2.txt", 2: "F3.txt"},
        front_end_option=BCTOption(
            linkage_method="average",
            dist_metric="euclidean",
            iterations=20,
            cutoff=0.5
        )
    )

    BCT_model = BCTModel(test_options=test_options)

    # Get the rolling window model and other test components
    rw_ratio_model = RollingWindowsModel(test_option=test_ratio_count)
    rw_ratio_windows = rw_ratio_model._get_windows()
    rw_ratio_graph = rw_ratio_model._generate_rwa_graph()
    rw_ratio_csv_frame = rw_ratio_model._get_rwa_csv_frame()
    rw_ratio_milestone = \
        rw_ratio_model._find_mile_stone_windows_indexes_in_all_windows(
            windows=rw_ratio_windows
        )

    def test_get_windows(self):
        np.testing.assert_array_equal(
            self.rw_ratio_windows,
            ['ha ', 'a h', ' ha', 'ha ', 'a h', ' ha', 'ha ', 'a h', ' ha',
             'ha ', 'a l', ' la', 'la ', 'a t', ' ta', 'ta ', 'a h', ' ha'])

    def test_token_ratio_windows(self):
        pd.testing.assert_series_equal(
            left=self.rw_ratio_model._find_token_ratio_in_windows(
                numerator_token="t",
                denominator_token="a",
                windows=self.rw_ratio_windows
            ),
            right=pd.Series(
                data=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0],
            ),
            check_names=False)

    def test_generate_rwa_graph(self):
        assert self.rw_ratio_graph['data'][0]['type'] == 'scattergl'

        np.testing.assert_array_equal(
            self.rw_ratio_graph['data'][0]['x'],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        )

        np.testing.assert_array_equal(
            self.rw_ratio_graph['data'][0]['y'],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.5, 0.5, 0.5, 0.0, 0.0]
        )

    def test_find_milestone(self):
        assert self.rw_ratio_milestone == {'t': [15],
                                           'a': [1, 4, 7, 10, 13, 16]}

    def test_csv_frame(self):
        pd.testing.assert_frame_equal(
            self.rw_ratio_csv_frame,
            pd.DataFrame(
                index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                       10, 11, 12, 13, 14, 15, 16, 17],
                columns=["t / (t + a)"],
                data=[[0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.],
                      [0.], [0.], [0.], [0.], [0.5], [0.5], [0.5], [0.], [0.]]
            )

        )

