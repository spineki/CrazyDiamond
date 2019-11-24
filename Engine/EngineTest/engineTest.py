from Engine.EngineTest.engineTests import EngineTests
import os

class EngineTest(EngineTests):

    def __init__(self):
        super().__init__()
        self.current_folder = os.path.dirname(__file__)
        self.name = "test"

    def get_task_template(self):
        task_template_file = os.path.join(self.current_folder, "task_template_engineTest.json")
        task_template = self.get_json_file(task_template_file)
        return task_template

    def switch(self):
        pass

    def switch_task_template(self, task_template):
        print("task_template reçu")