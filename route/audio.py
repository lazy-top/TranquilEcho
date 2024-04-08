from flask import Blueprint, Response, stream_with_context,Flask, request, send_file

from flask_jwt_extended import jwt_required
from gtts import gTTS
import os
audiobp=Blueprint('audio',__name__,url_prefix='/audio')
@audiobp.route('/get')
@jwt_required()
def stream_audio():    
    def generate():        
        with open('your_audio_file.wav', 'rb') as f:            
            data = f.read(1024)            
            while data:                
                yield data                
                data = f.read(1024)
    return Response(stream_with_context(generate()), mimetype='audio/x-wav')



@audiobp.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    # 从请求中获取需要转换为语音的文本
    text = request.form['text']
    
    # 创建gTTS对象并将文本转换为语音
    tts = gTTS(text, lang='zh')
    tts.save("output.mp3")
    
    # 将生成的语音文件以流式数据的形式返回给前端
    return send_file("output.mp3", as_attachment=True)