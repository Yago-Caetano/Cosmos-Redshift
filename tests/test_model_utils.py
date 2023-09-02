
import json
from utils.job_utils import JobUtils

def test_json_to_job_model():
    json_raw = '{"JOB_ID": "123", "JOB_IN_ARGS": "input_data", "JOB_OUT_ARGS": "output_data", "ACTIONS": [{"TARGET": "STH_COMET", "IN_ARGS": "", "STATE": 0, "ACTION": "GET_STH_COMET_DATA"}, {"TARGET": "CORRELATION_MODULE", "IN_ARGS": "", "STATE": 1, "ACTION": "EXECUTE_CORRELATION_ANALYSIS"}]}'

    job = JobUtils().convert_json_to_job(json_raw)
    json_dict = json.loads(json_raw)

    #check conversion
    assert(job != None)

    #check id
    assert(job.get_id() == json_dict['JOB_ID'])

    #check in args
    assert(job.get_in_args() == json_dict['JOB_IN_ARGS'])

    #check out args
    assert(job.get_out_args() == json_dict['JOB_OUT_ARGS'])

    #check actions
    for i in range(0,1,len(json_dict['ACTIONS'])):
        aux_action = job.get_actions()[i]

        assert(json_dict['ACTIONS'][i]['STATE'] == aux_action.get_state())
        assert(json_dict['ACTIONS'][i]['TARGET'] == aux_action.get_target())



    
