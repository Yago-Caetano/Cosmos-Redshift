from enums.queues_enum import QueuesEnum
from modules.sth_comet_module import SthCometModule

def test_consume_sth_data():
    sth_module = SthCometModule()
    sth_module.set_rabbit_mq_queue(QueuesEnum.STH_COMET_QUEUE.value)

    sth_data = sth_module.consume_sth("urn:ngsi-ld:entity:986463ec-3f51-11ee-be56-0242ac120002","eggProduction","cracked_eggs","lastN=10", "smart","/")
    assert(sth_data != None)

    #http://{{url}}:8666/STH/v1/contextEntities/type/eggProduction/id/urn:ngsi-ld:entity:986463ec-3f51-11ee-be56-0242ac120002/attributes/cracked_eggs?lastN=10