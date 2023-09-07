

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
                return True
        return False
    
    def convert_json_to_job(self,json_data) -> JobModel:
        try:
            # Parse JSON
            data = json.loads(json_data)

            # Get fields
            job_id = data.get(JobFieldsEnum.JOB_ID.value, None)
            job_args = data.get(JobFieldsEnum.JOB_ARGS.value, None)
            actions = data.get(JobFieldsEnum.ACTIONS.value, [])

            ret_job = JobModel(job_id)
            ret_job.add_args("args",job_args)
            
            for action in actions:
                #convert each node in ActionModel
                model = ActionModel()
                if(False == self.__check_string_belongs_to_enum(action[ActionFieldsEnum.ACTION.value],ActionEnum)):
                    break
                model.set_action(action[ActionFieldsEnum.ACTION.value])

                if(False == self.__check_string_belongs_to_enum(action[ActionFieldsEnum.TARGET.value],TargetEnum)):
                    break

                model.set_target(action[ActionFieldsEnum.TARGET.value])

                model.set_state(StateEnum(action[ActionFieldsEnum.STATE.value]))

                ret_job.add_action(model)

            return ret_job

        except Exception as e:
            print(f"convert_json_to_job Exception!!: {e}")
            return None

        pass
