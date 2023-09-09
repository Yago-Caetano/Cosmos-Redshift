from abc import ABC, abstractmethod
from queue import Queue
import threading
import pika
from enums.state_enum import StateEnum
from enums.queues_enum import QueuesEnum

from utils.job_utils import JobUtils

class BaseModule(ABC):

    def __init__(self):
        self.__jobs = Queue()
        self._external_queue = None
        self._external_queue_port = None
        self.__queue_channel = None
        self.__connection = None
        self.__thread = None
        self.__hostname = 'localhost'

        super().__init__()


    def set_rabbit_mq_queue(self,queue):
        self._external_queue = queue
        
    # Função para processar mensagens recebidas
    def __callback(self,ch, method, properties, body):
        #print(f"{__name__} Recebido: {body.decode('utf-8')}")
        job =JobUtils().convert_json_to_job(body.decode('utf-8'))

        if(job != None):
            #append into local queue
            self.__jobs.put(job)

    def __consume_rabbit_mq(self):
        # Inicie o loop para escutar a fila indefinidamente
        self.__queue_channel.start_consuming()

    def finalize_job_as_succed(self,job):
        job.get_next_pending_action().set_state(StateEnum.DONE)

        #dispatch job to main queue
        self.__post_job_to_main_queue(job)

    def __post_job_to_main_queue(self,job):

        HOST = 'localhost'
        
        # Configurações de conexão com o RabbitMQ
        conexao = pika.BlockingConnection(pika.ConnectionParameters(HOST))  # Altere para o endereço do seu servidor RabbitMQ, se necessário
        canal = conexao.channel()

        # Declaração da fila onde você deseja publicar mensagens
        fila = QueuesEnum.MAIN_QUEUE.value # Substitua pelo nome da sua fila

        mensagem = JobUtils().convert_job_to_json(job)
        print(mensagem)
        if(mensagem != None):
            print(mensagem)
            # Publica a mensagem na fila
            canal.basic_publish(exchange='', routing_key=fila, body=mensagem)

            print(f"Mensagem enviada para a fila {fila}: {mensagem}")

        # Fecha a conexão
        conexao.close()


    def get_job_from_inner_queue(self):
        return self.__jobs.get()

    @abstractmethod
    def on_start(self):
        '''
            Method invoked on first execution of worker
        '''
        raise NotImplementedError


    @abstractmethod
    def on_execute(self):
        '''
            Read RabbitMQ queue
        '''

        # Configurações de conexão com o RabbitMQ
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(self.__hostname))

        self.__queue_channel = self.__connection.channel()
        self.__queue_channel.queue_declare(queue=self._external_queue)

        # Create callback
        self.__queue_channel.basic_consume(queue=self._external_queue, on_message_callback=self.__callback, auto_ack=True)

        # Crie e inicie a thread de consumo
        self.__thread_consumo = threading.Thread(target=self.__consume_rabbit_mq)
        self.__thread_consumo.start()



    def start(self):
        try:
            self.on_start()

            if((self.__thread is None) or (not self.__thread.is_alive())):
                self.__thread = threading.Thread(target=self.on_execute)
                self.__thread.start()

        except Exception as e:
            print(e)

