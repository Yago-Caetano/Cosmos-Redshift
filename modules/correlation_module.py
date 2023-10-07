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


class CorrelationModule(BaseModule):
    def on_start(self):
        pass

    def on_execute(self):
        super().on_execute()
        while True:
            try:
                #consome local queue data
                local_job = self.get_job_from_inner_queue()

                if(local_job != None):
                    print(f'Correlation_module job taken: {local_job.get_next_pending_action().get_action()}')
                    if(local_job.get_next_pending_action().get_action() == ActionEnum.EXECUTE_CORRELATION_ANALYSIS):
                        print(f'CORRELATION_MODULE: {local_job}')
                        #convert incoming data to dataframe
                        img = self.analyze_and_visualize_correlations(local_job.get_args()[ArgsKeysEnums.DATASET.value],local_job.get_args()[ArgsKeysEnums.CORRELATION_TARGET_COLLUMNS.value])

                        local_job.add_args(ArgsKeysEnums.RESULT_CORRELATION.value,img)

                        #set this action as Complete
                        self.finalize_job_as_succed(local_job)   
            except Exception as e:
                print(f'{e}')        


    def analyze_and_visualize_correlations(self,dataframe, columns_to_analyze):
        
        matplotlib.use('Agg')

        df = pd.DataFrame(dataframe, columns=columns_to_analyze)

        # normalize data
        normalized_data = (df - df.mean()) / df.std()

        correlations = normalized_data.corr()
        if(len(columns_to_analyze) < 10):
            plt.figure(figsize=(10, 8))
        else:
            height = len(columns_to_analyze)
            # Create heat map
            plt.figure(figsize=(height, int(height/1.25)))

        sns.heatmap(correlations, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
        plt.title("Mapa de Calor das Correlações entre Colunas")
        plt.savefig('grafico.png', format='png')

        #plt.show()
        with open('grafico.png', 'rb') as png_file:
            png_contents = png_file.read()

        # Codificar em base64
        base64_image = base64.b64encode(png_contents).decode('utf-8')

        plt.clf()

        return base64_image
        #plt.savefig('output.eps', format='eps', bbox_inches='tight')