from flask import jsonify, request
from flask import Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required
from utils import db
from model import User
bp=Blueprint('user',__name__,url_prefix='/user')
@bp.route('/me')
@jwt_required()
def user():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



    
@bp.route('/login', methods=['POST'])
def login():
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return jsonify({"msg": "Invalid username or password"}), 401
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
@bp.route('/register', methods=['POST'])
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
        return jsonify({"msg": "Missing username or password"}), 400
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"msg": "Username already exists"}), 400
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered"}), 201
@bp.route('/audio_chat')
def audio_chat():
    return jsonify({"msg": "audio_chat"}), 200