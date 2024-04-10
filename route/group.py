from flask import Blueprint,render_template,render_template_string
from flask_jwt_extended import jwt_required
from flask_socketio import emit, join_room, leave_room
from utils import db,CustomResponse,siwa,socketio
groupbp=Blueprint('group',__name__,url_prefix='/group')
@groupbp.route('/ui')
# @jwt_required()
@siwa.doc(tags=['聊天社区'])
def ui():
    """
    显示聊天界面
    ---
    tags:
        - 聊天社区
    description: 显示聊天界面

    """
    return render_template('group.html')

# 用户连接事件
@socketio.event
@siwa.doc(tags=['聊天社区'])
def connect():
    print(f"User connected")

# 用户断开连接事件
@socketio.event
@siwa.doc(tags=['聊天社区'])
def disconnect():
    print(f"User disconnected")

# 接收并处理客户端发送的消息
@socketio.on('chat_message')
@siwa.doc(tags=['聊天社区'])
def handle_chat_message(data):
    print(f"Received message: {data}")
    message = data['message']
    username = data['username']
    room = data['room']

    # 广播消息到指定房间
    emit('chat_message', {'username': username, 'message': message}, room=room)

# 用户加入房间
@socketio.on('join')
@siwa.doc(tags=['聊天社区'])
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('user_entered', {'username': username}, room=room)

# 用户离开房间
@socketio.event
@siwa.doc(tags=['聊天社区'])
def leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('user_left', {'username': username}, room=room)