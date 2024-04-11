from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from utils import db,jwt,socketio,siwa,cors
from route.user import userbp
from route.chat import chatbp
from route.audio import audiobp
from route.group import groupbp
from route.visitor import visitorbp
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
    @app.route('/')
    def index_ui():
        return render_template('index.html')
    @app.route('/login')
    def login_ui():
     return render_template('login.html')
    @app.route('/ui/contract')
    def contract_ui():
     return render_template('contract.html')
    @app.route('/ui/Privacy_Policy')
    def Privacy_Policy_ui():
     return render_template('Privacy_Policy.html')



    # ...注册蓝图和其他应用配置...

    return app
if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)