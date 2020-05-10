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


    def add_new_Task(self, function, args= None, kwargs = {}):
        self.task_queue.put((function, args, kwargs))
        print("size: ", self.task_queue.qsize())

    def pooling(self):
        while True:
            time.sleep(0.250)
            print(self.task_queue)
            function, args, kwargs = self.task_queue.get()
            result = function(*args, **kwargs)



