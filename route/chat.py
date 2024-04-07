from flask import Blueprint,render_template

bp=Blueprint('chat',__name__,url_prefix='/chat')
@bp.route('/ui')
def ui():
    return render_template('chat.html')