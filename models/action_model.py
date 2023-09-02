
from enums.action_enum import ActionEnum
from enums.target_enum import TargetEnum
from enums.state_enum import StateEnum


class ActionModel():

    def __init__(self):
        self.__target = None
        self.__retryLimit = None
        self.__timeout = None
        self.__action = None
        self.__state = StateEnum.NOT_INITIALIZED

    def set_timeout(self,timeout:int):
        self.__timeout = timeout

    def get_timeout(self) -> int:
        return self.__timeout

    def set_target(self,target:TargetEnum):
        self.__target = target

    def get_target(self) -> TargetEnum:
        return self.__target

    def set_retry_limit(self,limit):
        self.__retryLimit = limit
    
    def get_retry_limit(self):
        return self.__retryLimit 

    def set_action(self,action: ActionEnum):
        self.__action = action

    def get_action(self) -> ActionEnum:
        return self.__action
    
    def set_state(self,state:StateEnum):
        self.__state = state

    def get_state(self):
        return self.__state
