from utils import siwa,CustomResponse,Chat_message,Authorization
from flask import Blueprint, request,Response
from flask_jwt_extended import jwt_required
import ollama
from services import selector,Choice
chatbp=Blueprint('chat',__name__,url_prefix='/chat')

@chatbp.route('/simple_stream', methods=['POST'])
@jwt_required()
@siwa.doc(description='输入文本，返回模型回复',tags=['聊天'],body=Chat_message,header=Authorization)
def chat_with_llama():
    user_message = request.json.get('message',[])
    def generate_response():
        response=ollama.chat(
            model='qwen',
            messages=[{'role': 'user', 'content': user_message}],
            stream=True,
        )


        # 逐条发送模型的回复
        for response_chunk in response:
            yield (response_chunk['message']['content'])+'\n'


    if request.method == 'POST':
        headers = {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
            }
        return Response(generate_response(),mimetype="text/event-stream", headers =headers)
@chatbp.route('/selector',methods=['POST'])
@jwt_required()
@siwa.doc(body=Chat_message,description='输入文本，调控中心返回对应的节点',tags=['聊天'],header=Authorization)
def selector():
    user_message = request.json.get('message',[])
    choice =selector(user_message)
    return CustomResponse(
        message='控制中心反馈',
        data=choice.value,
        status_code=200
    )

    