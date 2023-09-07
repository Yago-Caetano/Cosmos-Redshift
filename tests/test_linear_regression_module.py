

from enums.queues_enum import QueuesEnum
from modules.linear_regression_module import LinearRegressionModule

def test_do_linear_regression_analysis():

    module = LinearRegressionModule()
    module.set_rabbit_mq_queue(QueuesEnum.LINEAR_REGRESSION_QUEUE.value) 

    #create fake dataset
    import pandas as pd
    import random

    # Criar um dicionário com 10 colunas numéricas e algumas linhas de dados aleatórios
    data = {
        'Coluna1': [random.randint(1, 100) for _ in range(100)],
        'Coluna2': [random.uniform(0, 1) for _ in range(100)],
        'Coluna3': [random.uniform(10, 100) for _ in range(100)],
        'Coluna4': [random.uniform(-1, 1) for _ in range(100)],
        'Coluna5': [random.gauss(50, 10) for _ in range(100)],
        'Coluna6': [random.randrange(1, 100, 2) for _ in range(100)],
        'Coluna7': [random.randint(0, 1000) for _ in range(100)],
        'Coluna8': [random.uniform(100, 200) for _ in range(100)],
        'Coluna9': [random.uniform(0, 100) for _ in range(100)],
        'Coluna10': [random.uniform(-100, 100) for _ in range(100)]
    }


    ret_module = module.perform_linear_regression(data,['Coluna1','Coluna2'], 'Coluna10')

    assert(ret_module != None)