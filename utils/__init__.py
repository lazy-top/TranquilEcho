# -*- coding: utf-8 -*-#
# 验证手机号格式
import re
from flask import Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
#配置文件

socketio = SocketIO()
db = SQLAlchemy()
jwt = JWTManager()

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
    
class StandardResponse():
    def __init__(self, status_code, data=None, message=None, headers=None, **kwargs):
        """
        初始化标准化的JSON响应对象。

        Args:
            status_code (int): HTTP状态码。
            data (dict, optional): 要返回的数据，以字典形式表示。默认为None。
            message (str, optional): 提供给客户端的描述性消息。默认为None。
            headers (dict, optional): 额外的HTTP响应头。默认为None。
            kwargs: 其他传递给父类`Response`的构造方法的参数。
        """
        response_data = {"status": status_code}
        
        if data is not None:
            response_data["data"] = data
        if message is not None:
            response_data["message"] = message

        super().__init__(jsonify(response_data), status=status_code, headers=headers, **kwargs)

    
