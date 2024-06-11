# from flask_socketio import SocketIO, join_room, leave_room, send
# from app import socketio
# from backend.business.DTOs import NotificationDTO
# from flask import jsonify

# # -------------logging configuration----------------
# import logging

# logger = logging.getLogger('myapp')
# # ---------------------------------------------------

# # @socketio.on('connect')
# def handle_connect():
#     logger.info('Client connected')

# # @socketio.on('disconnect')
# def handle_disconnect():
#     logger.info('Client disconnected')

# @socketio.on('join')
# def handle_join(data):
#     handle_connect()
#     room = data['room']
#     logger.info(f'Client joining room {room}')
#     join_room(room)

# @socketio.on('leave')
# def handle_leave(data):
#     room = data['room']
#     logger.info(f'Client leaving room {room}')
#     leave_room(room)
#     handle_disconnect()

# def send_real_time_notification(user_id, notification: NotificationDTO):
#     message = jsonify({'message': notification.to_json()})
#     send(message, json=True, to=user_id, include_self=False)
#     logger.info(f"sent message to user {user_id}")