import os
class Config:
    SECRET_KEY=os.urandom(12).hex()
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:Ams_12345@localhost:3306/breakbroker'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
