import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = secrets.token_urlsafe(32)
    JWT_SECRET_KEY = SECRET_KEY
    JWT_TOKEN_LOCATION = ['headers']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'postgresql://user:password@localhost:5432/mydatabase')

class DockerDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DOCKER_DEV_DATABASE_URL', 'postgresql://user:password@db:5432/mydatabase')

class TestingConfig(Config):
    TESTING = True
    if os.getenv('DOCKER_ENV') == 'true':
        SQLALCHEMY_DATABASE_URI = os.getenv('DOCKER_TEST_DATABASE_URL', 'postgresql://user:password@db:5432/test_database')
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'postgresql://user:password@localhost:5432/test_database')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/prod_database')

config = {
    'development': DevelopmentConfig,
    'docker_development': DockerDevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
