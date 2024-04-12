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

@audiobp.route('/simple_text-to-speech', methods=['POST'])
@siwa.doc(body=Text_to_speech, tags=['音频'])
def simple_text_to_speech():
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


    try:
         # 保存到临时文件
        engine.save_to_file(text, 'temp.mp3')
        engine.runAndWait()
    except Exception as e:
        engine.stop()
        return jsonify(error=f'Failed to convert text to speech: {str(e)}'), 500


    # 读取临时文件并流式返回给前端
    def generate():
        with open('temp.mp3', 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                yield data

    # 以流的形式返回响应
    return Response(generate(), mimetype='audio/mp3')

@audiobp.route('/speech-to-text', methods=['POST'])
@siwa.doc(tags=['音频'])
def speech_to_text():
    """
    将语音转换为文本。
    
    该函数接收一个POST请求，其中包含语音文件的二进制数据。
    
    返回值:
        Response对象，包含转换后的文本。
    """
    # 获取请求中的语音文件
    audio_data = request.files['audio']
    if not audio_data:
        return jsonify(error='No audio file provided'), 400
    try:
        # 将语音转换为文本
        
        
        pass

    except Exception as e:
        return jsonify(error=str(e)), 500