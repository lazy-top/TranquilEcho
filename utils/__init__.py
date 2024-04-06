# -*- coding: utf-8 -*-#
# 验证手机号格式
import re
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# 预编译正则表达式，提高性能
PHONE_PATTERN = re.compile(r'^\d{11}$')

def check_phone_format(phone):
    """
    检查手机号的格式是否合法。
    
    参数:
    - phone: 待检查的手机号字符串。
    
    返回:
    - True，如果手机号格式合法。
    - False，如果手机号格式不合法。
    """
    # 检查输入是否为字符串类型
    if not isinstance(phone, str):
        raise ValueError("phone must be a string")
        
    # 检查手机号是否为空
    if not phone:
        return False
    
    # 使用预编译的正则表达式进行手机号格式的检查
    return PHONE_PATTERN.match(phone) is not None


