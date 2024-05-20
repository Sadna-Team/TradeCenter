# logging configuration
import logging
from logging.config import dictConfig

def setup_logging():
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)s: %(message)s',
            },
            'detailed': {
                'format': '%(asctime)s %(levelname)s [%(module)s:%(lineno)d]: %(message)s',
            },
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'formatter': 'detailed'
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi', 'file']
        },
        'loggers': {
            'myapp': {
                'level': 'DEBUG',
                'handlers': ['wsgi', 'file'],
                'propagate': False
            }
        }
    })
