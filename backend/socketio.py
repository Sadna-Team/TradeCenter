# from flask_socketio import SocketIO, join_room, leave_room, send
# from .app import socketio
# from backend.business.DTOs import NotificationDTO
# from flask import jsonify

# # -------------logging configuration----------------
# import logging

# logger = logging.getLogger('myapp')
# # ---------------------------------------------------

# # @socketio.on('connect')
# def handle_connect(id):
#     logger.info(f"Client {id} connected")

# # @socketio.on('disconnect')
# def handle_disconnect(id):
#     logger.info(f"Client {id} disconnected")

# @socketio.on('join')
# def handle_join(data):
#     room = data['room']
#     handle_connect(room)
#     logger.info(f'Client joining room {room}')
#     join_room(room)

# @socketio.on('leave')
# def handle_leave(data):
#     room = data['room']
#     logger.info(f'Client leaving room {room}')
#     leave_room(room)
#     handle_disconnect(room)

# def send_real_time_notification(user_id, notification: NotificationDTO):
#     message = jsonify({'message': notification.to_json()})
#     socketio.send(message, json=True, to=user_id, include_self=False)
#     logger.info(f"sent message to user {user_id}")