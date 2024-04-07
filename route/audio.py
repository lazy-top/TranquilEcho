from flask import Blueprint, Response, stream_with_context

bp=Blueprint('audio',__name__,url_prefix='/audio')
@bp.route('/get')
def stream_audio():    
    def generate():        
        with open('your_audio_file.wav', 'rb') as f:            
            data = f.read(1024)            
            while data:                
                yield data                
                data = f.read(1024)
    return Response(stream_with_context(generate()), mimetype='audio/x-wav')