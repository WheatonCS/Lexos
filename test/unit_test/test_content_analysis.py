from lexos.models.content_analysis_model import ContentAnalysisModel
import pandas as pd


def test_add_corpus():
    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test')
    assert test.corpus[0].name == "file1"
    assert test.corpus[0].label == "file1"
    assert test.corpus[0].content == "test"


def test_add_dictionary():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", content="test")
    assert test.dictionaries[0].name == "dict1"
    assert test.dictionaries[0].label == "dict1"
    assert test.dictionaries[0].content == ["test"]
    assert test.dictionaries[0].active


def test_delete_dictionary():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", content="test")
    assert len(test.dictionaries) == 1
    test.delete_dictionary("dict1")
    assert len(test.dictionaries) == 0


def test_toggle_dictionary():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", content="test")
    assert test.dictionaries[0].active
    test.toggle_dictionary("dict1")
    assert test.dictionaries[0].active is False
    test.toggle_dictionary("dict1")
    assert test.dictionaries[0].active


def test_get_active_dicts():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", content="test")
    test.add_dictionary(file_name="dict2", content="test")
    test.toggle_dictionary("dict1")
    active = test.get_active_dicts()
    assert len(active) == 1
    assert active[0].name == "dict2"


def test_count_words():
    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    assert test.counters[0][0] == 1

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test test test')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    assert test.counters[0][0] == 3

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='a test')
    test.add_dictionary(file_name="dict1", content="test, a")
    test.count_words()
    assert test.counters[0][0] == 2

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='a test')
    test.add_dictionary(file_name="dict1", content="test, a, a test")
    test.count_words()
    assert test.counters[0][0] == 1

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='a test test')
    test.add_dictionary(file_name="dict1", content="test, a, a test")
    test.count_words()
    assert test.counters[0][0] == 2

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='a test test a')
    test.add_dictionary(file_name="dict1", content="test, a, a test")
    test.count_words()
    assert test.counters[0][0] == 3


def test_generate_scores():
    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    test.generate_scores(formula="0")
    assert test.scores[0] == 0.0
    test.generate_scores(formula="[dict1]")
    assert test.scores[0] == 1

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test a')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    test.generate_scores(formula="[dict1]")
    assert test.scores[0] == 0.5

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='a test')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    test.generate_scores(formula="[dict1]*2")
    assert test.scores[0] == 1

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='a test a')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    test.generate_scores(formula="[dict1]")
    assert test.scores[0] == round(1 / 3, 3)


def test_generate_averages():
    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    test.generate_scores(formula="0")
    test.generate_averages()
    assert test.averages == ['Averages', 1.0, 0.0, 1.0, 0.0]

    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test')
    test.add_corpus(file_name="file1", label='file2', content='other file')
    test.add_dictionary(file_name="dict1", content="test")
    test.count_words()
    test.generate_scores(formula="0")
    test.generate_averages()
    assert test.averages == ['Averages', 0.5, 0.0, 1.5, 0.0]

    test.count_words()
    test.generate_scores(formula="4*[dict1]**2")
    test.generate_averages()
    assert test.averages == ['Averages', 0.5, 2.0, 1.5, 2.0]


def test_to_html():
    test = ContentAnalysisModel()
    assert test.to_html()


def test_to_data_frame():
    test = ContentAnalysisModel()
    test.add_corpus(file_name="file1", label='file1', content='test')
    test.add_corpus(file_name="file1", label='file2', content='other file')
    test.add_dictionary(file_name="dict1", content="test")
    test.add_dictionary(file_name="dict2", content="test")
    assert isinstance(test.to_data_frame(), type(pd.DataFrame()))


def test_is_secure():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", content="test")
    test.add_dictionary(file_name="dict2", content="test")
    assert test.is_secure("")
    assert test.is_secure("[dict1][dict2]")
    assert test.is_secure("0123456789 +-*/ () sin cos tan log sqrt")
    assert test.is_secure("os.system()") is False


def test_detect_active_dicts():
    test = ContentAnalysisModel()
    test.add_dictionary(file_name="dict1", content="test")
    test.add_dictionary(file_name="dict2", content="test")
    assert test.detect_active_dicts() == 2
