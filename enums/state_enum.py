from enum import Enum, IntEnum

class StateEnum(IntEnum):
    NOT_INITIALIZED = 0
    PENDING = 1
    EXECUTING = 2
    WAITING_RESPONSE=3
    DONE = 4
    FAILED = 5