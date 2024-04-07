from utils import db
import bcrypt
class User(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(50), unique=True, nullable=False)
       password_hash = db.Column(db.String(100), nullable=False)
       def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)