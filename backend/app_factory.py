from flask import Flask
from backend import create_app
import os
import logging

config_mode = os.getenv('FLASK_CONFIG', 'default')


class AppFactory:
    __instance = None

    def __new__(cls):
        if AppFactory.__instance is None:
            AppFactory.__instance = super(AppFactory, cls).__new__(cls)
            AppFactory.__instance.__initialized = False
        return AppFactory.__instance

    def __init__(self):
        if self.__initialized:
            return
        self.app = None
        self.logger = None
        self.__initialized = True

    def init_app(self, mode='development'):
        if self.app is None:
            self.app = create_app(mode)
            self.logger = logging.getLogger('myapp')
        return self.app

    def set_app(self, app):
        self.app = app

    def get_app(self):
        if self.app is None:
            self.app = create_app('development')
            self.logger = logging.getLogger('myapp')
        return self.app


def get_app():
    return AppFactory().get_app()

def set_app(app):
    AppFactory().set_app(app)


def create_app_instance(mode='development'):
    return AppFactory().init_app(mode)


def create_logger_instance(mode='development'):
    factory = AppFactory().init_app(mode)
    return factory.logger
