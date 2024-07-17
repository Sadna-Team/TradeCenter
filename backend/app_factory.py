from flask import Flask
from backend import create_app
import os
import logging

config_mode = os.getenv('FLASK_CONFIG', 'default')


def create_app_instance(mode='development'):
    factory = AppFactory()
    return factory.init_app(mode)



def create_logger_instance(mode='development'):
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
            # self.app = create_app(mode)
            # self.logger = logging.getLogger('myapp')
        
    def init_app(self, mode='development'):
        self.app = create_app(mode)
        self.logger = logging.getLogger('myapp')
        return self.app
