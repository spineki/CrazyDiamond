from Engine.EngineManga.engineMangas import EngineMangas


def test_get_soup():
    e = EngineMangas()

    verif = e.get_soup(" http://www.google.com")
    assert verif is not None

    verif = e.get_soup("srxdhguyiojpklôijhugyfd")
    assert verif is None

def test_lexicographical_list_converter():
    e = EngineMangas()
    name_list = ["banana_1.jpg", "cherry_100.jpg", "raspberry_30.jpg"]
    assert e.lexicographical_list_converter(name_list) == ["banana_001.jpg", "cherry_100.jpg", "raspberry_030.jpg"]

    name_list = ["banana_1_10.jpg", "cherry_100_1.jpg", "raspberry_30_451.jpg"]
    assert e.lexicographical_list_converter(name_list) == ["banana_001_010.jpg", "cherry_100_001.jpg", "raspberry_030_451.jpg"]

    name_list = ["banana_1_10.jpg", "cherry_100_1.jpg", "raspberry_30.jpg"]
    assert e.lexicographical_list_converter(name_list) == None

    name_list = ["banana_1_10.jpg", "cherry_100_1.jpg", "raspberry_30_.jpg"]
    assert e.lexicographical_list_converter(name_list) == None
