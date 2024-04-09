
from flask import Blueprint,render_template, request,Response
from flask_jwt_extended import jwt_required
from flask_socketio import emit,SocketIO
import ollama
sio=SocketIO()
chatbp=Blueprint('chat',__name__,url_prefix='/chat')
@chatbp.route('/ui')
@jwt_required()
def ui():
    return render_template('chat.html')
@chatbp.route('/stream', methods=['POST'])
@jwt_required()
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