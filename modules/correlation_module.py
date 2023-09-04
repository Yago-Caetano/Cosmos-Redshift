import time
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
            #consome local queue data
            local_job = self.__jobs.get()

            if(local_job != None):
                if(local_job.get_next_pending_action().get_action() == ActionEnum.EXECUTE_CORRELATION_ANALYSIS):
                    print(local_job)
                    #convert incoming data to dataframe
                    self.analyze_and_visualize_correlations(local_job.get_args()[ArgsKeysEnums.DATASET.value],local_job.get_args()[ArgsKeysEnums.COLLUMNS.value])
                    


    def analyze_and_visualize_correlations(self,dataframe, columns_to_analyze):

        df = pd.DataFrame(dataframe, columns=columns_to_analyze)

        # normalize data
        normalized_data = (df - df.mean()) / df.std()

        correlations = normalized_data.corr()

        # Create heat map
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlations, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
        plt.title("Mapa de Calor das Correlações entre Colunas")
        #plt.show()

        plt.savefig('output.eps', format='eps', bbox_inches='tight')