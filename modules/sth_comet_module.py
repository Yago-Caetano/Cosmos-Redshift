import time
import requests
from enums.action_enum import ActionEnum
from enums.argsKeysEnum import ArgsKeysEnums

from modules.base_module import BaseModule


class SthCometModule(BaseModule):


    def on_start(self):
        pass
        #return super().on_start()
    

    def consume_sth(self, entity_id, type, attr, query_param, fiware_service, service_path):
        try:
            
            HOST = "localhost"
            STH_PORT = 8666

            enspoint_str = f'http://{HOST}:{STH_PORT}/STH/v1/contextEntities/type/{type}/id/{entity_id}/attributes/{attr}'

            if(query_param != None):
                enspoint_str += f'?{query_param}'


            headers = {"fiware-service":fiware_service,"fiware-servicepath":service_path}

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


    def on_execute(self):
        super().on_execute()
        while True:
            try:
                #consome local queue data
                local_job = self.get_job_from_inner_queue()
                print(f'STH Comet reading: {local_job}')
                if(local_job != None):
                    if(local_job.get_next_pending_action().get_action() == ActionEnum.GET_STH_COMET_DATA.value):
                        print(local_job)


                        #convert incoming data to dataframe
                        sth_data = self.consume_sth(local_job.get_args()[ArgsKeysEnums.FIWARE_ENTITY.value],local_job.get_args()[ArgsKeysEnums.FIWARE_ENTITY_TYPE.value],local_job.get_args()[ArgsKeysEnums.FIWARE_ATTRS.value],local_job.get_args()[ArgsKeysEnums.STH_AGGR_METHOD.value],local_job.get_args()[ArgsKeysEnums.FIWARE_SERVICE.value],local_job.get_args()[ArgsKeysEnums.FIWARE_SERVICE_PATH.value])

                        print(sth_data)
            except Exception as e:
                print(e)
                pass
