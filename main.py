from time import sleep
from singleton.env_values_singleton import EnvValuesSingleton
from gateway.api_gateway import ApiGateway
from handlers.job_handler import job_handler_init

if __name__ == '__main__':
    print(f'Rabbit MQ - HOST: {EnvValuesSingleton().get_internal_queue_host()} -- PORT:{EnvValuesSingleton().get_internal_queue_port()}')

    # Configurar o logger
    #logging.basicConfig(level=logging.INFO)  # Defina o nível de severidade desejado

    # Registrar uma mensagem no log
    #logging.info(f'Rabbit MQ - HOST: {EnvValuesSingleton().get_internal_queue_host()} -- PORT:{EnvValuesSingleton().get_internal_queue_port()}')
    print("Running Component")
    wait_sec = 30
    print(f'Please, wait for {wait_sec} seconds')
    sleep(wait_sec)
    ApiGateway().run()
    job_handler_init()