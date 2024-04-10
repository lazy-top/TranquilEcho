from flask import Blueprint, Response, stream_with_context,Flask, request, send_file
from utils import siwa
from flask_jwt_extended import jwt_required
from gtts import gTTS
audiobp=Blueprint('audio',__name__,url_prefix='/audio')
@audiobp.route('/get')
@jwt_required()
@siwa.doc(tags=['音频'])
def stream_audio():
    """
    流式传输音频文件。
    
    该函数不会直接返回音频文件的全部内容，而是将音频文件分块传输，这样可以减少内存占用并提高响应速度。
    
    返回值:
        Response对象，包含流式音频数据，内容类型为'audio/x-wav'。
    """
    def generate():
        """
        生成器函数，用于分块读取音频文件。
        
        使用yield关键字逐块返回音频数据，使得客户端可以一边接收数据一边处理，而不需要等待整个文件加载完毕。
        """
        with open('your_audio_file.wav', 'rb') as f:
            data = f.read(1024)  # 每次读取1024字节
            while data:
                yield data  # 返回数据块给调用者
                data = f.read(1024)  # 继续读取下一个数据块
                
    return Response(stream_with_context(generate()), mimetype='audio/x-wav')

@audiobp.route('/text-to-speech', methods=['POST'])
@siwa.doc(tags=['音频'])
def text_to_speech():
    # 从请求中获取需要转换为语音的文本
    text = request.form['text']
    
    # 使用gTTS库将文本转换为语音，保存为mp3文件
    tts = gTTS(text, lang='zh')
    tts.save("output.mp3")
    
    # 将生成的语音文件以流式数据的形式返回给前端
    return send_file("output.mp3", as_attachment=True)

@audiobp.route('/speech-to-text', methods=['POST'])
@siwa.doc(tags=['音频'])
def speech_to_text():
    """
    将语音转换为文本。
    
    该函数接收一个POST请求，其中包含语音文件的二进制数据。
    
    返回值:
        Response对象，包含转换后的文本。
    """
    pass