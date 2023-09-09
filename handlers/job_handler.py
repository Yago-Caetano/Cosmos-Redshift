import threading
import time

import pika
from enums.queues_enum import QueuesEnum
from enums.argsKeysEnum import ArgsKeysEnums
from enums.target_enum import TargetEnum
from models.action_model import ActionModel
from models.job_model import JobModel
from utils.job_utils import JobUtils
from modules.sth_comet_module import SthCometModule
from modules.linear_regression_module import LinearRegressionModule
from modules.correlation_module import CorrelationModule
from enums.action_enum import ActionEnum


HOST = 'localhost'

channel = None
connection = None

def post_msg():

    global channel
    global connection



    # Configurações de conexão com o RabbitMQ
    conexao = pika.BlockingConnection(pika.ConnectionParameters(HOST))  # Altere para o endereço do seu servidor RabbitMQ, se necessário
    canal = conexao.channel()

    # Declaração da fila onde você deseja publicar mensagens
    fila = QueuesEnum.STH_COMET_QUEUE.value # Substitua pelo nome da sua fila

    # Mensagem que você deseja enviar
    #mensagem = '{"JOB_ID": "123", "ARGS": { "entity": "urn:ngsi-ld:entity:986463ec-3f51-11ee-be56-0242ac120002", "type": "eggProduction", "attribute": "cracked_eggs", "fiware_service": "smart", "fiware_service_path": "/", "sth_aggr": "lastN=10"  }, "ACTIONS": [{"TARGET": "STH_COMET", "IN_ARGS": "", "STATE": 0, "ACTION": "GET_STH_COMET_DATA"}]}'

    collect_job = JobModel("123")
    collect_job.add_args(ArgsKeysEnums.FIWARE_ENTITY.value,"urn:ngsi-ld:entity:986463ec-3f51-11ee-be56-0242ac120002")
    collect_job.add_args(ArgsKeysEnums.FIWARE_ENTITY_TYPE.value,"eggProduction")
    collect_job.add_args(ArgsKeysEnums.FIWARE_ATTRS.value,["cracked_eggs","temperature"])
    collect_job.add_args(ArgsKeysEnums.FIWARE_SERVICE.value,"smart")
    collect_job.add_args(ArgsKeysEnums.FIWARE_SERVICE_PATH.value,"/")
    collect_job.add_args(ArgsKeysEnums.STH_AGGR_METHOD.value,"lastN=10")

    action = ActionModel()
    action.set_target(TargetEnum.TARGET_STH_COMET)
    action.set_action(ActionEnum.GET_STH_COMET_DATA)

    collect_job.add_action(action)

    mensagem = JobUtils().convert_job_to_json(collect_job)

    if(mensagem != None):
        print(mensagem)
        # Publica a mensagem na fila
        canal.basic_publish(exchange='', routing_key=fila, body=mensagem)

        print(f"Mensagem enviada para a fila {fila}: {mensagem}")

    # Fecha a conexão
    conexao.close()
    time.sleep(5)


def consume_rabbit_mq():

    global channel
    global connection

    # Inicie o loop para escutar a fila indefinidamente
    channel.start_consuming()


def read_cb(ch, method, properties, body):
    print(f"{__name__} Recebido: {body.decode('utf-8')}")

    #try to convert data to job format
    job = JobUtils().convert_json_to_job(body.decode('utf-8'))

    if(job == None):
        print("Failed to parse JOB")


def connect_to_main_queue():

    global channel
    global connection

    # Configurações de conexão com o RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(HOST))

    channel = connection.channel()
    channel.queue_declare(queue=QueuesEnum.MAIN_QUEUE.value)
    
    # Create callback
    channel.basic_consume(queue=QueuesEnum.MAIN_QUEUE.value, on_message_callback=read_cb, auto_ack=True)

    # Crie e inicie a thread de consumo
    consume_thread = threading.Thread(target=consume_rabbit_mq)
    consume_thread.start()

    post_msg()



def job_handler_init():
    #initialize specialist modules
    correlation_module = CorrelationModule()
    correlation_module.set_rabbit_mq_queue(QueuesEnum.CORRELATION_QUEUE.value)
    correlation_module.start()


    linear_regression_module = LinearRegressionModule()
    linear_regression_module.set_rabbit_mq_queue(QueuesEnum.LINEAR_REGRESSION_QUEUE.value)
    linear_regression_module.start()

    sth_comet_module = SthCometModule()
    sth_comet_module.set_rabbit_mq_queue(QueuesEnum.STH_COMET_QUEUE.value)
    sth_comet_module.start()

    connect_to_main_queue()