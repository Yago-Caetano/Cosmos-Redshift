import json
import time
import requests
from enums.action_enum import ActionEnum
from enums.argsKeysEnum import ArgsKeysEnums
import pandas as pd
from enums.state_enum import StateEnum
from singleton.env_values_singleton import EnvValuesSingleton

from modules.base_module import BaseModule


class SthCometModule(BaseModule):


    def on_start(self):
        pass
        #return super().on_start()
    

    def __parse_raw_sth_data(self,payload):
        try:
            ret_dt = {}
            ret_list = []

            name = payload["contextResponses"][0]["contextElement"]["attributes"][0]["name"]

            #run over attr values
            values = payload["contextResponses"][0]["contextElement"]["attributes"][0]["values"]

            for value in values:
                ret_list.append(value["attrValue"])
                #print(f'{name} {value["attrValue"]}')

            ret_dt[name] = ret_list

            return [name,ret_dt]

        except Exception as e:
            print(e)
            return None

    def consume_sth(self, entity_id, type, attr, query_param, fiware_service, service_path):
        try:
            
            enspoint_str = f'http://{EnvValuesSingleton().get_internal_sth_host()}:{EnvValuesSingleton().get_internal_sth_port()}/STH/v1/contextEntities/type/{type}/id/{entity_id}/attributes/{attr}'

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
                ret_dt = {}
                
                #consome local queue data
                local_job = self.get_job_from_inner_queue()
                print(f'STH Comet reading: {local_job}')
                if(local_job != None):
                    if(local_job.get_next_pending_action().get_action() == ActionEnum.GET_STH_COMET_DATA):
                        print(local_job)

                        for attr in local_job.get_args()[ArgsKeysEnums.FIWARE_ATTRS.value]:
                            #convert incoming data to dataframe
                            sth_data = self.consume_sth(local_job.get_args()[ArgsKeysEnums.FIWARE_ENTITY.value],local_job.get_args()[ArgsKeysEnums.FIWARE_ENTITY_TYPE.value],attr,local_job.get_args()[ArgsKeysEnums.STH_AGGR_METHOD.value],local_job.get_args()[ArgsKeysEnums.FIWARE_SERVICE.value],local_job.get_args()[ArgsKeysEnums.FIWARE_SERVICE_PATH.value])

                            print(sth_data)
                            if(len(sth_data) > 0):
                                #parse return data
                                [name,collum] = self.__parse_raw_sth_data(sth_data)
                                ret_dt[name] = collum[name]
                            print(ret_dt)
                        
                        local_job.add_args(ArgsKeysEnums.DATASET.value,ret_dt)

                        #set this action as Complete
                        self.finalize_job_as_succed(local_job)

            except Exception as e:
                print(e)
                self.finalize_job_as_failed(local_job)
                pass
