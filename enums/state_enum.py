import enum


class StateEnum(enum):
    NOT_INITIALIZED = 0
    PENDING = 1
    EXECUTING = 2
    WAITING_RESPONSE=3