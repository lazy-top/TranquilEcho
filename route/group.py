from enum import Enum
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import emit, join_room, leave_room, SocketIO
from utils import siwa

groupbp = Blueprint('group', __name__, url_prefix='/group')
socketio = SocketIO()  # Assuming socketio instance is initialized somewhere else

class Message_type(Enum):
    TEXT = 1
    IMAGE = 2
    VIDEO = 3
    AUDIO = 4
    FILE = 5
    WARNING = 6
    NOTICE = 7

room_names = [
    "心灵港湾",
    "抑郁症支持小组",
    "焦虑自助论坛",
    "情绪管理交流室",
    "压力释放空间",
    "自尊心建设营",
    "积极心态工作坊",
    "心理健康启航",
    "情感调适中心",
    "幸福生活讨论区"
]

userList = []

# 强化了异常处理和安全性
@socketio.event
@siwa.doc(tags=['聊天社区'])
@jwt_required()
def connect():
    user_identity = get_jwt_identity()
    if user_identity:
        # 添加用户到列表中
        userList.append(socketio.get_current_user())
        emit('room_list', {'rooms': room_names})
    else:
        # 若认证失败，断开连接
        disconnect()
    print(f"User connected")

@socketio.event
@siwa.doc(tags=['聊天社区'])
def disconnect():
    try:
        userList.remove(socketio.get_current_user())
    except ValueError:
        pass  # 用户不在列表中，无需处理
    print(f"User disconnected")

# 增加了对消息类型的检查
@socketio.on('chat_message')
@siwa.doc(tags=['聊天社区'])
def handle_chat_message(data):
    time = data.get('time')
    if not time:
        return 'Invalid message format'  # 检查消息格式
    message_type = data.get('message_type')
    message = data.get('message')
    username = data.get('username')
    room = data.get('room')
    if room not in room_names:
        disconnect()
        return 'Invalid room'
    if message_type is None or message is None or username is None:
        return 'Invalid message format'
    if message_type not in [mt.value for mt in Message_type]:
        return 'Invalid message type'  # 检查消息类型
    # 广播消息到指定房间
    emit('chat_message', {'message_type': message_type, 'time': time, 'username': username, 'message': message}, room=room)
    print(f"Received message: {data}")

@socketio.on('join')
@siwa.doc(tags=['聊天社区'])
def on_join(data):
    username = data.get('username')
    room = data.get('room')
    if room not in room_names:
        disconnect()
        return 'Invalid room'
    join_room(room)
    emit('user_entered', {'username': username}, room=room)

@socketio.event
@siwa.doc(tags=['聊天社区'])
def leave(data):
    username = data.get('username')
    room = data.get('room')
    leave_room(room)
    emit('user_left', {'username': username}, room=room)