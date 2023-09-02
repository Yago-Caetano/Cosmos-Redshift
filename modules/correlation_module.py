
import time
from modules.base_module import BaseModule


class CorrelationModule(BaseModule):
    def on_start(self):
        pass

    def on_execute(self):
        super().on_execute()
        while True:
            time.sleep(1)
            print("Running")