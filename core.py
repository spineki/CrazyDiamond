import time
from Engine.EngineTest.engineTest import EngineTest
import threading, queue
import time

class Core:
    """Class Core that manages task affectation to pluggin-engines
    """

    def __init__(self):
        self.task_queue = queue.Queue()
        threading.Thread(target=self.pooling, daemon=True).start()


    def add_new_Task(self, function, args= None, kwargs = {}, startCallback=lambda x: None, callback=lambda x: None, endCallback=lambda x: None):
        self.task_queue.put((function, args, kwargs, startCallback, callback, endCallback))

    def pooling(self):
        while True:
            time.sleep(0.250)
            function, args, kwargs, startCallback, callback, endCallback = self.task_queue.get()
            startCallback(args)
            result = function(*args, **kwargs)
            endCallback(result)



