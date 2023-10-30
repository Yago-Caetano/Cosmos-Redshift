import base64
import time
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from enums.action_enum import ActionEnum
from enums.argsKeysEnum import ArgsKeysEnums
from modules.base_module import BaseModule


class BidimensionalGraphModule(BaseModule):
    def on_start(self):
        pass

    def on_execute(self):
        super().on_execute()
        while True:
            try:
                #consome local queue data
                local_job = self.get_job_from_inner_queue()

                if(local_job != None):
                    if(local_job.get_next_pending_action().get_action() == ActionEnum.EXECUTE_BIDIMENSIONAL_ANALYSIS):
                        print(f'BidimensionalGraphModule: {local_job}')
                        #convert incoming data to dataframe
                        img = self.generate_bidimensional_analysis(local_job.get_args()[ArgsKeysEnums.DATASET.value],local_job.get_args()[ArgsKeysEnums.TWO_DIM_GRAPHIC_TARGET_COLLUMNS.value])

                        local_job.add_args(ArgsKeysEnums.RESULT_2D_GRAPH.value,img)

                        #set this action as Complete
                        self.finalize_job_as_succed(local_job)   
            except:
                self.finalize_job_as_failed(local_job)
                pass        


    def generate_bidimensional_analysis(self,dataframe, columns_to_analyze):
        
        matplotlib.use('Agg')

        df = pd.DataFrame(dataframe, columns=columns_to_analyze)

        # normalize data
        normalized_data = (df - df.mean()) / df.std()

        # Create heat map
        plt.figure(figsize=(10, 8))
        
        plt.plot(df[columns_to_analyze[0]])
        plt.plot(df[columns_to_analyze[1]])
        plt.xlabel(columns_to_analyze[0])
        plt.ylabel(columns_to_analyze[1])

        plt.title(f'Gráfico {columns_to_analyze[0]} x {columns_to_analyze[1]}')
        plt.savefig('grafico.png', format='png')

        #plt.show()
        with open('grafico.png', 'rb') as png_file:
            png_contents = png_file.read()

        # Codificar em base64
        base64_image = base64.b64encode(png_contents).decode('utf-8')

        plt.clf()

        return base64_image
        #plt.savefig('output.eps', format='eps', bbox_inches='tight')