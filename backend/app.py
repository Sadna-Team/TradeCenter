from flask import Flask
# from service_layer.routes import api_routes  # Import API routes from service_layer
from __init__ import create_app
from logging_config import setup_logging

setup_logging()

app = create_app()
# Register API routes from service_layer
#app.register_blueprint(api_routes)

if __name__ == "__main__":
    app.run(debug=True)
    