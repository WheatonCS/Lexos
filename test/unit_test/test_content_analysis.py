import pandas as pd

from lexos.models.content_analysis_model import \
    ContentAnalysisModel


class TestOptions(object):
    def __init__(self, formula):
        self.formula = formula


def test_add_corpus():
    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='test')
    assert test.corpus[0].name == "file1"
    assert test.corpus[0].label == "file1"
    assert test.corpus[0].content == "test"


def test_add_dictionary():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", label="dict1", content="test")
    assert test.dictionaries[0].name == "dict1"
    assert test.dictionaries[0].label == "dict1"
    assert test.dictionaries[0].content == ["test"]
    assert test.dictionaries[0].active


def test_get_active_dicts():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.add_dictionary(file_name="dict2.txt", label="dict2", content="test")
    active = test.get_active_dicts()
    assert len(active) == 2


def test_count_words():
    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.count()
    assert test.counters[0][0] == 1

    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='test test test')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.count()
    assert test.counters[0][0] == 3

    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='a test')
    test.add_dictionary(file_name="dict1.txt", label="dict1",
                        content="test, a")
    test.count()
    assert test.counters[0][0] == 2

    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='a test')
    test.add_dictionary(file_name="dict1.txt", label="dict1",
                        content="test, a, a test")
    test.count()
    assert test.counters[0][0] == 1

    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='a test test')
    test.add_dictionary(file_name="dict1.txt", label="dict1",
                        content="test, a, a test")
    test.count()
    assert test.counters[0][0] == 2

    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='a test test a')
    test.add_dictionary(file_name="dict1.txt", label="dict1",
                        content="test, a, a test")
    test.count()
    assert test.counters[0][0] == 3


def test_generate_scores():
    test = ContentAnalysisModel(TestOptions(formula=""))
    test.add_file(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.count()
    test.generate_scores()
    assert test.scores[0] == 0.0
    test.test_option = TestOptions(formula="[dict1]")
    test.save_formula()
    test.generate_scores()
    assert test.scores[0] == 1

    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='test a')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.count()
    test.test_option = TestOptions(formula="[dict1]")
    test.save_formula()
    test.generate_scores()
    assert test.scores[0] == 0.5

    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='a test')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.count()
    test.test_option = TestOptions(formula="[dict1]*2")
    test.save_formula()
    test.generate_scores()
    assert test.scores[0] == 1

    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='a test a')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.count()
    test.test_option = TestOptions(formula="[dict1]")
    test.save_formula()
    test.generate_scores()
    assert test.scores[0] == round(1 / 3, 3)


def test_generate_averages():
    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.count()
    test.test_option = TestOptions(formula="0")
    test.save_formula()
    test.generate_scores()
    test.generate_averages()
    assert test.averages == [1.0, 0.0, 1.0, 0.0]

    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='test')
    test.add_file(file_name="file2", label='file2', content='other file')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.count()
    test.test_option = TestOptions(formula="0")
    test.save_formula()
    test.generate_scores()
    test.generate_averages()
    assert test.averages == [0.5, 0.0, 1.5, 0.0]

    test.count()
    test.test_option = TestOptions(formula="4*[dict1]**2")
    test.save_formula()
    test.generate_scores()
    test.generate_averages()
    assert test.averages == [0.5, 2.0, 1.5, 2.0]


# TODO: add test for to_html function.

def test_to_data_frame():
    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='test')
    test.add_file(file_name="file2", label='file2', content='other file')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.add_dictionary(file_name="dict2.txt", label="dict2", content="test")
    test.count()
    test.test_option = TestOptions(formula="")
    test.save_formula()
    test.generate_scores()
    test.generate_averages()
    assert isinstance(test.to_data_frame(), type(pd.DataFrame()))


def test_is_secure():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.add_dictionary(file_name="dict2.txt", label="dict2", content="test")
    test.test_option = TestOptions(formula="")
    test.save_formula()
    assert test.is_secure()
    test.test_option = TestOptions(formula="[dict1][dict2]")
    test.save_formula()
    assert test.is_secure()
    test.test_option = TestOptions(
        formula="0123456789 +-*/ () sin cos tan log sqrt")
    test.save_formula()
    assert test.is_secure()
    test.test_option = TestOptions(formula="os.system()")
    test.save_formula()
    assert test.is_secure() is False


def test_join_active_dicts():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test1")
    test.add_dictionary(file_name="dict2.txt", label="dict2", content="test2")
    joined_dicts = test.join_active_dicts()
    assert joined_dicts[0].dict_label == 'dict1'
    assert joined_dicts[0].content == 'test1'
    assert joined_dicts[1].dict_label == 'dict2'
    assert joined_dicts[1].content == 'test2'


def test_save_formula():
    test = ContentAnalysisModel(TestOptions(formula="√([dict1])^([dict2])"))
    test.save_formula()
    assert test._formula == "sqrt([dict1])**([dict2])"


def test_check_formula():
    test = ContentAnalysisModel(TestOptions(formula="()sin(1)"))
    assert test.check_formula() == ""
    test.test_option = TestOptions(formula="(")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>" \
                                   "Mismatched parenthesis<br>"
    test.test_option = TestOptions(formula="sin()")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>" \
                                   "sin takes exactly one argument (0 given)" \
                                   "<br>"
    test.test_option = TestOptions(formula="cos()")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>" \
                                   "cos takes exactly one argument (0 given)" \
                                   "<br>"
    test.test_option = TestOptions(formula="tan()")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>" \
                                   "tan takes exactly one argument (0 given)" \
                                   "<br>"
    test.test_option = TestOptions(formula="log()")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>" \
                                   "log takes exactly one argument (0 given)" \
                                   "<br>"


def test_dictionary_colors():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.add_dictionary(file_name="dict2.txt", label="dict2", content="test2")
    colors = test.dictionary_colors
    assert isinstance(colors["dict1"], str) and len(colors["dict1"]) > 0
    assert isinstance(colors["dict2"], str) and len(colors["dict1"]) > 0


def test_generate_corpus_counts_table():
    test = ContentAnalysisModel()
    test.test_option = TestOptions(formula="[]")
    test.save_formula()
    test.add_file(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.add_dictionary(file_name="dict2.txt", label="dict2", content="test2")
    html_table = test.generate_corpus_results(test.count())
    assert html_table[0][0] == "dict1"
    assert html_table[-1][0] == "dict2"


def test_generate_files_raw_counts_tables():
    test = ContentAnalysisModel()
    test.test_option = TestOptions(formula="[]")
    test.save_formula()
    test.add_file(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.add_dictionary(file_name="dict2.txt", label="dict2", content="test2")
    html_tables = test.generate_document_results(test.count())
    for html_table in html_tables:
        assert html_table["name"] == "file1"
        # assert html_table == "dict2"


def test_analyze():
    test = ContentAnalysisModel()
    test.test_option = TestOptions(formula="[]")
    test.save_formula()
    test.add_file(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.add_dictionary(file_name="dict2.txt", label="dict2", content="test2")
    overview_results, overview_csv, corpus_results, corpus_csv, \
        document_results, errors = test.analyze()
    assert overview_results == ""
    assert isinstance(errors, str)
