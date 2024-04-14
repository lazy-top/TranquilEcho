from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from utils import db,jwt,socketio,siwa,cors
from route.user import userbp
from route.chat import chatbp
from route.audio import audiobp
from route.group import groupbp
from route.visitor import visitorbp
import ollama
def create_app():
    class WanmaitFlask(Flask):
        jinja_options = Flask.jinja_options.copy()
        jinja_options.update(dict(variable_start_string='%%',
                                # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
                                variable_end_string='%%',))
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'se*@)&!Nsksmxm102810'
    app.config['JWT_SECRET_KEY'] = 'xs1xs015x1545#$@9451@（#&）0'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/mind'
    app.jinja_env.variable_start_string = '{['
    app.jinja_env.variable_end_string = ']}'
    app.register_blueprint(chatbp)
    app.register_blueprint(userbp)
    app.register_blueprint(audiobp)
    app.register_blueprint(groupbp)
    app.register_blueprint(visitorbp)
   


    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    siwa.init_app(app)
    cors.init_app(app)
    @socketio.on('chat message')
    def handle_message(msg):
        # 使用ollama生成个性化的提示词
        response = ollama.chat(model='qwen',messages=[
    {
      'role': 'system',
      'content': '作为一名心理咨询师，你的职责是帮助患者解决心理问题并提供有效的建议。请描述你如何倾听患者，并根据他们的需求提供适当的建议和支持。你的回答应包括建立信任关系的方法，了解患者的感受和想法，提供实用的建议和指导，以及跟进和帮助患者实现他们的目标。请提供具体的例子和案例，以帮助患者更好地理解你的建议，并提高你的专业性和可信度。让我们一步步来思考。让我们一步一步来思考'
    },
  {
    'role': 'user',
    'content': msg,
  },],
  stream=True,)
        complete_message = ""
        for chunk in response:
            complete_message += chunk['message']['content']
            print(complete_message)
            socketio.emit('bot response', complete_message)
            # 检查是否是完整的消息
        if chunk['message']['content'].endswith(''):
            complete_message = ""  # 重置消息内容

    
    
    @app.route('/')
    def index_ui():
        return render_template('index.html')
    @app.route('/login')
    def login_ui():
     return render_template('login.html')
    @app.route('/contact')
    def contract_ui():
     return render_template('contact.html')
    @app.route('/Privacy_Policy')
    def Privacy_Policy_ui():
     return render_template('Privacy_Policy.html')
    @app.route('/register')
    def register_ui():
     return render_template('register.html')
    @app.route('/chat')
    def chat_ui():
     return render_template('chat.html')
    @app.route('/group')
    def group_ui():
        return render_template('group.html')
    @app.route('/about')
    def about_ui():
        return render_template('about.html')
    @app.route('/services')
    def services_ui():
        return render_template('services.html')
    @app.route('/data')
    def visitor_ui():
        return render_template('data.html')
    @app.route('/create')
    def create_ui():
        return render_template('create.html')
    @app.route('/froget-password')
    def froget_password_ui():  
        return render_template('creat555.html')

    # ...注册蓝图和其他应用配置...

    return app
if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)