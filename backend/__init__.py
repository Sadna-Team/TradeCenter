from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import secrets
# from flask_sqlalchemy import SQLAlchemy
import os


class Config:
    SECRET_KEY = secrets.token_hex(32)


# db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    #    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from services.user_services.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
