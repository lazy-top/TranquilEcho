# -*- coding: utf-8 -*-#
# 验证手机号格式
import re
from flask import Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_siwadoc import SiwaDoc
from flask_cors import CORS
from langchain.prompts import PromptTemplate
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
class User_message(BaseModel):
    message:str
socketio = SocketIO()
db = SQLAlchemy()
jwt = JWTManager()
siwa=SiwaDoc()
cors=CORS()
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

choise_propmpt=PromptTemplate.from_template("""
                                        请仔细阅读以下用户输入，并根据输入内容选择最合适的功能模块选项。您的目标是理解用户的需求，并根据这些需求从可用的功能模块中选择最佳的选项。

用户输入:
{input}

根据上述指导，大语言模型应该能够分析用户输入并生成如下功能模块选项:

功能模块选项:
1. 功能模块A: 描述功能模块A如何满足用户需求。
2. 功能模块B: 描述功能模块B如何满足用户需求。
3. 功能模块C: 描述功能模块C如何满足用户需求。

请确保您的指导语句足够详细，以便大语言模型能够理解您的需求，并根据用户输入选择最合适的功能模块选项。如果您提供了具体的用户输入内容，我可以帮助您生成相应的功能模块选项。
                                        """)
assistant_prompt=PromptTemplate.from_template("""
                                        你是一个专业的{role}，请根据用户输入，生成一个最合适的回答。
                                        
                                        用户输入:
                                        {input}
                                        
                                        你的回答:
                                        """)

arg_prompt=PromptTemplate.from_template("""
                                        你是一个专业的{role}，请根据用户输入，生成一个最合适的回答。
                                        
                                        用户输入:
                                        {input}
                                        
                                        你的回答:
                                        """)


warning_prompt=PromptTemplate.from_template("""
                                            
                                            
                                            
                                            """)
