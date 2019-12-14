from Engine.EngineManga.engineMangas import EngineMangas

e = EngineMangas()

liste = ["a_50_1.jpg", "a_1_8.png", "a_300_30.argent"]
result = e.lexicographical_list_converter(liste)
print(result)