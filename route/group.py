from enum import Enum
from flask import Blueprint ,render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import emit, join_room, leave_room, SocketIO
from utils import siwa

# 匿名聊天社区
# 功能介绍：    用户可以匿名进入聊天室，与其他用户进行匿名聊天。
# 第一步，选择10个固有的房间，进入放入房间前，弹出输入框选择匿名的名称
# 第二步，选择房间，进入房间后，可以自由交流，可以发图片，文本，表情。
groupbp = Blueprint('group', __name__, url_prefix='/group')
@groupbp.route('/ui', methods=['GET'])
def ui():
    return render_template('group.html')

socketio = SocketIO()  # Assuming socketio instance is initialized somewhere else

class Message_type(Enum):
    TEXT = 1
    IMAGE = 2
    EMOTION = 3


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
# 用于统计在线人数
userList = []

# 定义一个用户类
class User:
    def __init__(self, username, room):
        self.username = username
        self.room = room

    def __str__(self):
        return self.username


# 定义一个消息类
class Message:
    def __init__(self, sender, content, message_type):
        self.sender = sender
        self.content = content
        self.message_type = message_type

    def __str__(self):
        return f"{self.sender}: {self.content}"


# 定义一个聊天室类
class Room:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.messages = []

    def add_user(self, user):
        self.users.append(user)

    def remove_user(self, user):
        self.users.remove(user)

    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages


# 初始化聊天室
rooms = [Room(name) for name in room_names]
@socketio.on('connect')
def connect():
    print('connect')
    emit('room_list', {'rooms': [room.name for room in rooms]})

# 加入房间事件
@socketio.on('join_room')
def join_room_event(data):
    print('join_room_event')
    room = data['room']
    username = data['username']
    user = User(username, room)
    join_room(room)
    rooms[room].add_user(user)
    userList.append(user)
    emit('join_room_response', {'room': room, 'users': [str(u) for u in rooms[room].users]}, room=room)


# 离开房间事件
@socketio.on('leave_room')
def leave_room_event(data):
    print('leave_room_event')
    room = data['room']
    username = data['username']
    user = User(username, room)
    leave_room(room)
    rooms[room].remove_user(user)
    userList.remove(user)
    emit('leave_room_response', {'room': room, 'users': [str(u) for u in rooms[room].users]}, room=room)


# 发送消息事件
@socketio.on('send_message')
def send_message_event(data):
    print('send_message_event')
    room = data['room']
    sender = data['sender']
    content = data['content']
    message_type = data['message_type']
    message = Message(sender, content, message_type)
    rooms[room].add_message(message)
    emit('receive_message', {'sender': sender, 'content': content, 'message_type': message_type}, room=room)


# 获取在线用户事件
@socketio.on('get_online_users')
def get_online_users_event(data):
    print('get_online_users_event')
    room = data['room']
    emit('online_users_response', {'users': [str(u) for u in rooms[room].users]}, room=room)


# 获取聊天记录事件
@socketio.on('get_chat_history')
def get_chat_history_event(data):
    room = data['room']
    chat_history = [str(m) for m in rooms[room].get_messages()]
    emit('chat_history_response', {'chat_history': chat_history}, room=room)


