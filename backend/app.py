from flask import Flask
from flask_socketio import SocketIO
# from service_layer.routes import api_routes  # Import API routes from service_layer
from __init__ import create_app
import logging

logger = logging.getLogger('myapp')

app = create_app()
socketio = SocketIO(app)

# Register API routes from service_layer
#app.register_blueprint(api_routes)

if __name__ == "__main__":
    app.logger.info("Starting app...")
    app.run(debug=True)