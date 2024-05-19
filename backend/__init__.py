from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import secrets
from backend.business.market import MarketFacade


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

    market_facade = MarketFacade()

    from services.user_services.routes import auth_bp, user_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')

    return app
