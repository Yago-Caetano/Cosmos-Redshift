

import os

from dotenv import load_dotenv

from singleton.singleton_meta import SingletonMeta


class EnvValuesSingleton(metaclass=SingletonMeta):

    def __init__(self) -> None:
        #load_dotenv()
        self.__internal_rb_queue_host = os.environ.get("INTERNAL_RABBIT_MQ_HOST")
        self.__internal_rb_queue_port = os.environ.get("INTERNAL_RABBIT_MQ_PORT")

        self.__sth_host = os.getenv("STH_COMET_HOST")
        self.__sth_port = os.getenv("STH_COMET_PORT")

        self.__orion_host = os.getenv("ORION_CONTEXT_BROKER_HOST")
        self.__orion_port = os.getenv("ORION_CONTEXT_BROKER_PORT")

        self.__fiware_service = os.getenv("FIWARE_SERVICE")
        self.__fiware_service_path = os.getenv("FIWARE_SERVICE_PATH")

    def get_internal_queue_host(self):
        return self.__internal_rb_queue_host

    def get_internal_queue_port(self):
        return self.__internal_rb_queue_port
  
    def get_internal_sth_host(self):
        return self.__sth_host
    
    def get_internal_sth_port(self):
        return self.__sth_port
    
    def get_orion_host(self):
        return self.__orion_host
    
    def get_orion_port(self):
        return self.__orion_port
    
    def get_fiware_service(self):
        return self.__fiware_service
    
    def get_fiware_service_path(self):
        return self.__fiware_service_path