import os
class Config:
    SECRET_KEY=os.urandom(12).hex()
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:Bishwajit_123@localhost:3306/breakbroker'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
