from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from utils import db,jwt,socketio
from route.user import userbp
from route.chat import chatbp
from route.audio import audiobp
from route.group import groupbp
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_SECRET_KEY'] = 'xs1xs015x1545#$@9451@（#&）0'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/mind'

    app.register_blueprint(chatbp)
    app.register_blueprint(userbp)
    app.register_blueprint(audiobp)
    app.register_blueprint(groupbp)
   

    swagger = Swagger(app)
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    @app.route('/')
    def open():
        return ""

    # ...注册蓝图和其他应用配置...

    return app
if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)