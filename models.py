from datetime import datetime
from . import db,login_manager,app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(db.Model,UserMixin):
    """
    id, username, email, image, date, posts
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    mobile = db.Column(db.String(80), nullable=True)
    username = db.Column(db.String(80), nullable=False,unique=True)
    email = db.Column(db.String(120), nullable=False,unique=True)
    image = db.Column(db.String(120), nullable=False,default='default.jpg')
    password = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(12), nullable=False,default=datetime.utcnow())
    posts = db.relationship('Posts',backref='author',lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image}')"