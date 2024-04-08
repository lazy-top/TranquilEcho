from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from utils import db
from route.user import bp
from route.chat import bp
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_SECRET_KEY'] = 'xs1xs015x1545#$@9451@（#&）0'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/mind'

    socketio = SocketIO(app)
    jwt = JWTManager(app)
    app.register_blueprint(bp)

    swagger = Swagger(app)
    db.init_app(app)
    @app.route('/')
    def open():
        return ""

    # ...注册蓝图和其他应用配置...

    return app
if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)