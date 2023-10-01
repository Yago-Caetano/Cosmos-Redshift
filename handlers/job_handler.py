import threading
import time

import pika
from enums.queues_enum import QueuesEnum
from enums.argsKeysEnum import ArgsKeysEnums
from enums.target_enum import TargetEnum
from modules.two_dimmensional_graph_module import BidimensionalGraphModule
from singleton.env_values_singleton import EnvValuesSingleton
from models.action_model import ActionModel
from models.job_model import JobModel
from utils.job_utils import JobUtils
from modules.sth_comet_module import SthCometModule
from modules.linear_regression_module import LinearRegressionModule
from modules.correlation_module import CorrelationModule
from enums.action_enum import ActionEnum



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

    pending_action = job.get_next_pending_action()

    if(pending_action == None):
        print(f'O trabalho {job.get_id()} foi ENCERRADO!!')

        print("Raw data")
        print(body)
        return
    
    #check next available job and dispatch it
    if(pending_action.get_action() == ActionEnum.EXECUTE_CORRELATION_ANALYSIS):

        # Configurações de conexão com o RabbitMQ
        conexao = pika.BlockingConnection(pika.ConnectionParameters(EnvValuesSingleton().get_internal_queue_host()))  # Altere para o endereço do seu servidor RabbitMQ, se necessário
        canal = conexao.channel()

        # Declaração da fila onde você deseja publicar mensagens
        fila = QueuesEnum.CORRELATION_QUEUE.value # Substitua pelo nome da sua fila

        mensagem = JobUtils().convert_job_to_json(job)

        if(mensagem != None):
            print(mensagem)
            # Publica a mensagem na fila
            canal.basic_publish(exchange='', routing_key=fila, body=mensagem)

            print(f"Mensagem enviada para a fila {fila}: {mensagem}")

        # Fecha a conexão
        conexao.close()

    elif(pending_action.get_action() == ActionEnum.EXECUTE_LINEAR_REGRESSION):
        
        # Configurações de conexão com o RabbitMQ
        conexao = pika.BlockingConnection(pika.ConnectionParameters(EnvValuesSingleton().get_internal_queue_host()))  # Altere para o endereço do seu servidor RabbitMQ, se necessário
        canal = conexao.channel()

        # Declaração da fila onde você deseja publicar mensagens
        fila = QueuesEnum.LINEAR_REGRESSION_QUEUE.value # Substitua pelo nome da sua fila

        mensagem = JobUtils().convert_job_to_json(job)

        if(mensagem != None):
            print(mensagem)
            # Publica a mensagem na fila
            canal.basic_publish(exchange='', routing_key=fila, body=mensagem)

            print(f"Mensagem enviada para a fila {fila}: {mensagem}")

        # Fecha a conexão
        conexao.close()

    elif(pending_action.get_action() == ActionEnum.GET_STH_COMET_DATA):

        # Configurações de conexão com o RabbitMQ
        conexao = pika.BlockingConnection(pika.ConnectionParameters(EnvValuesSingleton().get_internal_queue_host()))  # Altere para o endereço do seu servidor RabbitMQ, se necessário
        canal = conexao.channel()

        # Declaração da fila onde você deseja publicar mensagens
        fila = QueuesEnum.STH_COMET_QUEUE.value # Substitua pelo nome da sua fila

        mensagem = JobUtils().convert_job_to_json(job)

        if(mensagem != None):
            print(mensagem)
            # Publica a mensagem na fila
            canal.basic_publish(exchange='', routing_key=fila, body=mensagem)

            print(f"Mensagem enviada para a fila {fila}: {mensagem}")

        # Fecha a conexão
        conexao.close()

    elif((pending_action.get_action() == ActionEnum.SEND_RESPONSE_TO_API_GATEWAY) or (pending_action.get_action() == ActionEnum.SEND_ASYNC_RESPONSE_TO_API_GATEWAY)):
        # Configurações de conexão com o RabbitMQ
        conexao = pika.BlockingConnection(pika.ConnectionParameters(EnvValuesSingleton().get_internal_queue_host()))  # Altere para o endereço do seu servidor RabbitMQ, se necessário
        canal = conexao.channel()

        # Declaração da fila onde você deseja publicar mensagens
        fila = QueuesEnum.API_GATEWAY_RESPONSE_QUEUE.value

        mensagem = JobUtils().convert_job_to_json(job)

        if(mensagem != None):
            print(mensagem)
            # Publica a mensagem na fila
            canal.basic_publish(exchange='', routing_key=fila, body=mensagem)

            print(f"Mensagem enviada para a fila {fila}: {mensagem}")

        # Fecha a conexão
        conexao.close()

    elif((pending_action.get_action() == ActionEnum.EXECUTE_BIDIMENSIONAL_ANALYSIS) or (pending_action.get_action() == ActionEnum.EXECUTE_BIDIMENSIONAL_ANALYSIS)):
        
        # Configurações de conexão com o RabbitMQ
        conexao = pika.BlockingConnection(pika.ConnectionParameters(EnvValuesSingleton().get_internal_queue_host()))  # Altere para o endereço do seu servidor RabbitMQ, se necessário
        canal = conexao.channel()

        # Declaração da fila onde você deseja publicar mensagens
        fila = QueuesEnum.TWO_DIMENSIONAL_GRAPH.value

        mensagem = JobUtils().convert_job_to_json(job)

        if(mensagem != None):
            print(mensagem)
            # Publica a mensagem na fila
            canal.basic_publish(exchange='', routing_key=fila, body=mensagem)

            print(f"Mensagem enviada para a fila {fila}: {mensagem}")

        # Fecha a conexão
        conexao.close()


def connect_to_main_queue():

    global channel
    global connection

    # Configurações de conexão com o RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(EnvValuesSingleton().get_internal_queue_host()))

    channel = connection.channel()
    channel.queue_declare(queue=QueuesEnum.MAIN_QUEUE.value)
    
    # Create callback
    channel.basic_consume(queue=QueuesEnum.MAIN_QUEUE.value, on_message_callback=read_cb, auto_ack=True)

    # Crie e inicie a thread de consumo
    consume_thread = threading.Thread(target=consume_rabbit_mq)
    consume_thread.start()

    #post_msg()



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

    two_dimensional_graph_module = BidimensionalGraphModule()
    two_dimensional_graph_module.set_rabbit_mq_queue(QueuesEnum.TWO_DIMENSIONAL_GRAPH.value)
    two_dimensional_graph_module.start()

    connect_to_main_queue()