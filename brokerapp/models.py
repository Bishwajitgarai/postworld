from brokerapp import  login_manager,db
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedSerializer as Serialize
from brokerapp.config import Config
import os


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
    __tablename__='user'
    username=db.Column(db.String(100))
    email=db.Column(db.String(100))
    image_file=db.Column(db.String(100),default="Pro_default.jpg")
    password=db.Column(db.String(100))
    firstname=db.Column(db.String(100))
    lastname=db.Column(db.String(100))
    dob=db.Column(db.Date)
    category=db.Column(db.String(10))
    password=db.Column(db.String(100))
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    posts=db.relationship('CreatePost',backref='author' ,lazy=True)

    def get_rest_token(self,exp_sec=1500):
        s=Serialize(Config.SECRET_KEY)
        return s.dumps({'id':self.id})

    @staticmethod
    def verify_token(token):
        s=Serialize(Config.SECRET_KEY)
        try:
            user_id=s.loads(token)['id']
        except:
            return None
        return User.query.get(user_id)




class CreatePost(db.Model,UserMixin):
    __tablename__='posts'
    userid=db.Column(db.Integer,db.ForeignKey('user.id'))
    post_create_date=db.Column(db.DateTime,default=datetime.utcnow())
    postid=db.Column(db.Integer,autoincrement=True,primary_key=True)
    post_title=db.Column(db.String(1000))
    post_details=db.Column(db.String(7000))
    post_views=db.Column(db.Integer,default=0)

class PostImages(db.Model,UserMixin):
    __tablename__='postsimages'
    imageid=db.Column(db.Integer,autoincrement=True,primary_key=True)
    postid=db.Column(db.Integer,db.ForeignKey('posts.postid'))
    images_name=db.Column(db.String(400))
    userid=db.Column(db.Integer,db.ForeignKey('user.id'))

class Messages(db.Model,UserMixin):
    __tablename__='messages'
    messageid=db.Column(db.Integer,autoincrement=True,primary_key=True)
    filename=db.Column(db.String(400))
    userid=db.Column(db.Integer,db.ForeignKey('user.id'))
    senderid=db.Column(db.Integer,db.ForeignKey('user.id'))
    messagetime=db.Column(db.DateTime,default=datetime.utcnow())
    messagesdata=db.Column(db.String(3000))













