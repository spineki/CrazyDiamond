from Engine.engine import Engine

def test_react_to_keyword():
    e = Engine()
    e.reactive_keyword = ["apple", "banana"]
    verif = e.react_to_keyword("apple")
    assert verif == True
    verif = e.react_to_keyword("ban")
    assert verif == True
    verif = e.react_to_keyword("bananana")
    assert verif == False

def test_print_v(capsys):
    with capsys.disabled():
        e = Engine()

    e.verbose = True
    e.print_v("test")
    captured = capsys.readouterr()
    assert captured.out == "test\n"

    e.verbose = False
    e.print_v("second_test")
    captured = capsys.readouterr()
    assert captured.out == ""

    logs = e.log
    assert logs == ["test", "second_test"]

def test_get_logs():
    e = Engine()
    e.print_v("test1", "test2")
    e.print_v("test3")
    logs = e.get_logs()
    assert logs == "test1 test2\ntest3"

    logs = e.get_logs(sep="_")
    assert logs == "test1 test2_test3"

def test_purify_name():
    e = Engine()
    purified = e.purify_name("test")
    assert purified == "test"
    purified = e.purify_name("test>test|test<test?test!test")
    assert purified == "test_test_test_test_test_test"