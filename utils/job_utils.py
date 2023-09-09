

import json
from enums.job_fields_enum import JobFieldsEnum
from enums.action_fields_enum import ActionFieldsEnum
from enums.state_enum import StateEnum
from enums.action_enum import ActionEnum
from enums.target_enum import TargetEnum
from models.action_model import ActionModel
from models.job_model import JobModel


class JobUtils():

    def __init__(self) -> None:
        pass


    def __check_string_belongs_to_enum(self,string,enum):
        for status in enum:
            if status.value == string:
                return status
        return None
    
    def convert_job_to_json(self,job:JobModel):
        try:
            ret_dict = {}
            ret_dict[JobFieldsEnum.JOB_ID.value] = job.get_id()

            #args
            aux_args = {}
            if(job.get_args() != None):
                for key,value in job.get_args().items():
                    aux_args[key] = value

                ret_dict[JobFieldsEnum.JOB_ARGS.value] = aux_args
            
            #actions
            ret_actions = []

            for action in job.get_actions():
                action_dict = {}

                action_dict[ActionFieldsEnum.TARGET.value] = action.get_target().value
                action_dict[ActionFieldsEnum.STATE.value] = action.get_state().value
                action_dict[ActionFieldsEnum.ACTION.value] = action.get_action().value

                ret_actions.append(action_dict)

            ret_dict[JobFieldsEnum.ACTIONS.value] = ret_actions

            return json.dumps(ret_dict)
        
        except Exception as e:
            print(e)
            return None
    
    def convert_json_to_job(self,json_data) -> JobModel:
        try:
            # Parse JSON
            data = json.loads(json_data)

            # Get fields
            job_id = data.get(JobFieldsEnum.JOB_ID.value, None)
            job_args = data.get(JobFieldsEnum.JOB_ARGS.value, None)
            actions = data.get(JobFieldsEnum.ACTIONS.value, [])

            ret_job = JobModel(job_id)

            if(job_args != None):
                for key,value in job_args.items():
                    ret_job.add_args(key,value)
            
            for action in actions:
                #convert each node in ActionModel
                model = ActionModel()
                action_field =  self.__check_string_belongs_to_enum(action[ActionFieldsEnum.ACTION.value],ActionEnum)

                if(action_field == None):
                    break
                model.set_action(action_field)

                target_field = self.__check_string_belongs_to_enum(action[ActionFieldsEnum.TARGET.value],TargetEnum)
                if(target_field == None):
                    break

                model.set_target(target_field)

                model.set_state(StateEnum(action[ActionFieldsEnum.STATE.value]))

                ret_job.add_action(model)

            return ret_job

        except Exception as e:
            print(f"convert_json_to_job Exception!!: {e}")
            return None

        pass
