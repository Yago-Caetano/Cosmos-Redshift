import time
from modules.base_module import BaseModule


class SthCometModule(BaseModule):

    def on_start(self):
        pass
        #return super().on_start()
    
    def on_execute(self):
        super().on_execute()
        while True:
            try:
                time.sleep(1)
                #print("Running")
            except:
                pass
