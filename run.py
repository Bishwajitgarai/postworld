from brokerapp import createapp
# from flaskapp.models import Post,User
from brokerapp import db
app=createapp()
with app.app_context():
    db.create_all()
if __name__=="__main__":
    app.run(debug=True,port=5000, use_reloader=True)