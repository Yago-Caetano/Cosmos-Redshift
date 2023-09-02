from enum import Enum

class QueuesEnum(Enum):
    MAIN_QUEUE = "main_queue"
    CORRELATION_QUEUE = "correlation_queue"
    LINEAR_REGRESSION_QUEUE = "linear_reg_queue"
    STH_COMET_QUEUE = "sth_comet_queue"