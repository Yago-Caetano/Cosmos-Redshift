import copy
from enums.state_enum import StateEnum
from models.action_model import ActionModel


class JobModel():

    def __init__(self,id):
        self.__id = id
        self.__actions = []
        self.__state = StateEnum.NOT_INITIALIZED
        self.__args = {}
        self.__out_args = None

    def add_action(self,action:ActionModel):
        self.__actions.append(action)

    def get_next_pending_action(self):
        for action in self.__actions:
            if(action.get_state() != StateEnum.DONE):
                return action
        
        return None

    def get_actions(self):
        return self.__actions

    def change_state(self,state:StateEnum):
        self.__state = state

    def get_id(self):
        return self.__id
    
    def get_args(self):
        return self.__args
    
    def add_args(self,key,data):
        self.__args[key] = copy.deepcopy(data)
    
