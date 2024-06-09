from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import secrets
from backend.business.market import MarketFacade
from backend.business.authentication.authentication import Authentication



class Config:
    SECRET_KEY = secrets.token_urlsafe(32)  # Generate a random secret key
    JWT_SECRET_KEY = SECRET_KEY  # Use the same key for JWT if preferred
    JWT_TOKEN_LOCATION = ['headers']


bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    jwt.init_app(app)

    authentication = Authentication()
    authentication.set_jwt(jwt, bcrypt)

    MarketFacade()

    from backend.services.user_services.routes import auth_bp, user_bp
    from backend.services.ecommerce_services.routes import market_bp
    from backend.services.store_services.routes import store_bp
    from backend.services.third_party_services.routes import third_party_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(market_bp, url_prefix='/market')
    app.register_blueprint(store_bp, url_prefix='/store')
    app.register_blueprint(third_party_bp, url_prefix='/third_party')



    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        return authentication.check_if_token_in_blacklist(jwt_header, jwt_payload)
    return app


def clean_data():
    MarketFacade().clean_data()
    Authentication().clean_data()
