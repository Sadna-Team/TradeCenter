# backend/app.py
from backend.app_factory import create_app_instance
from backend.app_factory import create_logger_instance
from backend import socketio_manager
from backend import create_app



app = create_app_instance()
logger = create_logger_instance()

if __name__ == "__main__":
    # app = create_app('')
    app.logger.info("Starting app...")
    socketio_manager.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True, use_reloader=False)