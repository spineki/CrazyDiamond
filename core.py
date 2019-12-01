import time
from Engine.EngineTest.engineTest import EngineTest


class Core:
    def __init__(self):
        self.queue = []
        self.engines = []
        self.progress = 0.0
        self.id_count = 0
        self.current_task = None
        self.messages_to_display = []
        self.start_engines()

    def start_engines(self):
        e = EngineTest()
        self.addEngine(e)

    def addEngine(self, e):
        e.id = self.id_count
        self.id_count += 1
        self.engines.append(e)

    def get_all_engines(self):
        engines  = []
        for category in self.engines:
            for engine in self.engines[category]:
                engines.append(engine)
        return engines

    def task_analyzer(self, task):
        return None

    def get_reacting_motor(self, keyword):
        for engine in self.engines:
            if engine.react_to_keyword(keyword):
                return engine.__class__() # we reinit an object to avoir overloading

    # Handling message ****************************************************************************
    def error_handling_message(self, task):
        pass

    def success_handling_message(self, task):
        pass

    # RUN *****************************************************************************************
    def run_task(self, task):
        return None

    def pooling(self):
        while True:
            time.sleep(0.8)
            t = time.clock()
            if self.queue == []:
                continue

            self.current_task = self.queue.pop(0)
            handling = self.task_analyzer(self.current_task)
            if handling == False:
                self.error_handling_message(self.current_task)
                continue

            self.success_handling_message(self.current_task)
            self.progress = 0.0
            self.logs = self.run_task(handling)
            self.progress = 100.0
            t = time.clock() - t
            print("finished in ", t, "seconds")
