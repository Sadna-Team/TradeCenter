from flask import Flask

# from service_layer.routes import api_routes  # Import API routes from service_layer
from backend import create_app, socketio_manager
import logging
import os

logger = logging.getLogger('myapp')

config_mode = os.getenv('FLASK_CONFIG', 'default')

if __name__ == "__main__":
    app = create_app(config_mode)
    app.logger.info("Starting app...")
    socketio_manager.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True, use_reloader=False)
