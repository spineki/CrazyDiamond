from Engine.engine import Engine
import os

class EngineTest(Engine):

    def __init__(self):
        super().__init__()
        self.current_folder = os.path.dirname(__file__)

    def get_switch_task_template(self):
        task_template_file = os.path.join(self.current_folder, "task_template_engineTest.json")
        task_template = self.get_json_file(task_template_file)
        return task_template

    def switch(self):
        pass

    def switch_task_template(self, task_template):
        print("task_template reçu")