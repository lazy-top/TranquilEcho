from flask import Response, jsonify, request,render_template,Blueprint, stream_with_context
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required
# from services import process_user_input
from utils import db,StandardResponse
from model import User
userbp=Blueprint('user',__name__,url_prefix='/user')



@userbp.route('/me')
@jwt_required()
def user():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



    
@userbp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return StandardResponse(
            status_code=401, message='Invalid username or password'
        )
    access_token = create_access_token(identity=username)
    return StandardResponse(
        status_code=200,
        data={'access_token': access_token},
        message='Login successful'
)
@userbp.route('/register', methods=['POST'])
def register():
    """
    用户注册
    ---
    tags:
        - 用户相关接口
    description:

    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username is None or password is None:
        return StandardResponse(
            status_code=400, message='Missing username or password'
        )
    if User.query.filter_by(username=username).first() is not None:
        return StandardResponse(
            status_code=400, message='Username already exists'
        )
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return StandardResponse(
        status_code=201, 
        message='User created')
@userbp.route('/audio_chat')
@jwt_required()
def audio_chat():
    return render_template('audio_chat.html')

# @userbp.route('/text_chat',methods=['POST'])
# @jwt_required()
# def text_chat():
#     text = request.json.get('text', None)
#     return Response(stream_with_context(process_user_input(text)), mimetype="text/event-stream")
