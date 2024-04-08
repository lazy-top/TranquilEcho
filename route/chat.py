from flask import Blueprint,render_template
from flask_jwt_extended import jwt_required
from flask_socketio import emit,SocketIO

sio=SocketIO()
chatbp=Blueprint('chat',__name__,url_prefix='/chat')
@chatbp.route('/ui')
@jwt_required()
def ui():
    return render_template('chat.html')
@sio.on('send_message')
def handle_new_message(data):
    message = data['message']
    user = data['user']  # 如果有用户身份验证，此处应使用实际登录用户的标识

    # 可以在此处添加消息存储、过滤或其他业务逻辑

    # 广播消息到所有连接的客户端
    emit('new_message', {'user': user, 'message': message}, broadcast=True)