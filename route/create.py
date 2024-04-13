from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
import ollama
from utils import CustomResponse,siwa
visitorbp = Blueprint('create', __name__,url_prefix='/create')
@visitorbp.route('/assistant',methods=['POST'])
@siwa.doc(tags=['心理助手'],description='创建心理助手')
@jwt_required()
def chat():
    # 接受前端传递的文本数据，并进行验证
    user_message=request.json.get('message')
    
    
    pass
    
def create_prompt():
  response = ollama.chat(
  model='qwen',
  messages=[
  {
    'role': 'user',
    'content': '你能做什么呢？',
  },],
  stream=True,)
  
    
    
    

"""
已完成
"""