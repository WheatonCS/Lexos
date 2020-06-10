"""This is the statistics model which gets the statistics data."""

from typing import Optional, NamedTuple, List

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import plot

from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import MatrixReceiver
from lexos.receivers.matrix_receiver import DocumentLabelMap
from lexos.receivers.statistics_receiver import StatsReceiver, \
    StatsFrontEndOption
import lexos.managers.utility as utility


class TextAnomalies(NamedTuple):
    """A typed tuple to represent text anomalies of the whole corpus."""

    small_items: List[str]
    large_items: List[str]


class CorpusStats(NamedTuple):
    """A typed tuple to represent statistics of the whole corpus."""

    unit: str  # Unit of all statistics.
    mean: float  # Average size of all files.
    # File anomaly found using standard error.
    anomaly_se: TextAnomalies
    # File anomaly found using interquartile range.
    anomaly_iqr: TextAnomalies
    std_deviation: float  # Standard deviation of all file sizes.
    inter_quartile_range: float  # Interquartile range.


class StatsTestOptions(NamedTuple):
    """A typed tuple to hold all statistics test options."""

    token_type_str: str
    doc_term_matrix: pd.DataFrame
    front_end_option: StatsFrontEndOption
    document_label_map: DocumentLabelMap


class StatsModel(BaseModel):
    """The StatsModel inherits from the BaseModel."""

    def __init__(self, test_options: Optional[StatsTestOptions] = None):
        """Generate statistics of the input file.

        :param test_options: the input used in testing to override the
                             dynamically loaded option
        """
        super().__init__()
        if test_options is not None:
            self._test_dtm = test_options.doc_term_matrix
            self._test_token_type_str = test_options.token_type_str
            self._test_front_end_option = test_options.front_end_option
            self._test_document_label_map = test_options.document_label_map
        else:
            self._test_dtm = None
            self._test_token_type_str = None
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
    def _stats_option(self):
        """:return: statistics front end option."""
        return self._test_front_end_option \
            if self._test_front_end_option is not None \
            else StatsReceiver().options_from_front_end()

    @property
    def _active_doc_term_matrix(self) -> pd.DataFrame:
        """:return: A dtm that contains only user selected files."""
        return self._doc_term_matrix.loc[self._stats_option.active_file_ids]

    @property
    def _token_type_str(self) -> str:
        """:return: the token type that was used when calculating the stats."""
        if self._test_document_label_map is not None:
            return self._test_token_type_str
        else:
            # Get dtm front end options.
            dtm_options = MatrixReceiver().options_from_front_end()
            # Get the correct current type.
            token_type = dtm_options.token_option.token_type
            return "terms" if token_type == "word" else "character n-grams"

    @property
    def _get_document_statistics_dataframe(self) -> pd.DataFrame:
        """Get a Pandas dataframe containing the statistics of each document.

        :return: A Pandas dataframe containing statistics of each document.
        """
        # Check if empty corpus is given.
        assert not self._active_doc_term_matrix.empty, EMPTY_DTM_MESSAGE

        # Get file names.
        labels = [self._document_label_map[file_id]
                  for file_id in self._active_doc_term_matrix.index.values]

        # Set up data frame with proper headers.
        file_stats = pd.DataFrame(
            columns=["Documents",
                     f"Number of {self._token_type_str} occurring once",
                     f"Total number of {self._token_type_str}",
                     "Vocabulary Density",
                     f"Distinct number of {self._token_type_str}"])

        # Save document names in the data frame.
        file_stats["Documents"] = labels
        # Find number of token that appears only once.
        file_stats[f"Number of {self._token_type_str} occurring once"] = \
            self._active_doc_term_matrix.eq(1).sum(axis=1).values
        # Find total number of tokens.
        file_stats[f"Total number of {self._token_type_str}"] = \
            self._active_doc_term_matrix.sum(axis=1).values
        # Find distinct number of tokens.
        file_stats[f"Distinct number of {self._token_type_str}"] = \
            self._active_doc_term_matrix.ne(0).sum(axis=1).values
        # Find average number of appearance of tokens.
        file_stats["Vocabulary Density"] = \
            file_stats[f"Distinct number of {self._token_type_str}"] / \
            file_stats[f"Total number of {self._token_type_str}"]

        return file_stats

    @staticmethod
    def __get_quartile__(index: float, arr: np.array) -> float:
        """Get the quartile of the array.

        The numpy quantile function calculates the quartiles in a different way
        than how plotly calculates them and the results are slightly different
        so this is how plotly calculates the quartiles.
        :param index: the index of the array that is where the quartile is
        :param arr: the sorted array of all the document sizes
        :return: the value of the quartile of the array
        """
        if index % 1 == .5:
            ind = int(index)
            return arr[ind] * .5 + arr[ind + 1] * .5
        elif index % 1 == .25:
            ind = int(index)
            return arr[ind] * .75 + arr[ind + 1] * .25
        elif index % 1 == .75:
            ind = int(index)
            return arr[ind] * .25 + arr[ind + 1] * .75
        else:
            ind = int(index)
            return arr[ind]

    def get_corpus_stats(self) -> CorpusStats:
        """Convert word lists completely to statistic.

        :return: a typed tuple that holds all statistic of the entire corpus.
        """
        # Check if empty corpus is given.
        assert not self._active_doc_term_matrix.empty, EMPTY_DTM_MESSAGE

        # Get the active file ids.
        active_file_ids = self._active_doc_term_matrix.index

        # Get the file count sums by sum the column.
        file_sizes = self._active_doc_term_matrix.sum(axis="columns")
        # Get the average file word counts.
        mean = file_sizes.mean(axis="index")

        # Get the standard deviation of the file word counts.
        std_deviation = file_sizes.std(axis="index")

        # Get quartile indexes
        arr = np.array(file_sizes)
        arr.sort()
        length = len(arr)
        # if there is only one document automatically set the indexes to 0
        if length == 1:
            q1_index = 0
            q3_index = 0
        else:
            q1_index = length * .25 + .5 - 1
            q3_index = length * .75 + .5 - 1

        # Get the iqr of the file word counts.
        first_quartile = self.__get_quartile__(index=q1_index, arr=arr)
        third_quartile = self.__get_quartile__(index=q3_index, arr=arr)
        iqr = third_quartile - first_quartile

        # Standard error analysis: assume file sizes are normally distributed;
        # we detect anomaly by finding files with sizes that are more than two
        # standard deviation away from the mean. In another word, we find files
        # with sizes that are not in the major 95% range.
        anomaly_se_small = [
            self._document_label_map[file_id]
            for file_id in active_file_ids
            if file_sizes[file_id] < mean - 2 * std_deviation
        ]

        anomaly_se_large = [
            self._document_label_map[file_id]
            for file_id in active_file_ids
            if file_sizes[file_id] > mean + 2 * std_deviation
        ]

        anomaly_se = TextAnomalies(small_items=anomaly_se_small,
                                   large_items=anomaly_se_large)

        # Interquartile range analysis: We detect anomaly by finding files with
        # sizes that are either 1.5 interquartile ranges above third quartile
        # or 1.5 interquartile ranges below first quartile.
        anomaly_iqr_small = list(set(
            self._document_label_map[file_id]
            for file_id in active_file_ids
            if file_sizes[file_id] < first_quartile - 1.5 * iqr
        ))

        anomaly_iqr_large = list(set(
            self._document_label_map[file_id]
            for file_id in active_file_ids
            if file_sizes[file_id] > third_quartile + 1.5 * iqr
        ))

        anomaly_iqr = TextAnomalies(small_items=anomaly_iqr_small,
                                    large_items=anomaly_iqr_large)

        # Return the namedTuple and round each value.
        return CorpusStats(
            unit=self._token_type_str,
            mean=round(mean, 2),
            anomaly_se=anomaly_se,
            anomaly_iqr=anomaly_iqr,
            std_deviation=round(std_deviation, 2),
            inter_quartile_range=round(iqr, 2),
        )

    def get_document_statistics(self) -> dict:
        """Get the document statistics.

        :return: The document statistics.
        """
        result = self._get_document_statistics_dataframe.round(3)

        sorted_result = result.sort_values(
            by=[result.columns[self._stats_option.sort_column]],
            ascending=self._stats_option.sort_ascending
        )

        return {
            "statistics-table-head":
                ["Name", "Single-Occurrence Terms", "Total Terms",
                 "Vocabulary Density", "Distinct Terms"],
            "statistics-table-body": sorted_result.values.tolist(),
            "statistics-table-csv": sorted_result.to_csv()
        }

    def _get_box_plot_object(self) -> go.Figure:
        """Get box plot for the entire corpus.

        :return: A plotly object that contains the box plot.
        """
        # Get file names.
        labels = [self._document_label_map[file_id]
                  for file_id in self._active_doc_term_matrix.index.values]

        # Set up the points.
        scatter_plot = go.Scatter(
            x=[_ for _ in labels],
            y=self._active_doc_term_matrix.sum(1).values,
            hoverinfo="text",
            mode="markers",
            marker=dict(color=self._stats_option.highlight_color),
            text=labels
        )

        # Set up the box plot.
        box_plot = go.Box(
            x0=0,  # Initial position of the box plot
            y=self._active_doc_term_matrix.sum(1).values,
            hoverinfo="y",
            marker=dict(color=self._stats_option.highlight_color),
            jitter=.15
        )

        # Create a figure with two subplots and fill the figure.
        figure = tools.make_subplots(rows=1, cols=2, shared_yaxes=False)
        figure.append_trace(trace=scatter_plot, row=1, col=1)
        figure.append_trace(trace=box_plot, row=1, col=2)

        # Hide useless information on x-axis and set up title.
        figure.layout.update(
            dragmode="pan",
            showlegend=False,
            margin=dict(
                r=0,
                b=30,
                t=10,
                pad=4
            ),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            yaxis=dict(
                showline=False,
                zeroline=False,
                gridcolor=self._stats_option.text_color
            ),
            xaxis2=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            yaxis2=dict(
                showline=False,
                zeroline=False,
                gridcolor=self._stats_option.text_color
            ),
            hovermode="closest",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            font=dict(color=self._stats_option.text_color, size=16)
        )

        # Return the Plotly graph.
        return figure

    def get_box_plot(self) -> str:
        """Return the document size Plotly graph.

        :return: The document size Plotly graph.
        """
        config = {
            "displaylogo": False,
            "modeBarButtonsToRemove": ["toImage", "toggleSpikelines"],
            "scrollZoom": True
        }

        # Return the Plotly object as a div
        return plot(self._get_box_plot_object(),
                    include_plotlyjs=False,
                    output_type="div",
                    show_link=False,
                    config=config)
