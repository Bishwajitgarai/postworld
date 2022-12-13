from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from brokerapp.config import Config
from flask_socketio import SocketIO


db=SQLAlchemy()
bcrypt=Bcrypt()
socketio = SocketIO()
login_manager=LoginManager()
login_manager.login_view='users.login'

login_manager.login_message_category='info'
# login_manager.init_app(app)

def createapp(config_obj=Config):
    app=Flask(__name__)
    app.config.from_object(config_obj)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    from brokerapp.User.routes import users
    app.register_blueprint(users)
    # from flaskblog.flaskapp.Convert.routes import converts
    # app.register_blueprint(converts)
    from brokerapp.Post.routes import posts
    from brokerapp.Utilities.routes import utilities
    from brokerapp.Messages.routes import messages
    from brokerapp.Errors.handelrs import errors
    app.register_blueprint(errors)
    app.register_blueprint(posts)
    app.register_blueprint(utilities)
    app.register_blueprint(messages)
    return app



