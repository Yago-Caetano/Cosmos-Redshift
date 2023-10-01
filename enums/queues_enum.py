from enum import Enum

class QueuesEnum(Enum):
    MAIN_QUEUE = "main_queue"
    CORRELATION_QUEUE = "correlation_queue"
    LINEAR_REGRESSION_QUEUE = "linear_reg_queue"
    STH_COMET_QUEUE = "sth_comet_queue"
    API_GATEWAY_RESPONSE_QUEUE = "api_gateway_resp_queue"
    TWO_DIMENSIONAL_GRAPH = "2d_graph_queue"