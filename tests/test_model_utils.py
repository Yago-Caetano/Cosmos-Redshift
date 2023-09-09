
import json
from enums.action_enum import ActionEnum
from enums.target_enum import TargetEnum
from enums.state_enum import StateEnum
from models.action_model import ActionModel
from models.job_model import JobModel
from utils.job_utils import JobUtils

def test_json_to_job_model():
    json_raw = '{"JOB_ID": "123", "ARGS": { "teste_field": "test_value" }, "ACTIONS": [{"TARGET": "STH_COMET", "IN_ARGS": "", "STATE": 0, "ACTION": "GET_STH_COMET_DATA"}, {"TARGET": "CORRELATION_MODULE", "IN_ARGS": "", "STATE": 1, "ACTION": "EXECUTE_CORRELATION_ANALYSIS"}]}'

    job = JobUtils().convert_json_to_job(json_raw)
    json_dict = json.loads(json_raw)

    #check conversion
    assert(job != None)

    #check id
    assert(job.get_id() == json_dict['JOB_ID'])

    #check in args
    #assert(job.get_args() == json_dict['ARGS'])

    #check actions
    for i in range(0,1,len(json_dict['ACTIONS'])):
        aux_action = job.get_actions()[i]

        assert(json_dict['ACTIONS'][i]['STATE'] == aux_action.get_state())
        assert(json_dict['ACTIONS'][i]['TARGET'] == aux_action.get_target())



    
def test_convert_job_to_json():
    json_str_target = '{"JOB_ID": "123", "ARGS": {"teste_field": "test_value"}, "ACTIONS": [{"TARGET": "STH_COMET", "STATE": 0, "ACTION": "GET_STH_COMET_DATA"}, {"TARGET": "CORRELATION_MODULE", "STATE": 1, "ACTION": "EXECUTE_CORRELATION_ANALYSIS"}]}'

    job = JobModel("123")

    job.add_args("teste_field","test_value")

    first_action = ActionModel()
    first_action.set_action(ActionEnum.GET_STH_COMET_DATA)
    first_action.set_target(TargetEnum.TARGET_STH_COMET)
    first_action.set_state(StateEnum.NOT_INITIALIZED)
    
    second_action = ActionModel()
    second_action.set_action(ActionEnum.EXECUTE_CORRELATION_ANALYSIS)
    second_action.set_target(TargetEnum.TARGET_CORRELATION_MODULE)
    second_action.set_state(StateEnum.PENDING)

    job.add_action(first_action)
    job.add_action(second_action)


    retJson = JobUtils().convert_job_to_json(job)

    print(retJson)
    
    assert(retJson != None)

    assert(json_str_target == retJson)