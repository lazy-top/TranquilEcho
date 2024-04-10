from flask import jsonify, request,Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required
from utils import db,CustomResponse,siwa
from model import User
userbp=Blueprint('user',__name__,url_prefix='/user')
# 需要JWT认证的当前用户信息
@userbp.route('/me')
@jwt_required()
@siwa.doc(tags=['用户'])
def user():
    """
    获取当前登录用户的个人信息
    ---
    tags:
        - 用户相关接口
    description: 使用用户token来获取个人信息
    """
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# 用户登录接口
@userbp.route('/login', methods=['POST'])
@siwa.doc(tags=['用户'])
def login():
    """
    用户登录，返回访问token
    ---
    tags:
        - 用户相关接口
    description: 用户提交用户名和密码进行登录，返回访问token
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return CustomResponse(
            status_code=401, message='Invalid username or password'
        ).to_response()
    access_token = create_access_token(identity=username)
    return CustomResponse(
        status_code=200,
        data={'access_token': access_token},
        message='Login successful'
    ).to_response()

# 用户注册接口
@userbp.route('/register', methods=['POST'])
@siwa.doc(tags=['用户'])
def register():
    """
    注册新用户
    ---
    tags:
        - 用户相关接口
    description: 提交用户名和密码进行注册
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username is None or password is None:
        return CustomResponse(
            status_code=400, message='Missing username or password'
        ).to_response()
    if User.query.filter_by(username=username).first() is not None:
        return CustomResponse(
            status_code=400, message='Username already exists'
        ).to_response()
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return CustomResponse(
        status_code=201, 
        message='User created'
    ).to_response()

#更换密码
@userbp.route('/change_password', methods=['POST'])
@jwt_required()
@siwa.doc(tags=['用户'])
def change_password():
    """
    更换密码
    ---
    tags:
        - 用户相关接口
    description: 提交旧密码和新密码来更换用户密码
    """
    username=get_jwt_identity()
    old_password = request.json.get('old_password', None)
    new_password = request.json.get('new_password', None)
    if(old_password is None or new_password is None):
        return CustomResponse(
            status_code=400, message='Missing old_password or new_password'
        ).to_response()
    if(new_password==old_password):
        return CustomResponse(
            status_code=400, message='new_password is same as old_password'
        ).to_response()
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(old_password):
        return CustomResponse(
            status_code=401, message='Invalid username or password')
    user.set_password(new_password)
    db.session.commit()
    db.session.close()
    
            