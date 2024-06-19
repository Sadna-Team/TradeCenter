from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import secrets
from backend.business.market import MarketFacade
from backend.business.authentication.authentication import Authentication
from backend.business.notifier.notifier import Notifier
from flask_socketio import SocketIO, join_room, leave_room, send
from backend.business.DTOs import NotificationDTO
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt


# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')
# ---------------------------------------------------

bcrypt = Bcrypt()
jwt = JWTManager()
socketio_manager = SocketIO()


# @socketio.on('connect')
def handle_connect(id):
    logger.info(f"Client {id} connected")

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

@socketio_manager.on('leave')
def handle_leave(data):
    room = data['room']
    logger.info(f'Client leaving room {room}')
    leave_room(room)
    handle_disconnect(room)


class Config:
    SECRET_KEY = secrets.token_urlsafe(32)  # Generate a random secret key
    JWT_SECRET_KEY = SECRET_KEY  # Use the same key for JWT if preferred
    JWT_TOKEN_LOCATION = ['headers']




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio_manager.init_app(app)

    authentication = Authentication()
    authentication.set_jwt(jwt, bcrypt)

    notifier = Notifier()
    notifier.set_socketio_manager(socketio_manager)

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
