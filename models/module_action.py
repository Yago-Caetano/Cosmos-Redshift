from enums.action_enum import ActionEnum
from action_handler import ActionHandler


class ModelAction():
    def __init__(self):
        self.__action = None
        self.__handler = None

    def register_action_with_handler(self,action:ActionEnum,handler:ActionHandler):
        self.__action = action
        self.__handler = handler

    def get_action(self)->ActionEnum:
        return self.__action

    def get_handler(self)->ActionHandler:
        return self.__handler
