
import time
import pika
import requests

from flask import Flask, request
import threading
from enums.queues_enum import QueuesEnum
from singleton.env_values_singleton import EnvValuesSingleton
from utils.job_utils import JobUtils
from models.job_model import JobModel
from utils.api_utils import ApiRequestUtils

from utils import api_utils

class ApiGateway():

    def __init__(self) -> None:
        self.__app = Flask(__name__)
        self.__app.add_url_rule('/api/availableEntities', 'collect_available_entities', self.collect_available_entities, methods=['GET'])
        self.__app.add_url_rule('/api/sync/requestAnalysis', 'request_sync_analysis', self.request_sync_analysis, methods=['POST'])
        self.__app.add_url_rule('/api/requestAnalysis', 'request_analysis', self.request_async_analysis, methods=['POST'])
        self.__pending_job_id = None
        self.__wainting_for_job_conclusion = False

        self.__resp_job = None

    def read_cb(self,ch, method, properties, body):

        print(f"{__name__} Recebido: {body.decode('utf-8')}")

        #try to convert data to job format
        job = JobUtils().convert_json_to_job(body.decode('utf-8'))

        if(job == None):
            return
        
        if((self.__wainting_for_job_conclusion == True) and (self.__pending_job_id == job.get_id())):
            self.__resp_job = job
            self.__wainting_for_job_conclusion = False

    def __consome_api_resp_queue(self):
        
        # Configurações de conexão com o RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(EnvValuesSingleton().get_internal_queue_host()))

        channel = connection.channel()
        channel.queue_declare(queue=QueuesEnum.API_GATEWAY_RESPONSE_QUEUE.value)
        
        # Create callback
        channel.basic_consume(queue=QueuesEnum.API_GATEWAY_RESPONSE_QUEUE.value, on_message_callback=self.read_cb, auto_ack=True)

        # Inicie o loop para escutar a fila indefinidamente
        channel.start_consuming()


    def run(self):
        # Inicia a aplicação Flask em uma thread separada
        self.flask_thread = threading.Thread(target=self.__app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
        self.flask_thread.daemon = True
        self.flask_thread.start()

        # Inicia o Consumo da fila de respostas ao API gateway
        self.resp_queue_handler = threading.Thread(target=self.__consome_api_resp_queue)
        self.resp_queue_handler.daemon = True
        self.resp_queue_handler.start()


    def __post_msg(self,job:JobModel):

        global channel
        global connection

        # Configurações de conexão com o RabbitMQ
        conexao = pika.BlockingConnection(pika.ConnectionParameters(EnvValuesSingleton().get_internal_queue_host()))  # Altere para o endereço do seu servidor RabbitMQ, se necessário
        canal = conexao.channel()

        fila = QueuesEnum.MAIN_QUEUE.value # Substitua pelo nome da sua fila

        mensagem = JobUtils().convert_job_to_json(job)

        if(mensagem != None):
            print(mensagem)
            # Publica a mensagem na fila
            canal.basic_publish(exchange='', routing_key=fila, body=mensagem)

            print(f"Mensagem enviada para a fila {fila}: {mensagem}")

        # Fecha a conexão
        conexao.close()

    def request_sync_analysis(self):
        job = ApiRequestUtils().convert_request_to_job(request.json)

        if(job == None):
            return "Requisição Inválida",400

        self.__pending_job_id = job.get_id()
        self.__wainting_for_job_conclusion = True

        self.__post_msg(job)


        while(self.__wainting_for_job_conclusion == True):
            time.sleep(0.01)

        return JobUtils().convert_job_to_json(self.__resp_job)
    
    def request_async_analysis(self):
        job = ApiRequestUtils().convert_request_to_job(request.json)

        if(job == None):
            return "Requisição Inválida",400
        
        self.__post_msg(job)



        return "Análise Assincrona"



    def collect_available_entities(self):
        try:

            enspoint_str = f'http://{EnvValuesSingleton().get_orion_host()}:{EnvValuesSingleton().get_orion_port()}/v2/entities'

            headers = {"fiware-service":"smart","fiware-servicepath":"/"}

            response = requests.get(enspoint_str, headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                print(enspoint_str)
                print(f"Erro na solicitação GET. Código de status: {response.status_code}")
                return None
            
        except requests.exceptions.RequestException as e:
            print(f"Erro na solicitação GET: {str(e)}")
            return None


    def parse_api_request(self):
        pass
