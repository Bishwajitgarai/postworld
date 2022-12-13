from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,DateField
from wtforms.validators import DataRequired,Length
from flask_login import current_user
from brokerapp.models import User
from flask_wtf.file import FileField,FileAllowed



class SendMessage(FlaskForm):
    meassage=StringField("Meassage",render_kw={"placeholder": "Meassage"})
    meassage_time=DateField("Time")
    file=FileField("Add Files",validators=[FileAllowed(["jpg","jpeg","png","jfif"])])
    submit=SubmitField("Send")