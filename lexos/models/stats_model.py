from typing import List, Tuple, Optional, NamedTuple
from plotly.offline import plot
import pandas as pd
import numpy as np
import plotly.graph_objs as go

from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import MatrixReceiver, IdTempLabelMap


class StatsTestOptions(NamedTuple):
    """A typed tuple to hold test options."""
    doc_term_matrix: pd.DataFrame
    id_temp_label_map: IdTempLabelMap


class CorpusStats(NamedTuple):
    """A typed tuple to represent statistics of the whole corpus."""
    mean: float  # Average size of all files.
    # File anomaly found using standard error.
    anomaly_se: List[Optional[Tuple[str, str]]]
    # File anomaly found using interquartile range.
    anomaly_iqr: List[Optional[Tuple[str, str]]]
    std_deviation: float  # Standard deviation of all file sizes.
    inter_quartile_range: float  # Interquartile range.


class StatsModel(BaseModel):
    def __init__(self, test_options: Optional[StatsTestOptions] = None):
        """This is the class to generate statistics of the input file.

        :param test_options: the input used in testing to override the
                             dynamically loaded option
        """
        super().__init__()
        if test_options is not None:
            self._test_dtm = test_options.doc_term_matrix
            self._test_id_temp_label_map = test_options.id_temp_label_map
        else:
            self._test_dtm = None
            self._test_id_temp_label_map = None

    @property
    def _doc_term_matrix(self) -> pd.DataFrame:
        """:return: the document term matrix"""
        return self._test_dtm if self._test_dtm is not None \
            else MatrixModel().get_matrix()

    @property
    def _id_temp_label_map(self) -> IdTempLabelMap:
        """:return: a map takes an id to temp labels"""
        return self._test_id_temp_label_map \
            if self._test_id_temp_label_map is not None \
            else MatrixModel().get_id_temp_label_map()

    def get_corpus_info(self) -> CorpusStats:
        """Converts word lists completely to statistic.

        :return: a typed tuple that holds all statistic of the entire corpus.
        """

        # Check if empty corpus is given.
        assert not self._doc_term_matrix.empty, EMPTY_DTM_MESSAGE

        # Get file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Get the file count sums by sum the column.
        file_sizes = self._doc_term_matrix.sum(1)
        # Get the average file word counts.
        mean = file_sizes.mean(0)
        # Get the standard deviation of the file word counts.
        std_deviation = file_sizes.std(0)
        # Get the median of the file word counts.
        median = file_sizes.mean(0)
        # Get the iqr of the file word counts.
        first_quartile = file_sizes.quantile(0.25)
        third_quartile = file_sizes.quantile(0.75)
        iqr = third_quartile - first_quartile

        # Standard error analysis: assume file sizes are normally distributed;
        # we detect anomaly by finding files with sizes that are more than two
        # standard deviation away from the mean. In another word, we find files
        # with sizes that are not in the major 95% range.

        anomaly_se = [
            ("small", label)
            if file_sizes[count] < mean - 2 * std_deviation
            else ("large", label)
            if file_sizes[count] > mean + 2 * std_deviation
            else None
            for count, label in enumerate(labels)]

        # Interquartile range analysis: We detect anomaly by finding files with
        # sizes that are either 1.5 interquartile ranges above third quartile
        # or 1.5 interquartile ranges below first quartile.

        anomaly_iqr = [
            ("small", label)
            if file_sizes[count] < first_quartile - 1.5 * iqr
            else ("large", label)
            if file_sizes[count] > third_quartile + 1.5 * iqr
            else None
            for count, label in enumerate(labels)]

        return CorpusStats(mean=mean,
                           anomaly_se=anomaly_se,
                           anomaly_iqr=anomaly_iqr,
                           std_deviation=std_deviation,
                           inter_quartile_range=iqr)

    def get_file_info(self) -> str:
        """Get statistics of each file.

        :return: A HTML table converted from a pandas data frame.
        """
        # Check if empty corpus is given.
        assert not self._doc_term_matrix.empty, EMPTY_DTM_MESSAGE

        # Get file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Get proper name headers.
        token_type = \
            MatrixReceiver().options_from_front_end().token_option.token_type

        token_name = "Terms" if token_type == "word" else "Characters"

        file_stats = pd.DataFrame(
            columns=["Documents",
                     f"Number of {token_name} occuring once",
                     f"Total number of {token_name}",
                     f"Average number of {token_name}",
                     f"Distinct number of {token_name}"])

        file_stats["Documents"] = labels
        file_stats[f"Number of {token_name} occuring once"] = \
            self._doc_term_matrix.eq(1).sum(axis=1).values
        file_stats[f"Total number of {token_name}"] = \
            self._doc_term_matrix.sum(axis=1).values
        file_stats[f"Distinct number of {token_name}"] = \
            self._doc_term_matrix.ne(0).sum(axis=1).values
        file_stats[f"Average number of {token_name}"] = \
            file_stats[f"Total number of {token_name}"] / \
            file_stats[f"Distinct number of {token_name}"]

        return file_stats.round(4).to_html(
            index=False,
            classes="table table-striped table-bordered"
        )

    def get_box_plot(self) -> str:
        """Get box plot for the entire corpus.

        :return: A plotly object that contains the box plot.
        """
        # Get file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Set up the box plot.
        box_plot = go.Box(x0=0.5,  # Initial position of the box plot
                          y=self._doc_term_matrix.sum(1).values,
                          name="Corpus Box Plot",
                          hoverinfo="y",
                          marker=dict(color='rgb(10, 140, 200)'))

        # Set up the points.
        scatter_plot = go.Scatter(
            # Get random x values with the range.
            x=[np.random.uniform(-0.3, 0) for _, _ in enumerate(labels)],
            y=self._doc_term_matrix.sum(1).values,
            name="Corpus Scatter Plot",
            hoverinfo="text",
            mode="markers",
            text=labels)

        # Set up the plot data set.
        data = [scatter_plot, box_plot]

        # Hide information on x-axis as we do not really need any of those.
        layout = go.Layout(
            xaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                autotick=False,
                showline=False,
                showticklabels=False
            )
        )

        # Return plotly object as a div.
        return plot(go.Figure(data=data, layout=layout),
                    show_link=False,
                    output_type="div")
