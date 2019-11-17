from Engine.engine import Engine
import os

class EngineTests(Engine):

    def __init__(self):
        super().__init__()
        self.current_folder = os.path.dirname(__file__)
        self.category = "Test"