import copy
from enums.state_enum import StateEnum
from models.action_model import ActionModel


class JobModel():

    def __init__(self,id):
        self.__id = id
        self.__actions = []
        self.__state = StateEnum.NOT_INITIALIZED
        self.__in_args = None
        self.__out_args = None

    def add_action(self,action:ActionModel):
        self.__actions.append(action)

    def get_actions(self):
        return self.__actions

    def change_state(self,state:StateEnum):
        self.__state = state

    def get_id(self):
        return self.__id
    
    def get_in_args(self):
        return self.__in_args
    
    def set_in_args(self,data):
        self.__in_args = copy.deepcopy(data)
    
    def set_out_args(self,data):
        self.__out_args = copy.deepcopy(data)

    def get_out_args(self):
        return self.__out_args