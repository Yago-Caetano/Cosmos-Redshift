import time
from enums.api_request_fields_enum import ApiRequestFieldsEnum
from enums.api_actions_enum import ApiActionsEnum
from enums.argsKeysEnum import ArgsKeysEnums
from enums.action_enum import ActionEnum
from enums.target_enum import TargetEnum
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
    
    def convert_request_to_job(self,request_dict) -> JobModel:
        try:
            retJob = JobModel(str(int(time.time())))

            retJob.add_args(ArgsKeysEnums.FIWARE_SERVICE.value,"smart")
            retJob.add_args(ArgsKeysEnums.FIWARE_SERVICE_PATH.value,"/")

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

                #aggregration mode
                retJob.add_args(ArgsKeysEnums.STH_AGGR_METHOD.value,"lastN=10")

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
                pass

            else:
                return None
        

            #include action to send this job back to api gateway
            api_resp_action = ActionModel()
            api_resp_action.set_target(TargetEnum.TARGET_API_GATEWAY)
            api_resp_action.set_action(ActionEnum.SEND_RESPONSE_TO_API_GATEWAY)

            retJob.add_action(api_resp_action)
            
            return retJob

        except Exception as e:
            return None