from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from backend.business.market import MarketFacade
from backend.business.authentication.authentication import Authentication
from backend.business.notifier.notifier import Notifier
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_cors import CORS
from backend.config import config  # Import the config object
from backend.services import InitialState

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from backend.database import db

# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')
# ---------------------------------------------------

bcrypt = Bcrypt()
jwt = JWTManager()
socketio_manager = SocketIO()
migrate = Migrate()
cors = CORS(origin='http://localhost:3000', supports_credentials=True)

@socketio_manager.on('connect')
@jwt_required()
def handle_connect(data):
    logger.info(f"Connect data: {data}")
    logger.info(f"Client {get_jwt_identity()} connected")

@socketio_manager.on('disconnect')
def handle_disconnect(id=None):
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

def create_app(mode='development'):
    app = Flask(__name__)
    app.config.from_object(config[mode])  # Load the appropriate configuration

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    cors.origins = ['http://localhost:3000']
    socketio_manager.init_app(app, cors_allowed_origins="*")

    # Ensure the test database is created
    if mode == 'testing':
        test_db_url = app.config['SQLALCHEMY_DATABASE_URI']
        engine = create_engine(test_db_url)
        if not database_exists(engine.url):
            create_database(engine.url)
            print(f"Test database created at {test_db_url}")
        else:
            print(f"Test database already exists at {test_db_url}")


    with app.app_context():
        # Ensure that the database tables are created
        db.create_all()

        if not hasattr(app, 'initialization_done'):
            app.initialization_done = True
            authentication = Authentication()
            authentication.set_jwt(jwt, bcrypt)

            notifier = Notifier()
            notifier.set_socketio_manager(socketio_manager)

            MarketFacade()
            if mode != 'testing':

                InitialState(app, db).init_system_from_file()
            # MarketFacade().default_setup()

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
