from flask import Flask
# from service_layer.routes import api_routes  # Import API routes from service_layer

app = Flask(__name__)

# Register API routes from service_layer
#app.register_blueprint(api_routes)

if __name__ == "__main__":
    app.run(debug=True)