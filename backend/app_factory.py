from flask import Flask
from backend import create_app2
import os
import logging

config_mode = os.getenv('FLASK_CONFIG', 'default')


def create_app_instance(mode='development'):
    factory = AppFactory()
    return factory.get_app(mode)

def create_logger_instance():
    factory = AppFactory()
    return factory.logger

class AppFactory:
    # singleton
    __instance = None

    def __new__(cls):
        if AppFactory.__instance is None:
            AppFactory.__instance = super(AppFactory, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.app = None
        self.logger = None
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.logger = logging.getLogger('myapp')
            self.logger.info("Creating app factory, this message should only appear once")
            print("Creating app factory, this message should only appear once")
            self.__dev_app = create_app2('development')
            self.__test_app = create_app2('testing')
            

    def get_app(self, mode):
        if mode == 'development':
            return self.__dev_app
        elif mode == 'testing':
            return self.__test_app
        else:
            return None
