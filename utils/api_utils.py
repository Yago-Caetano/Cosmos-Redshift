import json
import time
from enums.api_request_fields_enum import ApiRequestFieldsEnum
from enums.api_actions_enum import ApiActionsEnum
from enums.argsKeysEnum import ArgsKeysEnums
from enums.action_enum import ActionEnum
from enums.target_enum import TargetEnum
from singleton.env_values_singleton import EnvValuesSingleton
from models.action_model import ActionModel
from models.job_model import JobModel


class ApiRequestUtils():
        
    def __init__(self) -> None:
        pass

    def __check_string_belongs_to_enum(self,string,enum):
        for status in enum:
            if status.value == string:
                return status
        return None
    
    def __check_string_is_key_from_dict(self,dict,string):
        ret = False
        keys = dict.keys()
        for key in keys:
            if(string in key):
                ret = True
                break
        return ret

    def parse_sth_aggregation_options(self,sth_agg_args, job:JobModel):
        #recuperar a listagem e montar a query de acordo com 

        #for aggr_met in sth_agg_args:
            

        pass


    def convert_to_sucess_msg(self,job:JobModel):
        ret_dict = {"response":"SUCESS"}

        if(ArgsKeysEnums.RESULT_CORRELATION.value in job.get_args()):
            ret_dict["img"] = job.get_args()[ArgsKeysEnums.RESULT_CORRELATION.value]

        if(ArgsKeysEnums.RESULT_LINEAR_REGRESSION.value in job.get_args()):
            ret_dict["params"] = job.get_args()[ArgsKeysEnums.RESULT_LINEAR_REGRESSION.value][ArgsKeysEnums.RESULT_LINEAR_REGRESSION_PARAMS.value]
            ret_dict["img"] = job.get_args()[ArgsKeysEnums.RESULT_LINEAR_REGRESSION.value][ArgsKeysEnums.RESULT_LINEAR_REGRESSION_FIGURE.value]
        
        if(ArgsKeysEnums.RESULT_2D_GRAPH.value in job.get_args()):
            ret_dict["img"] = job.get_args()[ArgsKeysEnums.RESULT_2D_GRAPH.value]

        return json.dumps(ret_dict)

    def convert_request_to_job(self,request_dict,async_job:bool) -> JobModel:
        try:
            retJob = JobModel(str(int(time.time())))

            retJob.add_args(ArgsKeysEnums.FIWARE_SERVICE.value,EnvValuesSingleton().get_fiware_service())
            retJob.add_args(ArgsKeysEnums.FIWARE_SERVICE_PATH.value,EnvValuesSingleton().get_fiware_service_path())

            #first, check if action is valid
            if(request_dict[ApiRequestFieldsEnum.ACTION.value] == None):
                return None

            action = self.__check_string_belongs_to_enum(request_dict[ApiRequestFieldsEnum.ACTION.value],ApiActionsEnum)

            if(action == None):
                return None
            
            #check if collumns were set
            if(request_dict[ApiRequestFieldsEnum.DATA_COLLUMNS.value] == None):
                return None
            
            #check if entity id and entity type was provided
            if(request_dict[ApiRequestFieldsEnum.ENTITY.value] == None):
                return None
            
            if(request_dict[ApiRequestFieldsEnum.ENTITY_TYPE.value] == None):
                return None
            
            #according job action, data columns should assume specific arg on job
            if(action == ApiActionsEnum.CORRELATION_ANALYSIS):
                #entity id
                retJob.add_args(ArgsKeysEnums.FIWARE_ENTITY.value,request_dict[ApiRequestFieldsEnum.ENTITY.value])

                #entity type
                retJob.add_args(ArgsKeysEnums.FIWARE_ENTITY_TYPE.value,request_dict[ApiRequestFieldsEnum.ENTITY_TYPE.value])

                #data to collect
                aux_datas_to_retrieve = []
                for data in request_dict[ApiRequestFieldsEnum.DATA_COLLUMNS.value]:
                    aux_datas_to_retrieve.append(data)

                retJob.add_args(ArgsKeysEnums.FIWARE_ATTRS.value,aux_datas_to_retrieve)

                if ApiRequestFieldsEnum.STH_AGGREGATION.value in request_dict:
                    #aggregration mode

                    retJob.add_args(ArgsKeysEnums.STH_AGGR_METHOD.value,request_dict[ApiRequestFieldsEnum.STH_AGGREGATION.value])
                else:
                    retJob.add_args(ArgsKeysEnums.STH_AGGR_METHOD.value,"lastN=100")


                retJob.add_args(ArgsKeysEnums.CORRELATION_TARGET_COLLUMNS.value,aux_datas_to_retrieve)

                #include actions
                sth_action = ActionModel()
                sth_action.set_target(TargetEnum.TARGET_STH_COMET)
                sth_action.set_action(ActionEnum.GET_STH_COMET_DATA)

                action_corr = ActionModel()
                action_corr.set_target(TargetEnum.TARGET_CORRELATION_MODULE)
                action_corr.set_action(ActionEnum.EXECUTE_CORRELATION_ANALYSIS)

                retJob.add_action(sth_action)
                retJob.add_action(action_corr)

            elif(action == ApiActionsEnum.LINEAR_REGRESSION_ANALYSIS):
                #entity id
                retJob.add_args(ArgsKeysEnums.FIWARE_ENTITY.value,request_dict[ApiRequestFieldsEnum.ENTITY.value])

                #entity type
                retJob.add_args(ArgsKeysEnums.FIWARE_ENTITY_TYPE.value,request_dict[ApiRequestFieldsEnum.ENTITY_TYPE.value])
                #data to collect
                aux_datas_to_retrieve = []
                for data in request_dict[ApiRequestFieldsEnum.DATA_COLLUMNS.value]:
                    aux_datas_to_retrieve.append(data)

                retJob.add_args(ArgsKeysEnums.FIWARE_ATTRS.value,aux_datas_to_retrieve)

                if ApiRequestFieldsEnum.STH_AGGREGATION.value in request_dict:
                    #aggregration mode
                    retJob.add_args(ArgsKeysEnums.STH_AGGR_METHOD.value,request_dict[ApiRequestFieldsEnum.STH_AGGREGATION.value])
                else:
                    retJob.add_args(ArgsKeysEnums.STH_AGGR_METHOD.value,"lastN=100")

                retJob.add_args(ArgsKeysEnums.CORRELATION_TARGET_COLLUMNS.value,aux_datas_to_retrieve)

                retJob.add_args(ArgsKeysEnums.LINEAR_REG_ANALYSE_COLLUMNS.value,aux_datas_to_retrieve[:-1])
                retJob.add_args(ArgsKeysEnums.LINEAR_REG_TARGET_COLLUMNS.value,aux_datas_to_retrieve[len(aux_datas_to_retrieve)-1])

                #include actions
                sth_action = ActionModel()
                sth_action.set_target(TargetEnum.TARGET_STH_COMET)
                sth_action.set_action(ActionEnum.GET_STH_COMET_DATA)

                action_lin_reg = ActionModel()
                action_lin_reg.set_target(TargetEnum.TARGET_LINEAR_REG_MODULE)
                action_lin_reg.set_action(ActionEnum.EXECUTE_LINEAR_REGRESSION)

                retJob.add_action(sth_action)
                retJob.add_action(action_lin_reg)



            elif(action == ApiActionsEnum.TWO_DIMENSIONAL_GRAPHIC):
                
                #entity id
                retJob.add_args(ArgsKeysEnums.FIWARE_ENTITY.value,request_dict[ApiRequestFieldsEnum.ENTITY.value])

                #entity type
                retJob.add_args(ArgsKeysEnums.FIWARE_ENTITY_TYPE.value,request_dict[ApiRequestFieldsEnum.ENTITY_TYPE.value])
                #data to collect
                aux_datas_to_retrieve = []
                for data in request_dict[ApiRequestFieldsEnum.DATA_COLLUMNS.value]:
                    aux_datas_to_retrieve.append(data)

                retJob.add_args(ArgsKeysEnums.FIWARE_ATTRS.value,aux_datas_to_retrieve)

                if ApiRequestFieldsEnum.STH_AGGREGATION.value in request_dict:
                    #aggregration mode
                    retJob.add_args(ArgsKeysEnums.STH_AGGR_METHOD.value,request_dict[ApiRequestFieldsEnum.STH_AGGREGATION.value])
                else:
                    retJob.add_args(ArgsKeysEnums.STH_AGGR_METHOD.value,"lastN=100")

                #2d graphic collumns
                retJob.add_args(ArgsKeysEnums.TWO_DIM_GRAPHIC_TARGET_COLLUMNS.value,aux_datas_to_retrieve)


                #include actions
                sth_action = ActionModel()
                sth_action.set_target(TargetEnum.TARGET_STH_COMET)
                sth_action.set_action(ActionEnum.GET_STH_COMET_DATA)

                two_dim_action_reg = ActionModel()
                two_dim_action_reg.set_target(TargetEnum.TARGET_2D_GRAPHIC_MODULE)
                two_dim_action_reg.set_action(ActionEnum.EXECUTE_BIDIMENSIONAL_ANALYSIS)

                retJob.add_action(sth_action)
                retJob.add_action(two_dim_action_reg)

            else:
                return None
        
            if(async_job == False):
                #include action to send this job back to api gateway
                api_resp_action = ActionModel()
                api_resp_action.set_target(TargetEnum.TARGET_API_GATEWAY)
                api_resp_action.set_action(ActionEnum.SEND_RESPONSE_TO_API_GATEWAY)

                retJob.add_action(api_resp_action)
            else:
                #include action to send this job back to api gateway
                api_resp_action = ActionModel()
                api_resp_action.set_target(TargetEnum.TARGET_API_GATEWAY)
                api_resp_action.set_action(ActionEnum.SEND_ASYNC_RESPONSE_TO_API_GATEWAY)

                retJob.add_action(api_resp_action)

            
            return retJob

        except Exception as e:
            print("Exception: {e}")
            return e