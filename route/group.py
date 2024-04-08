from flask import Blueprint,render_template
from flask_socketio import emit, join_room, leave_room
from utils import socketio
groupbp=Blueprint('group',__name__,url_prefix='/group')
@groupbp.route('/ui')
def ui():
    return render_template('group.html')

# 用户连接事件
@socketio.event
def connect():
    print(f"User connected")

# 用户断开连接事件
@socketio.event
def disconnect():
    print(f"User disconnected")

# 接收并处理客户端发送的消息
@socketio.on('chat_message')
def handle_chat_message(data):
    message = data['message']
    username = data['username']
    room = data['room']

    # 广播消息到指定房间
    emit('chat_message', {'username': username, 'message': message}, room=room)

# 用户加入房间
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('user_entered', {'username': username}, room=room)

# 用户离开房间
@socketio.event
def leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('user_left', {'username': username}, room=room)