from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import secrets
from backend.business.market import MarketFacade
from backend.business.authentication.authentication import Authentication
from backend.business.notifier.notifier import Notifier
from backend.business.DTOs import NotificationDTO
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_cors import CORS
import threading
# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')
# ---------------------------------------------------

bcrypt = Bcrypt()
jwt = JWTManager()
socketio_manager = SocketIO()
cors = CORS(origin='http://localhost:3000', supports_credentials=True)

@socketio_manager.on('connect')
@jwt_required()
def handle_connect(data):
    logger.info(f"Connect data: {data}")
    logger.info(f"Client {get_jwt_identity()} connected")


# @socketio.on('disconnect')
def handle_disconnect(id):
    logger.info(f"Client {id} disconnected")



@socketio_manager.on('join')
@jwt_required()
def handle_join():
    room = get_jwt_identity()
    handle_connect(room)
    logger.info(f'Client joining room {room}')
    join_room(room=room)

    # Send a message to the client
    emit('connected', {'data': 'Connected to the server'}, room=room)








@socketio_manager.on('leave')
@jwt_required()
def handle_leave():
    room = get_jwt_identity()
    logger.info(f'Client leaving room {room}')
    leave_room(room)
    handle_disconnect(room)


class Config:
    SECRET_KEY = secrets.token_urlsafe(32)  # Generate a random secret key
    JWT_SECRET_KEY = SECRET_KEY  # Use the same key for JWT if preferred
    JWT_TOKEN_LOCATION = ['headers']


def create_app(mode='development'):
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    cors.origins = ['http://localhost:3000']
    socketio_manager.init_app(app, cors_allowed_origins="*")
    authentication = Authentication()
    authentication.set_jwt(jwt, bcrypt)

    notifier = Notifier()
    notifier.set_socketio_manager(socketio_manager)

    MarketFacade()

    if mode == 'development':
        # initialize default market data(for tests)
        default_setup = input("Do you want to setup default data? (y/n): ")
        default_setup = default_setup.lower()
        default_setup = True if default_setup == 'y' else False
        if default_setup:
            MarketFacade().default_setup()

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
