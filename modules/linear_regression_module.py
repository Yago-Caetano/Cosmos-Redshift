import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from enums.action_enum import ActionEnum
from enums.argsKeysEnum import ArgsKeysEnums

from modules.base_module import BaseModule


class LinearRegressionModule(BaseModule):
    def on_start(self):
        pass
        #return super().on_start()
    
    def on_execute(self):
        super().on_execute()
        while True:
            try:
                #consome local queue data
                local_job = self.__jobs.get()

                if(local_job != None):
                    if(local_job.get_next_pending_action().get_action() == ActionEnum.EXECUTE_LINEAR_REGRESSION):
                        print(local_job)
                        #convert incoming data to dataframe
                        self.perform_linear_regression(local_job.get_args()[ArgsKeysEnums.DATASET.value],local_job.get_args()[ArgsKeysEnums.COLLUMNS.value])
            except:
                pass


    def perform_linear_regression(self,dataset, columns_to_analyze, target_column):

        df = pd.DataFrame(dataset)

        df = df[columns_to_analyze + [target_column]]

        X = df[columns_to_analyze].values
        y = df[target_column].values

        model = LinearRegression()
        model.fit(X, y)

        parameters = {
            'intercept': model.intercept_,
            'coefficients': dict(zip(columns_to_analyze, model.coef_))
        }

        predictions = model.predict(X)

        plt.plot(predictions, color='blue')
        plt.plot(y, color='red')

        plt.ylabel(target_column)
        plt.title("Gráfico de Predição")
        #plt.show()

        return {"params": parameters, "figure": plt}