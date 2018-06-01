import json
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
from typing import List, Tuple, Optional, NamedTuple
from lexos.helpers.error_messages import EMPTY_DTM_MESSAGE
from lexos.models.base_model import BaseModel
from lexos.models.matrix_model import MatrixModel
from lexos.receivers.matrix_receiver import MatrixReceiver, IdTempLabelMap
from lexos.receivers.stats_receiver import StatsReceiver


class StatsTestOptions(NamedTuple):
    """A typed tuple to hold test options."""
    token_type: str
    doc_term_matrix: pd.DataFrame
    id_temp_label_map: IdTempLabelMap


class CorpusStats(NamedTuple):
    """A typed tuple to represent statistics of the whole corpus."""
    mean: float  # Average size of all files.
    # File anomaly found using standard error.
    anomaly_se: List[Optional[str]]
    # File anomaly found using interquartile range.
    anomaly_iqr: List[Optional[str]]
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
            self._test_token_type = test_options.token_type
            self._test_id_temp_label_map = test_options.id_temp_label_map
        else:
            self._test_dtm = None
            self._test_token_type = None
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

    @property
    def _stats_option(self):

        return StatsReceiver().options_from_front_end()

    @property
    def token_type(self) -> str:
        """:return: the token type that was used when calculating the stats."""
        if self._test_id_temp_label_map is not None:
            return self._test_token_type
        else:
            # Get dtm front end options.
            dtm_options = MatrixReceiver().options_from_front_end()
            # Get the correct current type.
            token_type = dtm_options.token_option.token_type
            return "terms" if token_type == "word" else "characters"

    def get_corpus_stats(self) -> CorpusStats:
        """Converts word lists completely to statistic.

        :return: a typed tuple that holds all statistic of the entire corpus.
        """
        A = self._stats_option
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

        # Get the iqr of the file word counts.
        first_quartile = file_sizes.quantile(0.25)
        third_quartile = file_sizes.quantile(0.75)
        iqr = third_quartile - first_quartile

        # Standard error analysis: assume file sizes are normally distributed;
        # we detect anomaly by finding files with sizes that are more than two
        # standard deviation away from the mean. In another word, we find files
        # with sizes that are not in the major 95% range.
        anomaly_se = [
            f"small: {label}"
            if file_sizes[count] < mean - 2 * std_deviation
            else f"large: {label}"
            if file_sizes[count] > mean + 2 * std_deviation
            else None
            for count, label in enumerate(labels)]

        # Interquartile range analysis: We detect anomaly by finding files with
        # sizes that are either 1.5 interquartile ranges above third quartile
        # or 1.5 interquartile ranges below first quartile.
        anomaly_iqr = [
            f"small: {label}"
            if file_sizes[count] < first_quartile - 1.5 * iqr
            else f"large: {label}"
            if file_sizes[count] > third_quartile + 1.5 * iqr
            else None
            for count, label in enumerate(labels)]

        return CorpusStats(
            mean=round(mean, 2),
            anomaly_se=anomaly_se,
            anomaly_iqr=anomaly_iqr,
            std_deviation=round(std_deviation, 2),
            inter_quartile_range=round(iqr, 2),
        )

    def get_file_stats(self) -> str:
        """Get statistics of each file.

        :return: A HTML table converted from a pandas data frame.
        """
        # Check if empty corpus is given.
        assert not self._doc_term_matrix.empty, EMPTY_DTM_MESSAGE

        # Get file names.
        labels = [self._id_temp_label_map[file_id]
                  for file_id in self._doc_term_matrix.index.values]

        # Set up data frame with proper headers.
        file_stats = pd.DataFrame(
            columns=["Documents",
                     f"Number of {self.token_type} occuring once",
                     f"Total number of {self.token_type}",
                     f"Average number of {self.token_type}",
                     f"Distinct number of {self.token_type}"])

        # Save document names in the data frame.
        file_stats["Documents"] = labels
        # Find number of token that appears only once.
        file_stats[f"Number of {self.token_type} occuring once"] = \
            self._doc_term_matrix.eq(1).sum(axis=1).values
        # Find total number of tokens.
        file_stats[f"Total number of {self.token_type}"] = \
            self._doc_term_matrix.sum(axis=1).values
        # Find distinct number of tokens.
        file_stats[f"Distinct number of {self.token_type}"] = \
            self._doc_term_matrix.ne(0).sum(axis=1).values
        # Find average number of appearance of tokens.
        file_stats[f"Average number of {self.token_type}"] = \
            file_stats[f"Total number of {self.token_type}"] / \
            file_stats[f"Distinct number of {self.token_type}"]

        # Round all the values and return as a HTML string.
        return file_stats.round(3).to_html(
            index=False,
            classes="table table-striped table-bordered"
        )

    def _get_box_plot_object(self) -> go.Figure:
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
            x=[np.random.uniform(-0.3, 0) for _ in labels],
            y=self._doc_term_matrix.sum(1).values,
            name="Corpus Scatter Plot",
            hoverinfo="text",
            mode="markers",
            text=labels)

        # Set up the plot data set.
        data = [scatter_plot, box_plot]

        # Hide information on x-axis as we do not really need any of those.
        # Set the title of the graph.
        layout = go.Layout(
            title="Statistics of the Given Corpus",
            xaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                autotick=False,
                showline=False,
                showticklabels=False
            )
        )

        # Return a plotly figure.
        return go.Figure(data=data, layout=layout)

    def get_box_plot(self) -> str:
        """Return a HTML string that is ready to be displayed on the web.

        :return: A string in HTML format that contains the plotly boxplot.
        """
        # Return plotly object as a div.
        return plot(self._get_box_plot_object(),
                    include_plotlyjs=False,
                    output_type="div",
                    show_link=False)
