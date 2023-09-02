import threading
import time

import pika
from enums.queues_enum import QueuesEnum
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

    while True:

        # Configurações de conexão com o RabbitMQ
        conexao = pika.BlockingConnection(pika.ConnectionParameters(HOST))  # Altere para o endereço do seu servidor RabbitMQ, se necessário
        canal = conexao.channel()

        # Declaração da fila onde você deseja publicar mensagens
        fila = QueuesEnum.CORRELATION_QUEUE.value # Substitua pelo nome da sua fila

        # Mensagem que você deseja enviar
        mensagem = 'Esta é uma mensagem de exemplo'

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