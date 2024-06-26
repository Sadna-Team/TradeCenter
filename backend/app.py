from flask import Flask

# from service_layer.routes import api_routes  # Import API routes from service_layer
from backend import create_app, socketio_manager
import logging

logger = logging.getLogger('myapp')

app = create_app()

# Register API routes from service_layer
#app.register_blueprint(api_routes)

if __name__ == "__main__":
    app.logger.info("Starting app...")
    socketio_manager.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

