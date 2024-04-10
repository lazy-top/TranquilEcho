# -*- coding: utf-8 -*-#
# 验证手机号格式
import re
from flask import Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_siwadoc import SiwaDoc
from pydantic import BaseModel
#配置文件
class Chat_message(BaseModel):
    message_type:str
    message:str
    time:str
    user_id:str
class Text_to_speech(BaseModel):
    text:str
class Authorization(BaseModel):
    Authorization:str
class Login(BaseModel):
    username:str
    password:str
class Register(BaseModel):
    username:str
    password:str
    repassword:str
socketio = SocketIO()
db = SQLAlchemy()
jwt = JWTManager()
siwa=SiwaDoc()
# 正则表达式匹配中国大陆的手机号码
phone_number_pattern = re.compile(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$')
# 正则表达式匹配大多数电子邮件地址
email_pattern = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
# 正则表达式匹配包含数字和字母，长度大于6小于20的密码
password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,20}$')

# 检查手机号码格式
def validate_phone_number(phone_number):    
    if phone_number_pattern.match(phone_number):        
        return True   
    else:        
        return False

def validate_email(email):    
    if email_pattern.match(email):        
        return True    
    else:        
        return False

# 验证密码格式
def validate_password(password):    
    if password_pattern.match(password):        
        return True    
    else:        
        return False
    
class CustomResponse(object):
    def __init__(self, status_code=200, message="", data=None):
        self.status_code = status_code
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            'code': self.status_code,
            'msg': self.message,
            'data': self.data or {}
        }

    def to_response(self):
        return jsonify(self.to_dict()), self.status_code

def validate_message(message):
    
    pass
