import time


class Core:
    def __init__(self):
        self.queue = []
        self.engines = []
        self.progress = 0.0
        self.current_task = None
        self.messages_to_display = []
        self.start_engines()

    def start_engines(self):
        """e = EngineLelscan()
        self.engines.append(e)
        e = EngineScansMangas()
        self.engines.append(e)"""
        pass

    def task_analyzer(self, task):
        return None

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
