from Engine.engine import Engine
import os

class EngineTests(Engine):
    """
    The super Class `EngineTests` is not designed to be instanciated, but to be inherited from.

        It handles nothing and it's only purpose is only to test the module architecture without launching downloads.

    """
    def __init__(self):
        super().__init__()
        self.current_folder = os.path.dirname(__file__)
        self.category = "Test"