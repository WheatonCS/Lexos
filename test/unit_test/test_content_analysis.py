from lexos.models.content_analysis_model import ContentAnalysisModel
import pandas as pd


class TestOptions(object):
    def __init__(self, dict_label=None, formula=None):
        self.label = dict_label
        self.dict_label = dict_label
        self.formula = formula
TestOptions()

def test_add_corpus():
    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='test')
    assert test.corpus[0].name == "file1"
    assert test.corpus[0].label == "file1"
    assert test.corpus[0].content == "test"
test_add_corpus()

def test_add_dictionary():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", label="dict1", content="test")
    assert test.dictionaries[0].name == "dict1"
    assert test.dictionaries[0].label == "dict1"
    assert test.dictionaries[0].content == ["test"]
    assert test.dictionaries[0].active
test_add_dictionary()

def test_get_active_dicts():
    test = ContentAnalysisModel(TestOptions(dict_label="dict1"))
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.add_dictionary(file_name="dict2.txt", label="dict2", content="test")
    active = test.get_active_dicts()
    assert len(active) == 2
test_get_active_dicts()

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
test_count_words()

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
test_generate_scores()

def test_generate_averages():
    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.count()
    test.test_option = TestOptions(formula="0")
    test.save_formula()
    test.generate_scores()
    test.generate_averages()
    assert test.averages == ['Averages', 1.0, 0.0, 1.0, 0.0]

    test = ContentAnalysisModel()
    test.add_file(file_name="file1", label='file1', content='test')
    test.add_file(file_name="file2", label='file2', content='other file')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.count()
    test.test_option = TestOptions(formula="0")
    test.save_formula()
    test.generate_scores()
    test.generate_averages()
    assert test.averages == ['Averages', 0.5, 0.0, 1.5, 0.0]

    test.count()
    test.test_option = TestOptions(formula="4*[dict1]**2")
    test.save_formula()
    test.generate_scores()
    test.generate_averages()
    assert test.averages == ['Averages', 0.5, 2.0, 1.5, 2.0]
test_generate_averages()

def test_to_html():
    test = ContentAnalysisModel()
    assert test.to_html()
test_to_html()

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
test_to_data_frame()

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
test_is_secure()

def test_join_active_dicts():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test1")
    test.add_dictionary(file_name="dict2.txt", label="dict2", content="test2")
    joined_dicts = test.join_active_dicts()
    assert joined_dicts[0].dict_label == 'dict1'
    assert joined_dicts[0].content == 'test1'
    assert joined_dicts[1].dict_label == 'dict2'
    assert joined_dicts[1].content == 'test2'
test_join_active_dicts()

def test_save_formula():
    test = ContentAnalysisModel(TestOptions(formula="√([dict1])^([dict2])"))
    test.save_formula()
    assert test._formula == "sqrt([dict1])**([dict2])"
test_save_formula()

def test_check_formula():
    test = ContentAnalysisModel(TestOptions(formula="()sin(1)"))
    assert test.check_formula() == 0
    test.test_option = TestOptions(formula="(")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>"\
                                   "Mismatched parenthesis<br>"
    test.test_option = TestOptions(formula="sin()")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>"\
                                   "sin takes exactly one argument (0 given)"\
                                   "<br>"
    test.test_option = TestOptions(formula="cos()")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>"\
                                   "cos takes exactly one argument (0 given)"\
                                   "<br>"
    test.test_option = TestOptions(formula="tan()")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>"\
                                   "tan takes exactly one argument (0 given)"\
                                   "<br>"
    test.test_option = TestOptions(formula="log()")
    test.save_formula()
    assert test.check_formula() == "Formula errors:<br>"\
                                   "log takes exactly one argument (0 given)"\
                                   "<br>"
test_check_formula()

def test_analyze():
    test = ContentAnalysisModel()
    test.test_option = TestOptions(formula="[]")
    test.save_formula()
    test.add_file(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1.txt", label="dict1", content="test")
    test.add_dictionary(file_name="dict2.txt", label="dict2", content="test2")
    result_table, formula_errors = test.analyze()
    print(result_table, formula_errors)
    assert result_table is None
    assert isinstance(formula_errors, str)
    test.test_option = TestOptions(formula="[dict1]")
    test.save_formula()
    result_table, formula_errors = test.analyze()
    assert result_table == test.to_html()
    assert formula_errors == 0
test_analyze()
