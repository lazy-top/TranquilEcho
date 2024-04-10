import io
from flask import Blueprint, Response, jsonify, stream_with_context,Flask, request, send_file
from utils import siwa,Text_to_speech
from flask_jwt_extended import jwt_required
from gtts import gTTS
import pyttsx3
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



# 假设MAX_TEXT_LENGTH为允许的最大文本长度
MAX_TEXT_LENGTH = 10000

@audiobp.route('/text-to-speech', methods=['POST'])
@siwa.doc(body=Text_to_speech, tags=['音频'])
def text_to_speech():
    # 接收前端传递的文本数据，并进行验证
    text = request.json.get('text', None)
    if not text or len(text) > MAX_TEXT_LENGTH:
        return jsonify(error='Invalid input or text too long'), 400

    # 初始化TTS引擎，并加入异常处理
    try:
        engine = pyttsx3.init()
    except Exception as e:
        return jsonify(error=f'Failed to initialize TTS engine: {str(e)}'), 500

    # 设置语音属性
    engine.setProperty('rate', 150)  # 调整语速

    # 将文本转换为语音并保存到字节缓冲区
    buffer = io.BytesIO()
    try:
        engine.save_to_file(text, buffer)
        engine.runAndWait()
    except Exception as e:
        engine.quit()
        return jsonify(error=f'Failed to convert text to speech: {str(e)}'), 500

    # 移动到缓冲区的开始位置
    buffer.seek(0)

    # 定义一个生成器函数来流式传输音频
    def generate(buffer):
        data = buffer.read(1024)
        while data:
            yield data
            data = buffer.read(1024)

    # 以流的形式返回响应
    return Response(generate(buffer), mimetype='audio/mp3')
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