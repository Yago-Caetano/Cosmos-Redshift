from enums.state_enum import StateEnum
from models.action_model import ActionModel


class JobModel():

    def __init__(self):
        self.__actions = []
        self.__state = StateEnum.NOT_INITIALIZED

    def add_action(self,action:ActionModel):
        self.__actions.append(action)

    def change_state(self,state:StateEnum):
        self.__state = state