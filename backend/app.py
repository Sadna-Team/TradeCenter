# backend/app.py
from backend.app_factory import create_app_instance
from backend.app_factory import create_logger_instance
from backend import socketio_manager
import socket


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't matter if we send it or not, we just want to get the IP address
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


if __name__ == "__main__":
    print("In mainnnnnn")
    app = create_app_instance()
    logger = create_logger_instance()
    app.logger.info("Starting app...")

    ip_address = get_ip_address()
    print(f"Server is running on IP address: {ip_address}")

    # start but not on localhost, so we can access it from another machine
    # Bind to '0.0.0.0' to make the app accessible from other machines on the network
    socketio_manager.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True, use_reloader=False)