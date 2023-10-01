import base64
import time
import matplotlib
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
                local_job = self.get_job_from_inner_queue()

                if(local_job != None):
                    if(local_job.get_next_pending_action().get_action() == ActionEnum.EXECUTE_LINEAR_REGRESSION):
                        print(local_job)
                        #convert incoming data to dataframe
                        img = self.perform_linear_regression(local_job.get_args()[ArgsKeysEnums.DATASET.value],local_job.get_args()[ArgsKeysEnums.LINEAR_REG_ANALYSE_COLLUMNS.value],local_job.get_args()[ArgsKeysEnums.LINEAR_REG_TARGET_COLLUMNS.value])

                        print(img)

                        local_job.add_args(ArgsKeysEnums.RESULT_LINEAR_REGRESSION.value,img)

                        #set this action as Complete
                        self.finalize_job_as_succed(local_job)   
            except Exception as e:
                print(e)
                pass


    def perform_linear_regression(self,dataset, columns_to_analyze, target_column):
        matplotlib.use('Agg')

        df = pd.DataFrame(dataset)

        df = df[columns_to_analyze + [target_column]]

        X = df[columns_to_analyze].values
        y = df[target_column].values

        model = LinearRegression()
        model.fit(X, y)


        parameters = {
            'intercept':  model.intercept_.tolist(),
            'coefficients': model.coef_.tolist()
        }

        predictions = model.predict(X)

        plt.plot(predictions, color='blue')
        plt.plot(y, color='red')

        plt.ylabel(target_column)
        plt.title("Gráfico de Predição")
        #plt.show()

        plt.savefig('grafico.png', format='png')

        #plt.show()
        with open('grafico.png', 'rb') as png_file:
            png_contents = png_file.read()

        # Codificar em base64
        base64_image = base64.b64encode(png_contents).decode('utf-8')

        plt.clf()

        return {ArgsKeysEnums.RESULT_LINEAR_REGRESSION_PARAMS.value: parameters, ArgsKeysEnums.RESULT_LINEAR_REGRESSION_FIGURE.value: base64_image}